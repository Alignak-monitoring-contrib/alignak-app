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
    Application manage process, configuration and global application.
"""

import os
import sys
import signal
from logging import getLogger

from alignak_app.alignak_data import AlignakData
from alignak_app.app_menu import AppMenu
from alignak_app.utils import get_alignak_home

import configparser as cfg

import gi
from gi.repository import GLib  # pylint: disable=no-name-in-module
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # pylint: disable=wrong-import-position
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as AppIndicator  # pylint: disable=wrong-import-position
gi.require_version('Notify', '0.7')
from gi.repository import Notify  # pylint: disable=wrong-import-position


logger = getLogger(__name__)
home_user = get_alignak_home()


class AlignakApp(object):
    """
        Class who create AlignakApp application.
    """

    def __init__(self):
        self.config = None
        self.backend_data = None
        self.indicator = None
        self.app_menu = None
        self.logger = None

    def main(self):
        """
        Create indicator, menu and main Gtk

        """

        # Create Menus
        self.app_menu = AppMenu(self.config)
        self.app_menu.build_items()

        # Connect to Backend
        self.backend_data = AlignakData()
        self.backend_data.log_to_backend(self.config)

        # Add menu to AppIndicator
        indicator = self.set_indicator()
        indicator.set_menu(self.create_menu())

    def read_configuration(self):
        """
        Read the configuration file.

        """

        config_file = get_alignak_home() + '/alignak_app/settings.cfg'

        self.config = cfg.ConfigParser()
        logger.info('Read configuration file...')

        if os.path.isfile(config_file):
            self.config.read(config_file)
            logger.info('Configuration file is OK.')
        else:
            logger.error('Configuration file is missing in [' + config_file + '] !')
            sys.exit('Configuration file is missing in [' + config_file + '] !')

    def set_indicator(self):
        """
        Initialize a new Indicator and his notifications

        :return: Indicator
        :rtype: **gi.repository.AppIndicator3.Indicator**
        """

        # Define ID and build Indicator
        app_id = 'appalignak'
        img_path = home_user \
            + self.config.get('Config', 'path') \
            + self.config.get('Config', 'img') \
            + '/'
        img = os.path.abspath(img_path + self.config.get('Config', 'icon'))

        self.indicator = AppIndicator.Indicator.new(
            app_id,
            img,
            AppIndicator.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)

        # Init notify
        Notify.init(app_id)

        return self.indicator

    def create_menu(self):
        """
        Create the menu, and get first states.

        :return: menu
        :rtype: **gi.repository.Gtk.Menu**
        """
        logger.info('Build menus...')
        menu = Gtk.Menu()
        self.app_menu.build_menu(menu)

        # Get first states
        hosts_states, services_states = self.get_state()
        self.app_menu.update_hosts_menu(hosts_states, services_states)

        return menu

    def start_process(self):
        """
        Start process loop.

        """
        check_interval = int(self.config.get('Alignak-App', 'check_interval'))
        GLib.timeout_add_seconds(check_interval, self.notify_change)

    def notify_change(self):  # pragma: no cover
        """
        Send a notification if DOWN

        :return: True to continue process
        :rtype: bool
        """

        hosts_states, services_states = self.get_state()

        message = "Info: all is OK.)"
        icon = 'ok'

        img_path = home_user \
            + self.config.get('Config', 'path') \
            + self.config.get('Config', 'img') \
            + '/'

        # Initialize img to default
        img = os.path.abspath(img_path + self.config.get('Config', 'ok'))

        if (services_states['ok'] < 0) or (hosts_states['up'] < 0):
            icon = 'error'
            message = "AlignakApp has something broken. Check your logs."
            img = os.path.abspath(img_path + self.config.get('Config', 'error'))
        elif services_states['critical'] <= 0 and hosts_states['down'] <= 0:
            if services_states['unknown'] > 0 or services_states['warning'] > 0:
                icon = 'warning'
                message = "Warning: some Services are unknown or warning."
                img = os.path.abspath(img_path + self.config.get('Config', 'warning'))
        elif (services_states['critical'] > 0) or (hosts_states['down'] > 0):
            icon = 'alert'
            message = "Alert: Hosts or Services are DOWN !"
            img = os.path.abspath(img_path + self.config.get('Config', 'alert'))

        # Notify or Not
        if 'true' in self.config.get('Alignak-App', 'notifications'):
            Notify.Notification.new(
                str(message),
                self.app_menu.update_hosts_menu(
                    hosts_states,
                    services_states
                ),
                img,
            ).show()
            self.change_icon(icon)
        elif 'false' in self.config.get('Alignak-App', 'notifications'):
            self.app_menu.update_hosts_menu(
                hosts_states,
                services_states
            )
            self.change_icon(icon)
        else:
            logger.error('Bad parameters in config file, [notifications]')

        return True

    def get_state(self):
        """
        Check the hosts states.

        :return: number of hosts and services UP, UNKNOWN and DOWN in two dict.
        :rtype: dict
        """

        logger.info('Get state of Host and Services...')
        # Dicts for states
        hosts_states = {
            'up': 0,
            'down': 0,
            'unreachable': 0
        }
        services_states = {
            'ok': 0,
            'critical': 0,
            'unknown': 0,
            'warning': 0
        }

        # Collect Hosts state
        hosts_data = self.backend_data.get_host_state()
        if not hosts_data:
            hosts_states['up'] = -1
        else:
            for _, v in hosts_data.items():
                if 'UP' in v:
                    hosts_states['up'] += 1
                if 'DOWN' in v:
                    hosts_states['down'] += 1
                if 'UNREACHABLE' in v:
                    hosts_states['unreachable'] += 1
            hosts_log = str(hosts_states['up']) + ' host(s) Up, ' \
                + str(hosts_states['down']) + ' host(s) Down, ' \
                + str(hosts_states['unreachable']) + ' host(s) unreachable, '
            logger.info(hosts_log)

        # Collect Services state
        services_data = self.backend_data.get_service_state()
        if not services_data:
            services_states['ok'] = -1
        else:
            for _, v in services_data.items():
                if 'OK' in v:
                    services_states['ok'] += 1
                if 'CRITICAL' in v:
                    services_states['critical'] += 1
                if 'UNKNOWN' in v:
                    services_states['unknown'] += 1
                if 'WARNING' in v:
                    services_states['warning'] += 1
            services_log = str(services_states['ok']) + ' service(s) Ok, ' \
                + str(services_states['warning']) + ' service(s) Warning, ' \
                + str(services_states['critical']) + ' service(s) Critical, ' \
                + str(services_states['unknown']) + ' service(s) Unknown.'
            logger.info(services_log)
        return hosts_states, services_states

    def change_icon(self, state):  # pragma: no cover
        """
        Change icon depending on the hosts / services status

        :param state: icon wanted
        :type state: str
        """

        if "ok" in state:
            icon = self.config.get('Config', 'ok')
        elif "alert" in state:
            icon = self.config.get('Config', 'alert')
        elif "warning" in state:
            icon = self.config.get('Config', 'warning')
        elif "error" in state:
            icon = self.config.get('Config', 'error')
        else:
            icon = self.config.get('Config', 'icon')

        img_path = home_user \
            + self.config.get('Config', 'path') \
            + self.config.get('Config', 'img') \
            + '/'
        img = os.path.abspath(img_path + icon)

        self.indicator.set_icon(img)

    def run(self):  # pragma: no cover
        """
        Run application. read configuration, create menus and start process.

        """

        logger.info('Alignak-App start :)')

        # Read settings.cfg
        self.read_configuration()

        # Run main to initialize app
        self.main()

        # Start loop process
        self.start_process()

        # Start main Gtk
        Gtk.main()
        signal.signal(signal.SIGINT, signal.SIG_DFL)
