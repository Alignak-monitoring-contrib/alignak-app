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

        logger.info('Initialize notifier...')
        timer.timeout.connect(self.check_data)

    def check_data(self):
        """
        Collect data from Backend-Client.

        """
        hosts_states, services_states = self.alignak_data.get_state()

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

        notification = get_app_config().getboolean('Alignak-App', 'notifications')

        if notification:
            self.popup.send_notification(title, hosts_states, services_states)
