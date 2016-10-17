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
    Menu manage the creation of Application menus.
"""

import sys
import os
import webbrowser

from logging import getLogger

from alignak_app.utils import get_alignak_home

from PyQt5.QtWidgets import QSystemTrayIcon  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QMenu  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QAction  # pylint: disable=no-name-in-module
from PyQt5.QtGui import QIcon  # pylint: disable=no-name-in-module


logger = getLogger(__name__)


class AppIcon(QSystemTrayIcon):
    """
        Class who create QMenu and QAction.
    """

    def __init__(self, icon, config, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.config = config
        self.menu = QMenu(parent)
        self.hosts_actions = {}
        self.services_actions = {}
        self.quit_menu = None

    def build_menu(self):
        """
        Initialize and create each action of menu.

        """

        # General path of images
        qicon_path = get_alignak_home() \
            + self.config.get('Config', 'path') \
            + self.config.get('Config', 'img') \
            + '/'

        # Create actions
        self.create_hosts_actions(qicon_path)
        self.create_services_actions(qicon_path)
        self.create_quit_action()
        self.add_actions_to_menu()

        self.setContextMenu(self.menu)

    def create_hosts_actions(self, qicon_path):
        """
        Create hosts actions.

        """
        logger.info('Create Host Actions')

        img_h_up = os.path.abspath(qicon_path + self.config.get('Config', 'host_up'))
        self.hosts_actions['hosts_up'] = QAction(
            QIcon(img_h_up),
            'Host UP (0)',
            self
        )

        img_h_down = os.path.abspath(qicon_path + self.config.get('Config', 'host_down'))
        self.hosts_actions['host_down'] = QAction(
            QIcon(img_h_down),
            'Host DOWN (0)',
            self
        )

        img_h_unreach = os.path.abspath(qicon_path + self.config.get('Config', 'host_unreach'))
        self.hosts_actions['host_unreach'] = QAction(
            QIcon(img_h_unreach),
            'Host UNREACHABLE (0)',
            self
        )

    def create_services_actions(self, qicon_path):
        """
        Create services actions.

        """

        logger.info('Create Service Actions')

        img_s_ok = os.path.abspath(qicon_path + self.config.get('Config', 'service_ok'))
        self.services_actions['services_ok'] = QAction(
            QIcon(img_s_ok),
            'Services OK (0)',
            self
        )

        img_s_warning = os.path.abspath(qicon_path + self.config.get('Config', 'service_warning'))
        self.services_actions['services_warning'] = QAction(
            QIcon(img_s_warning),
            'Services WARNING (0)',
            self
        )

        img_s_critical = os.path.abspath(qicon_path + self.config.get('Config', 'service_critical'))
        self.services_actions['services_critical'] = QAction(
            QIcon(img_s_critical),
            'Services CRITICAL (0)',
            self
        )

        img_s_unknown = os.path.abspath(qicon_path + self.config.get('Config', 'service_unknown'))
        self.services_actions['services_unknown'] = QAction(
            QIcon(img_s_unknown),
            'Services UNKNOWN (0)',
            self
        )

    def create_quit_action(self):
        """
        Create quit action.

        """

        logger.info('Create Quit Actions')
        self.quit_menu = QAction(QIcon('../etc/images/error.svg'), 'Quit', self)
        self.quit_menu.triggered.connect(self.quit_app)

    def add_actions_to_menu(self):
        """
        Add all actions to QMenu.

        """

        logger.info('Add action to menu')
        for h_action in self.hosts_actions:
            self.menu.addAction(self.hosts_actions[h_action])
            self.hosts_actions[h_action].triggered.connect(self.open_url)
        for s_action in self.services_actions:
            self.menu.addAction(self.services_actions[s_action])
            self.services_actions[s_action].triggered.connect(self.open_url)
        self.menu.addAction(self.quit_menu)

    @staticmethod
    def quit_app():
        """
        Quit application.

        """
        sys.exit(0)

    def open_url(self):  # pragma: no cover
        """
        Add a link to Alignak-WebUI on every menu

        """

        target = self.sender()
        label = target.property('text')

        webui_url = 'http://94.76.229.155:6001'

        # Define each filter for items
        if "UP" in label:
            endurl = '/hosts/table?search=ls_state:UP'
        elif "DOWN" in label:
            endurl = '/hosts/table?search=ls_state:DOWN'
        elif "UNREACHABLE" in label:
            endurl = '/hosts/table?search=ls_state:UNREACHABLE'
        elif 'OK' in label:
            endurl = '/services/table?search=ls_state:OK'
        elif 'CRITICAL' in label:
            endurl = '/services/table?search=ls_state:CRITICAL'
        elif 'WARNING' in label:
            endurl = '/services/table?search=ls_state:WARNING'
        elif 'UNKNOWN' in label:
            endurl = '/services/table?search=ls_state:UNKNOWN'
        else:
            endurl = '/dashboard'

        webbrowser.open(webui_url + endurl)
