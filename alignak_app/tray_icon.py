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
import os
import webbrowser

from logging import getLogger

from alignak_app.utils import get_alignak_home, get_template
from alignak_app import __releasenotes__, __version__, __copyright__, __doc_url__, __project_url__
from alignak_app import __application__

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QSystemTrayIcon  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QMenu  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QAction  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QMessageBox  # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QIcon  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import Qt  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    try:
        __import__('PyQt4')
        from PyQt4.Qt import QSystemTrayIcon  # pylint: disable=import-error
        from PyQt4.Qt import QMenu  # pylint: disable=import-error
        from PyQt4.Qt import QAction  # pylint: disable=import-error
        from PyQt4.Qt import QWidget  # pylint: disable=import-error
        from PyQt4.Qt import QMessageBox  # pylint: disable=import-error
        from PyQt4.QtGui import QIcon  # pylint: disable=import-error
    except ImportError:
        sys.exit('\nYou must have PyQt installed to run this app.\nPlease read the doc.')


logger = getLogger(__name__)


class TrayIcon(QSystemTrayIcon):
    """
        Class who create QMenu and QAction.
    """

    def __init__(self, icon, config, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.config = config
        self.menu = QMenu(parent)
        self.hosts_actions = {}
        self.services_actions = {}
        self.about_menu = None
        self.quit_menu = None

    def build_menu(self):
        """
        Initialize and create each action of menu.

        """

        # Create actions
        self.create_hosts_actions()
        self.create_services_actions()
        self.create_about_action()
        self.create_quit_action()
        self.add_actions_to_menu()

        self.setContextMenu(self.menu)

    def create_hosts_actions(self):
        """
        Create hosts actions.

        """

        logger.info('Create Host Actions')

        img_h_up = self.get_icon_path() + self.config.get('Config', 'host_up')
        self.hosts_actions['hosts_up'] = QAction(
            QIcon(img_h_up),
            'Hosts UP, Wait...',
            self
        )
        self.hosts_actions['hosts_up'].triggered.connect(self.open_url)

        img_h_down = self.get_icon_path() + self.config.get('Config', 'host_down')
        self.hosts_actions['hosts_down'] = QAction(
            QIcon(img_h_down),
            'Hosts DOWN, Wait...',
            self
        )
        self.hosts_actions['hosts_down'].triggered.connect(self.open_url)

        img_h_unreach = self.get_icon_path() + self.config.get('Config', 'host_unreach')
        self.hosts_actions['hosts_unreach'] = QAction(
            QIcon(img_h_unreach),
            'Hosts UNREACHABLE, Wait...',
            self
        )
        self.hosts_actions['hosts_unreach'].triggered.connect(self.open_url)

    def create_services_actions(self):
        """
        Create services actions.

        """

        logger.info('Create Service Actions...')

        img_s_ok = self.get_icon_path() + self.config.get('Config', 'service_ok')
        self.services_actions['services_ok'] = QAction(
            QIcon(img_s_ok),
            'Services OK, Wait...',
            self
        )
        self.services_actions['services_ok'].triggered.connect(self.open_url)

        img_s_warning = self.get_icon_path() + self.config.get('Config', 'service_warning')
        self.services_actions['services_warning'] = QAction(
            QIcon(img_s_warning),
            'Services WARNING, Wait...',
            self
        )
        self.services_actions['services_warning'].triggered.connect(self.open_url)

        img_s_critical = self.get_icon_path() + self.config.get('Config', 'service_critical')
        self.services_actions['services_critical'] = QAction(
            QIcon(img_s_critical),
            'Services CRITICAL, Wait...',
            self
        )
        self.services_actions['services_critical'].triggered.connect(self.open_url)

        img_s_unknown = self.get_icon_path() + self.config.get('Config', 'service_unknown')
        self.services_actions['services_unknown'] = QAction(
            QIcon(img_s_unknown),
            'Services UNKNOWN, Wait...',
            self
        )
        self.services_actions['services_unknown'].triggered.connect(self.open_url)

    def create_about_action(self):
        """
        Create about action.

        """

        logger.info('Create About Action')
        img_about = os.path.abspath(self.get_icon_path() + self.config.get('Config', 'about'))
        self.about_menu = QAction(QIcon(img_about), 'About', self)

        self.about_menu.triggered.connect(self.about_message)

    def about_message(self):  # pragma: no cover
        """
        Show about message.

        """

        msg_box = QMessageBox()
        msg_box.setWindowIcon(self.icon())

        about_dict = dict(
            application=__application__,
            version=__version__,
            copyright=__copyright__,
            project_url=__project_url__,
            doc_url=__doc_url__,
            releasenotes=__releasenotes__
        )

        msg = get_template('about.tpl', about_dict, self.config)

        msg_box.about(None, 'About ' + __application__, msg)
        msg_box.show()

    def create_quit_action(self):
        """
        Create quit action.

        """

        logger.info('Create Quit Action')
        img_quit = os.path.abspath(self.get_icon_path() + self.config.get('Config', 'exit'))
        self.quit_menu = QAction(QIcon(img_quit), 'Quit', self)

        self.quit_menu.triggered.connect(self.quit_app)

    def add_actions_to_menu(self):
        """
        Add all actions to QMenu.

        """

        logger.info('Add action to menu')
        self.menu.addAction(self.hosts_actions['hosts_up'])
        self.menu.addAction(self.hosts_actions['hosts_down'])
        self.menu.addAction(self.hosts_actions['hosts_unreach'])
        self.menu.addSeparator()

        self.menu.addAction(self.services_actions['services_ok'])
        self.menu.addAction(self.services_actions['services_warning'])
        self.menu.addAction(self.services_actions['services_critical'])
        self.menu.addAction(self.services_actions['services_unknown'])
        self.menu.addSeparator()

        self.menu.addAction(self.about_menu)
        self.menu.addAction(self.quit_menu)

    def update_menu_actions(self, hosts_states, services_states):
        """
        Update items Menu

        :param hosts_states: number of hosts UP, DOWN or UNREACHABLE
        :type hosts_states: dict
        :param services_states: number of services OK, CRITICAL, WARNING or UNKNOWN
        :type services_states: dict
        """

        logger.info('Update menus...')
        self.hosts_actions['hosts_up'].setText(
            'Hosts UP (' + str(hosts_states['up']) + ')')
        self.hosts_actions['hosts_down'].setText(
            'Hosts DOWN (' + str(hosts_states['down']) + ')')
        self.hosts_actions['hosts_unreach'].setText(
            'Hosts UNREACHABLE (' + str(hosts_states['unreachable']) + ')')

        self.services_actions['services_ok'].setText(
            'Services OK (' + str(services_states['ok']) + ')')
        self.services_actions['services_critical'].setText(
            'Services CRITICAL (' + str(services_states['critical']) + ')')
        self.services_actions['services_warning'].setText(
            'Services WARNING (' + str(services_states['warning']) + ')')
        self.services_actions['services_unknown'].setText(
            'Services UNKNOWN (' + str(services_states['unknown']) + ')')

    def get_icon_path(self):
        """
        Get the path for all icons

        :return: path of icon
        :rtype: str
        """
        icon_path = get_alignak_home() \
            + self.config.get('Config', 'path') \
            + self.config.get('Config', 'img') \
            + '/'
        return icon_path

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

        webui_url = self.config.get('Webui', 'webui_url')

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

        webbrowser.open(webui_url + endurl)
