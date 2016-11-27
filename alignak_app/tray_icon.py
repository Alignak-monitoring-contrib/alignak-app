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
    Tray_icon manage the creation of Application menus.
"""

import sys
import webbrowser

from logging import getLogger

from alignak_app.utils import get_app_config
from alignak_app.status import AlignakStatus
from alignak_app.about import AppAbout
from alignak_app.actions_factory import ActionFactory

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QSystemTrayIcon  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QMenu  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    try:
        __import__('PyQt4')
        from PyQt4.Qt import QSystemTrayIcon  # pylint: disable=import-error
        from PyQt4.Qt import QMenu  # pylint: disable=import-error
    except ImportError:
        sys.exit('\nYou must have PyQt installed to run this app.\nPlease read the doc.')


logger = getLogger(__name__)


class TrayIcon(QSystemTrayIcon):
    """
        Class who create QMenu and QAction.
    """

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QMenu(parent)
        self.alignak_status = None
        self.app_about = None
        self.action_factory = ActionFactory()

    def build_menu(self):
        """
        Initialize and create each action of menu.

        """

        # Create actions
        self.create_status_action()
        self.menu.addSeparator()

        self.create_hosts_actions()
        self.menu.addSeparator()

        self.create_services_actions()
        self.menu.addSeparator()

        self.create_about_action()
        self.menu.addSeparator()

        self.create_quit_action()

        self.setContextMenu(self.menu)

    def create_hosts_actions(self):
        """
        Create hosts actions.

        """

        logger.info('Create Host Actions')

        self.action_factory.create(
            'hosts_up',
            'Hosts UP, Wait...',
            self
        )
        self.action_factory.get('hosts_up').triggered.connect(self.open_url)

        self.action_factory.create(
            'hosts_down',
            'Hosts DOWN, Wait...',
            self
        )
        self.action_factory.get('hosts_down').triggered.connect(self.open_url)

        self.action_factory.create(
            'hosts_unreach',
            'Hosts UNREACHABLE, Wait...',
            self
        )
        self.action_factory.get('hosts_unreach').triggered.connect(self.open_url)

        # Add hosts actions to menu
        self.menu.addAction(self.action_factory.get('hosts_up'))
        self.menu.addAction(self.action_factory.get('hosts_down'))
        self.menu.addAction(self.action_factory.get('hosts_unreach'))

    def create_services_actions(self):
        """
        Create services actions.

        """

        logger.info('Create Service Actions')

        self.action_factory.create(
            'services_ok',
            'Services OK, Wait...',
            self
        )
        self.action_factory.get('services_ok').triggered.connect(self.open_url)

        self.action_factory.create(
            'services_warning',
            'Services WARNING, Wait...',
            self
        )
        self.action_factory.get('services_warning').triggered.connect(self.open_url)

        self.action_factory.create(
            'services_critical',
            'Services CRITICAL, Wait...',
            self
        )
        self.action_factory.get('services_critical').triggered.connect(self.open_url)

        self.action_factory.create(
            'services_unknown',
            'Services UNKNOWN, Wait...',
            self
        )
        self.action_factory.get('services_unknown').triggered.connect(self.open_url)

        # Add services actions to menu
        self.menu.addAction(self.action_factory.get('services_ok'))
        self.menu.addAction(self.action_factory.get('services_warning'))
        self.menu.addAction(self.action_factory.get('services_critical'))
        self.menu.addAction(self.action_factory.get('services_unknown'))

    def create_status_action(self):
        """
        Create AlignakStatus and status action

        """

        self.action_factory.create(
            'icon',
            'Alignak States',
            self
        )

        self.alignak_status = AlignakStatus()
        self.alignak_status.create_status()

        self.action_factory.get('icon').triggered.connect(self.alignak_status.show_states)

        self.menu.addAction(self.action_factory.get('icon'))

    def create_about_action(self):
        """
        Create AppAbout and about action.

        """

        logger.info('Create About Action')

        self.app_about = AppAbout()
        self.app_about.create_window()

        self.action_factory.create(
            'about',
            'About',
            self
        )

        self.action_factory.get('about').triggered.connect(self.app_about.show_about)

        self.menu.addAction(self.action_factory.get('about'))

    def create_quit_action(self):
        """
        Create quit action.

        """

        logger.info('Create Quit Action')

        self.action_factory.create(
            'exit',
            'Quit',
            self
        )

        self.action_factory.get('exit').triggered.connect(self.quit_app)

        self.menu.addAction(self.action_factory.get('exit'))

    def update_menu_actions(self, hosts_states, services_states):
        """
        Update items Menu

        :param hosts_states: number of hosts UP, DOWN or UNREACHABLE
        :type hosts_states: dict
        :param services_states: number of services OK, CRITICAL, WARNING or UNKNOWN
        :type services_states: dict
        """

        logger.info('Update menus...')
        self.action_factory.get('hosts_up').setText(
            'Hosts UP (' + str(hosts_states['up']) + ')')
        self.action_factory.get('hosts_down').setText(
            'Hosts DOWN (' + str(hosts_states['down']) + ')')
        self.action_factory.get('hosts_unreach').setText(
            'Hosts UNREACHABLE (' + str(hosts_states['unreachable']) + ')')

        self.action_factory.get('services_ok').setText(
            'Services OK (' + str(services_states['ok']) + ')')
        self.action_factory.get('services_critical').setText(
            'Services CRITICAL (' + str(services_states['critical']) + ')')
        self.action_factory.get('services_warning').setText(
            'Services WARNING (' + str(services_states['warning']) + ')')
        self.action_factory.get('services_unknown').setText(
            'Services UNKNOWN (' + str(services_states['unknown']) + ')')

    @staticmethod
    def quit_app():  # pragma: no cover
        """
        Quit application.

        """

        sys.exit(0)

    def open_url(self):  # pragma: no cover
        """
        Add a link to Alignak-WebUI on every menu

        """

        target = self.sender()

        webui_url = get_app_config('Webui', 'webui_url')

        # Define each filter for items
        if "UP" in target.text():
            endurl = '/hosts/table?search=ls_state:UP'
        elif "DOWN" in target.text():
            endurl = '/hosts/table?search=ls_state:DOWN'
        elif "UNREACHABLE" in target.text():
            endurl = '/hosts/table?search=ls_state:UNREACHABLE'
        elif 'OK' in target.text():
            endurl = '/services/table?search=ls_state:OK'
        elif 'CRITICAL' in target.text():
            endurl = '/services/table?search=ls_state:CRITICAL'
        elif 'WARNING' in target.text():
            endurl = '/services/table?search=ls_state:WARNING'
        elif 'UNKNOWN' in target.text():
            endurl = '/services/table?search=ls_state:UNKNOWN'
        else:
            endurl = '/dashboard'

        logger.debug('Open url : ' + webui_url + endurl)
        webbrowser.open(webui_url + endurl)
