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

from alignak_app.alignak_data import AlignakData
from alignak_app.popup import AppPopup
from alignak_app.utils import get_app_config

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

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.alignak_data = None
        self.tray_icon = None
        self.popup = None
        self.notify = False

    def start_process(self, tray_icon):
        """
        Start process loop of application with a QTimer.

        :param tray_icon: QSystemTrayIcon menu.
        :type tray_icon: :class:`~alignak_app.tray_icon.TrayIcon`
        """

        self.tray_icon = tray_icon

        check_interval = int(get_app_config().get('Alignak-App', 'check_interval'))
        check_interval *= 1000

        timer = QTimer(self)
        timer.start(check_interval)

        self.popup = AppPopup()
        self.popup.initialize_notification()

        self.alignak_data = AlignakData()
        self.alignak_data.log_to_backend()

        self.notify = self.notification()

        logger.info('Initialize notifier...')
        timer.timeout.connect(self.check_data)

    @staticmethod
    def notification():
        """
        Check if user want to be notify or not.

        :return: notifications in settings.cfg
        :rtype: bool
        """
        return get_app_config().getboolean('Alignak-App', 'notifications')

    @staticmethod
    def model_changes():
        """
        Define model for changes dict

        :return: model dict for changes
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

        old_states = {}
        changes = self.model_changes()

        if self.notification() and self.alignak_data.states:
            old_states = copy.deepcopy(self.alignak_data.states)

        hosts_states, services_states = self.alignak_data.get_state()

        if self.notification() and old_states:
            changes = self.check_changes(old_states)

        # Check state to prepare popup
        if services_states['critical'] > 0 or hosts_states['down'] > 0:
            title = 'CRITICAL'
        elif services_states['unknown'] > 0 or \
                services_states['warning'] > 0 or \
                hosts_states['unreachable'] > 0:
            title = 'WARNING !'
        else:
            title = 'OK'

        # Trigger changes and send notification
        self.tray_icon.update_menu_actions(hosts_states, services_states)

        if self.notify:
            self.popup.send_notification(title, hosts_states, services_states, changes)

    def check_changes(self, old_states):
        """
        Check if there have been any change since the last check

        """

        logger.debug('Old_states : ' + str(old_states))
        logger.debug('New states : ' + str(self.alignak_data.states))

        changes = self.model_changes()

        if old_states == self.alignak_data.states:
            logger.info('No changes since the last check...')
            self.notify = False
        else:
            logger.info('Changes since the last check !')
            self.notify = True
            for key, _ in self.alignak_data.states['hosts'].items():
                if old_states['hosts'][key] != self.alignak_data.states['hosts'][key]:
                    diff = self.alignak_data.states['hosts'][key] - old_states['hosts'][key]
                    changes['hosts'][key] = diff
            for key, _ in self.alignak_data.states['services'].items():
                if old_states['services'][key] != self.alignak_data.states['services'][key]:
                    diff = self.alignak_data.states['services'][key] - old_states['services'][key]
                    changes['services'][key] = diff

        logger.debug(changes)

        return changes
