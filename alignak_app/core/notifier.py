#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2017:
#   Matthieu Estrada, ttamalfor@gmail.com
#
# This file is part of (AlignakApp).
#
# (AlignakApp) is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# (AlignakApp) is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with (AlignakApp).  If not, see <http://www.gnu.org/licenses/>.

"""
    Notifier manage notifications and collect data from AppBackend.
"""

import copy
import datetime
from logging import getLogger

from alignak_app.core.utils import get_app_config
from alignak_app.core.data_manager import data_manager
from alignak_app.models.item_livesynthesis import LiveSynthesis
from alignak_app.widgets.banner import send_banner


logger = getLogger(__name__)


class AppNotifier(object):
    """
        Class who manage notifications and states of hosts and services.
    """

    first_start = True

    def __init__(self):
        self.tray_icon = None
        self.dashboard = None
        self.changes = False
        self.interval = 0
        self.old_synthesis = None
        self.old_notifications = []

    def initialize(self, tray_icon, dashboard):
        """
       AppNotifier manage notifications and changes

       :param tray_icon: TrayIcon object
       :type tray_icon: alignak_app.systray.tray_icon.TrayIcon
       :param dashboard: Dashboard object
       :type dashboard: alignak_app.dashboard.app_dashboard.Dashboard
       """

        self.tray_icon = tray_icon
        self.dashboard = dashboard

        # Define interval
        self.set_interval()

        logger.info('Start notifier...')

    def set_interval(self):
        """
        Set interval from config

        """

        interval = int(get_app_config('Alignak-App', 'synthesis_interval'))

        if bool(interval) and interval > 0:
            logger.debug('Dashboard will be updated in %ss', str(interval))
            interval *= 1000
        else:  # pragma: no cover - not testable
            logger.error(
                '"synthesis_interval" option must be greater than 0. Replace by default: 30s'
            )
            interval = 30000

        self.interval = interval

    def check_data(self):
        """
        Check data from Backend API, emit pyqtSignal if there is change to update QWidgets

        """

        # Send notifications
        self.send_notifications()

        # Update Synthesis
        synthesis = data_manager.get_synthesis_count()

        if self.first_start:
            # Simulate old state
            self.old_synthesis = copy.deepcopy(synthesis)
            diff_synthesis = LiveSynthesis.get_synthesis_count_model()

            # Changes to true to apply changes
            self.first_start = False
            self.changes = True
        else:  # pragma: no cover - not testable
            if self.old_synthesis == synthesis:
                # No changes
                self.old_synthesis = copy.deepcopy(synthesis)
                diff_synthesis = LiveSynthesis.get_synthesis_count_model()
                self.changes = False
            else:
                # Changes: Get differences
                diff_synthesis = self.diff_last_states(synthesis)
                self.old_synthesis = copy.deepcopy(synthesis)
                self.changes = True

        if self.changes:
            # Emit pyqtSignals to update TrayIcon and Dashboard
            logger.info('Changes since last check...')
            self.tray_icon.update_tray.emit(synthesis)
            self.dashboard.dashboard_updated.emit(synthesis, diff_synthesis)
        else:
            logger.info('No Changes.')

    def diff_last_states(self, synthesis):
        """
        Return the synthesis differences since the last check

        :param synthesis: new synthesis states in dict
        :type synthesis: dict
        :return: diff of twice synthesis in a dict
        :rtype: dict
        """

        logger.debug('Old_states : ' + str(self.old_synthesis))
        logger.debug('New states : ' + str(synthesis))

        diff_synthesis = LiveSynthesis.get_synthesis_count_model()

        for key, _ in self.old_synthesis['hosts'].items():
            if synthesis['hosts'][key] != self.old_synthesis['hosts'][key]:
                cur_diff = synthesis['hosts'][key] - self.old_synthesis['hosts'][key]
                diff_synthesis['hosts'][key] = cur_diff
        for key, _ in self.old_synthesis['services'].items():
            if synthesis['services'][key] != self.old_synthesis['services'][key]:
                cur_diff = synthesis['services'][key] - self.old_synthesis['services'][key]
                diff_synthesis['services'][key] = cur_diff

        return diff_synthesis

    def send_notifications(self):
        """
        Get the last notifications

        """

        notifications = data_manager.database['notifications']
        logger.debug('%s founded: ', str(notifications))

        for notif in notifications:
            # If the notification has not already been sent to the last check
            if notif.item_id not in self.old_notifications:
                message_split = notif.data['message'].split(';')
                item_type = 'HOST' if 'HOST' in message_split[0] else 'SERVICE'
                host = message_split[1]
                if 'SERVICE' in item_type:
                    service = message_split[2]
                    state = message_split[3]
                    output = message_split[5]
                else:
                    service = ''
                    state = message_split[2]
                    output = message_split[4]

                # Convert updated date to user local time
                gmt_time = datetime.datetime.strptime(
                    notif.data['_updated'], "%a, %d %b %Y %H:%M:%S GMT"
                )
                local_time = gmt_time.replace(
                    tzinfo=datetime.timezone.utc) \
                    .astimezone(tz=None) \
                    .strftime("%a, %d %b %Y %H:%M:%S %Z")

                # Define message
                if service:
                    message = "%s(%s) [%s]: %s - %s" % (
                        service, host, state, output, local_time
                    )
                else:
                    message = "%s [%s]: %s - %s" % (host, state, output, local_time)

                send_banner(state, message)
                logger.info("Send history notification: [%s] - %s", state, str(message))

                self.old_notifications.append(notif.item_id)
