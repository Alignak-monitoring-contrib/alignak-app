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
# TODO : update doc
"""
    TODO
"""

import sys
import webbrowser

from logging import getLogger
from PyQt5.QtWidgets import QSystemTrayIcon
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon


logger = getLogger(__name__)


class AppIcon(QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QMenu(parent)
        self.hosts_actions = {}
        self.services_actions = {}
        self.quit_menu = None
        self.build_menu()
        self.setContextMenu(self.menu)
        # TODO add config to this class

    def build_menu(self):
        """
        Initialize and create each item of menu.

        """

        self.create_hosts_actions()
        self.create_services_actions()
        self.create_quit_action()
        self.add_actions_to_menu()

    def create_hosts_actions(self):
        print('Create Host Actions')
        self.hosts_actions['hosts_up'] = QAction(
            QIcon('../etc/images/host_up.svg'),
            'Host UP (0)',
            self
        )
        self.hosts_actions['host_down'] = QAction(
            QIcon('../etc/images/host_down.svg'),
            'Host DOWN (0)',
            self
        )
        self.hosts_actions['host_unreach'] = QAction(
            QIcon('../etc/images/host_unreach.svg'),
            'Host UNREACHABLE (0)',
            self
        )

    def create_services_actions(self):
        print('Create Service Actions')

        self.services_actions['services_ok'] = QAction(
            QIcon('../etc/images/service_ok.svg'),
            'Services OK (0)',
            self
        )
        self.services_actions['services_warning'] = QAction(
            QIcon('../etc/images/service_warning.svg'),
            'Services WARNING (0)',
            self
        )
        self.services_actions['services_critical'] = QAction(
            QIcon('../etc/images/service_critical.svg'),
            'Services CRITICAL (0)',
            self
        )
        self.services_actions['services_unknown'] = QAction(
            QIcon('../etc/images/service_unknown.svg'),
            'Services UNKNOWN (0)',
            self
        )

    def create_quit_action(self):
        print('Create Quit Actions')
        self.quit_menu = QAction(QIcon('../etc/images/error.svg'), 'Quit', self)
        self.quit_menu.triggered.connect(self.quit_app)

    def add_actions_to_menu(self):
        print('Add action to menu')
        for h_action in self.hosts_actions:
            print(self.hosts_actions[h_action])
            self.menu.addAction(self.hosts_actions[h_action])
            self.hosts_actions[h_action].triggered.connect(self.open_url)
        for s_action in self.services_actions:
            print(self.services_actions[s_action])
            self.menu.addAction(self.services_actions[s_action])
            self.services_actions[s_action].triggered.connect(self.open_url)
        self.menu.addAction(self.quit_menu)

    @staticmethod
    def quit_app():
        sys.exit(0)

    def open_url(self):  # pragma: no cover
        """
        Add a link to WebUI on every menu

        :param item: items of Gtk menu
        :type item: **gi.repository.Gtk.ImageMenuItem**
        """
        # assert isinstance(item, QAction)

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


