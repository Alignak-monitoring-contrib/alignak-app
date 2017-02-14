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

    def __init__(self, app_backend, tray_icon):
        """

        :param app_backend: App Backend
        :type app_backend: alignak_app.core.backend.AppBackend
        :param tray_icon:
        """
        self.app_backend = app_backend
        self.tray_icon = tray_icon
        self.dashboard = Dashboard()
        self.dashboard.initialize()
        self.notify = True
        self.interval = 0
        self.old_synthesis = self.basic_diff_model()

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
            logger.info('Notifier will not display Dashboard !')
            interval = 30000

        self.interval = interval

    @staticmethod
    def basic_diff_model():
        """
        Define a basic model of dict for diff

        :return: model dict for diff
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
        Collect data from Backend-Client.

        """

        synthesis = self.app_backend.synthesis_count()
        print('Old synthesis ', self.old_synthesis)
        print('New synthesis ', synthesis)

        if self.old_synthesis != synthesis:
            print('Changes')
            diff_synthesis = self.diff_since_last_check(synthesis)
            self.old_synthesis = copy.deepcopy(synthesis)
            self.notify = True
        else:
            print('No Changes')
            diff_synthesis = self.basic_diff_model()
            self.old_synthesis = copy.deepcopy(synthesis)
            self.notify = False

        # Define dashboard level
        if synthesis['services']['critical'] > 0 or synthesis['hosts']['down'] > 0:
            level_notif = 'CRITICAL'
        elif synthesis['services']['unknown'] > 0 or \
                synthesis['services']['warning'] > 0 or \
                synthesis['hosts']['unreachable'] > 0:
            level_notif = 'WARNING'
        else:
            level_notif = 'OK'

        if self.notify:
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

    def diff_since_last_check(self, synthesis):
        """
        Check if there have been any change since the last check

        :param synthesis: new synthesis states in dict
        :type synthesis: dict
        :return: diff of twice synthesis in a dict
        :rtype: dict
        """

        logger.debug('Old_states : ' + str(self.old_synthesis))
        logger.debug('New states : ' + str(synthesis))

        diff_synthesis = self.basic_diff_model()

        for key, _ in self.old_synthesis['hosts'].items():
            if synthesis['hosts'][key] != self.old_synthesis['hosts'][key]:
                cur_diff = synthesis['hosts'][key] - self.old_synthesis['hosts'][key]
                diff_synthesis['hosts'][key] = cur_diff
        for key, _ in self.old_synthesis['services'].items():
            if synthesis['services'][key] != self.old_synthesis['services'][key]:
                cur_diff = synthesis['services'][key] - self.old_synthesis['services'][key]
                diff_synthesis['services'][key] = cur_diff

        return diff_synthesis
