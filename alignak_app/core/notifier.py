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
        self.app_backend = app_backend
        self.tray_icon = tray_icon
        self.popup = Dashboard()
        self.popup.initialize()
        self.notify = True
        self.interval = 0

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

        # Init dict
        old_states = {}
        diff = self.basic_diff_model()

        if self.app_backend.states:
            logger.info('Store old states...')
            old_states = copy.deepcopy(self.app_backend.states)

        current_states = self.app_backend.synthesis_count()

        if old_states:
            diff = self.diff_since_last_check(old_states)

        # Define dashboard level
        if current_states['services']['critical'] > 0 or current_states['hosts']['down'] > 0:
            level_notif = 'CRITICAL'
        elif current_states['services']['unknown'] > 0 or \
                current_states['services']['warning'] > 0 or \
                current_states['hosts']['unreachable'] > 0:
            level_notif = 'WARNING'
        else:
            level_notif = 'OK'

        if self.notify:
            # Update Menus
            self.tray_icon.update_menu_actions(
                current_states['hosts'],
                current_states['services']
            )

            # Send dashboard
            if bool(int(get_app_config('Alignak-App', 'check_interval'))):
                self.popup.display_dashboard(
                    level_notif, current_states['hosts'],
                    current_states['services'],
                    diff
                )
        else:
            logger.info('No Notify.')

        logger.debug('Dashboard Level : ' + str(level_notif))

    def diff_since_last_check(self, old_states):
        """
        Check if there have been any change since the last check

        """

        logger.debug('Old_states : ' + str(old_states))
        logger.debug('New states : ' + str(self.app_backend.states))

        diff = self.basic_diff_model()

        if old_states == self.app_backend.states:
            logger.info('[No changes] since the last check...')
            self.notify = False
        else:
            logger.info('[Changes] since the last check !')
            self.notify = True
            for key, _ in self.app_backend.states['hosts'].items():
                if old_states['hosts'][key] != self.app_backend.states['hosts'][key]:
                    cur_diff = self.app_backend.states['hosts'][key] - old_states['hosts'][key]
                    diff['hosts'][key] = cur_diff
            for key, _ in self.app_backend.states['services'].items():
                if old_states['services'][key] != self.app_backend.states['services'][key]:
                    cur_diff = \
                        self.app_backend.states['services'][key] \
                        - old_states['services'][key]
                    diff['services'][key] = cur_diff

        return diff
