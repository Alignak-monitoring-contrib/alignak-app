#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016:
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
    Notifier manage notifications and collect data from backend.
"""

import copy
from logging import getLogger

from alignak_app.core.backend import AppBackend
from alignak_app.core.utils import get_app_config
from alignak_app.widgets.popup import AppPopup

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QSystemTrayIcon  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import QTimer  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QSystemTrayIcon  # pylint: disable=import-error
    from PyQt4.QtCore import QTimer  # pylint: disable=import-error

logger = getLogger(__name__)


class AppNotifier(QSystemTrayIcon):
    """
    Class who manage notifications and states of hosts and services.
    """

    def __init__(self, icon, backend, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.backend = backend
        self.tray_icon = None
        self.popup = None
        self.notify = True

    def start_process(self, tray_icon):
        """
        Start process loop of application with a QTimer.

        :param tray_icon: QSystemTrayIcon menu.
        :type tray_icon: :class:`~alignak_app.tray_icon.TrayIcon`
        """

        self.tray_icon = tray_icon

        check_interval = int(get_app_config('Alignak-App', 'check_interval'))
        check_interval *= 1000
        logger.debug('Check Interval : ' + str(check_interval))

        timer = QTimer(self)
        timer.start(check_interval)

        self.popup = AppPopup()
        self.popup.initialize_notification()

        logger.info('Initialize notifier...')
        logger.debug('Be notify : ' + str(self.notify))

        timer.timeout.connect(self.check_data)

    @staticmethod
    def basic_diff_model():
        """
        Define a basic model of dict for diff

        :return: model dict for diff
        :rtype: dict
        """
        changes = {
            'hosts': {
                'up': 'no changes',
                'down': 'no changes',
                'unreachable': 'no changes'
            },
            'services': {
                'ok': 'no changes',
                'warning': 'no changes',
                'critical': 'no changes',
                'unknown': 'no changes'
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

        if self.backend.states:
            logger.info('Store old states...')
            old_states = copy.deepcopy(self.backend.states)

        current_states = self.backend.synthesis_count()

        if old_states:
            diff = self.diff_last_check(old_states)

        # Define notification level
        if current_states['services']['critical'] > 0 or current_states['hosts']['down'] > 0:
            level_notif = 'CRITICAL'
        elif current_states['services']['unknown'] > 0 or \
                current_states['services']['warning'] > 0 or \
                current_states['hosts']['unreachable'] > 0:
            level_notif = 'WARNING'
        else:
            level_notif = 'OK'

        logger.debug('Notification Level : ' + str(level_notif))
        logger.debug('Be notify : ' + str(self.notify))

        if self.notify:
            # Trigger changes and send notification
            self.tray_icon.update_menu_actions(
                current_states['hosts'],
                current_states['services']
            )
            self.popup.send_notification(
                level_notif, current_states['hosts'],
                current_states['services'],
                diff
            )

    def diff_last_check(self, old_states):
        """
        Check if there have been any change since the last check

        """

        logger.debug('Old_states : ' + str(old_states))
        logger.debug('New states : ' + str(self.backend.states))

        diff = self.basic_diff_model()

        if old_states == self.backend.states:
            logger.info('[No changes] since the last check...')
            self.notify = False
        else:
            logger.info('[Changes] since the last check !')
            self.notify = True
            for key, _ in self.backend.states['hosts'].items():
                if old_states['hosts'][key] != self.backend.states['hosts'][key]:
                    cur_diff = self.backend.states['hosts'][key] - old_states['hosts'][key]
                    diff['hosts'][key] = cur_diff
            for key, _ in self.backend.states['services'].items():
                if old_states['services'][key] != self.backend.states['services'][key]:
                    cur_diff = \
                        self.backend.states['services'][key] \
                        - old_states['services'][key]
                    diff['services'][key] = cur_diff

        return diff
