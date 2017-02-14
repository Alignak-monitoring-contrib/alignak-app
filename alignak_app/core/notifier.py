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
    Notifier manage notifications and collect data from app_backend.
"""

import copy
from logging import getLogger

from alignak_app.core.utils import get_app_config
from alignak_app.dashboard.app_dashboard import Dashboard

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QSystemTrayIcon  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import QTimer  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QSystemTrayIcon  # pylint: disable=import-error
    from PyQt4.QtCore import QTimer  # pylint: disable=import-error

logger = getLogger(__name__)


class AppNotifier(object):
    """
        Class who manage notifications and states of hosts and services.
    """

    first_start = True

    def __init__(self):
        self.app_backend = None
        self.tray_icon = None
        self.dashboard = None
        self.changes = False
        self.notify = True
        self.interval = 0
        self.old_synthesis = None

    def initialise(self, app_backend, tray_icon, dashboard):
        """
       AppNotifier manage notifications and changes

       :param app_backend: AppBackend object
       :type app_backend: alignak_app.core.backend.AppBackend
       :param tray_icon: TrayIcon object
       :type tray_icon: alignak_app.systray.tray_icon.TrayIcon
       :param dashboard: Dashboard object
       :type dashboard: alignak_app.dashboard.app_dashboard.Dashboard
       """

        self.app_backend = app_backend
        self.tray_icon = tray_icon
        self.dashboard = dashboard

        # Define interval
        self.set_interval()

    def set_interval(self):
        """
        Set interval from config.

        """

        interval = int(get_app_config('Alignak-App', 'check_interval'))

        if bool(interval):
            logger.info('Start notifier...')
            logger.debug('Dashboard will be displayed in ' + str(interval) + 's')

            interval *= 1000
        else:
            logger.info('Notifier will not notify Dashboard !')
            interval = 30000
            self.notify = False

        self.interval = interval

    @staticmethod
    def none_synthesis_model():
        """
        Return a synthesis data model

        :return: synthesis model dict
        :rtype: dict
        """

        changes = {
            'hosts': {
                'up': 0,
                'down': 0,
                'unreachable': 0,
                'acknowledge': 0,
                'downtime': 0
            },
            'services': {
                'ok': 0,
                'warning': 0,
                'critical': 0,
                'unknown': 0,
                'unreachable': 0,
                'acknowledge': 0,
                'downtime': 0
            }
        }

        return changes

    def check_data(self):
        """
        Collect data from Backend API object

        """

        synthesis = self.app_backend.synthesis_count()

        print('Old synthesis ', self.old_synthesis)
        print('New synthesis ', synthesis)

        if self.first_start:
            # Simulate old state
            self.old_synthesis = copy.deepcopy(synthesis)
            diff_synthesis = self.none_synthesis_model()

            # Changes to true to apply changes
            self.first_start = False
            self.changes = True
        else:
            if self.old_synthesis == synthesis:
                # No changes
                self.old_synthesis = copy.deepcopy(synthesis)
                diff_synthesis = self.none_synthesis_model()
                self.changes = False
            else:
                # Changes: Get differences
                diff_synthesis = self.diff_last_states(synthesis)
                self.old_synthesis = copy.deepcopy(synthesis)
                self.changes = True

        # TODO: MOVE THIS Define dashboard level
        if synthesis['services']['critical'] > 0 or synthesis['hosts']['down'] > 0:
            level_notif = 'CRITICAL'
        elif synthesis['services']['unknown'] > 0 or \
                synthesis['services']['warning'] > 0 or \
                synthesis['hosts']['unreachable'] > 0:
            level_notif = 'WARNING'
        else:
            level_notif = 'OK'

        # TODO Review this part
        if self.changes:
            self.tray_icon.update_tray.emit(self)
            # Update Menus
            self.tray_icon.update_menu_actions(
                synthesis['hosts'],
                synthesis['services']
            )

            # Send dashboard
            if bool(int(get_app_config('Alignak-App', 'check_interval'))):
                self.dashboard.display_dashboard(
                    level_notif, synthesis['hosts'],
                    synthesis['services'],
                    diff_synthesis
                )
        else:
            logger.info('No Notify.')

        logger.debug('Dashboard Level : ' + str(level_notif))

    def diff_last_states(self, synthesis):
        """
        Check if there have been any change since the last check

        :param synthesis: new synthesis states in dict
        :type synthesis: dict
        :return: diff of twice synthesis in a dict
        :rtype: dict
        """

        logger.debug('Old_states : ' + str(self.old_synthesis))
        logger.debug('New states : ' + str(synthesis))

        diff_synthesis = self.none_synthesis_model()

        for key, _ in self.old_synthesis['hosts'].items():
            if synthesis['hosts'][key] != self.old_synthesis['hosts'][key]:
                cur_diff = synthesis['hosts'][key] - self.old_synthesis['hosts'][key]
                diff_synthesis['hosts'][key] = cur_diff
        for key, _ in self.old_synthesis['services'].items():
            if synthesis['services'][key] != self.old_synthesis['services'][key]:
                cur_diff = synthesis['services'][key] - self.old_synthesis['services'][key]
                diff_synthesis['services'][key] = cur_diff

        return diff_synthesis
