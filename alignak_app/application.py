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

import os
import signal
import configparser as cfg
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as AppIndicator

gi.require_version('Notify', '0.7')
from gi.repository import Notify

from gi.repository import GLib

from alignak_app.alignak_data import AlignakData
from alignak_app.app_menu import AppMenu


class AlignakApp(object):
    """
        App application

        This is the main class of Alignak-App.
    """

    def __init__(self):
        self.config = None
        self.backend_data = None
        self.indicator = None
        self.app_menu = None

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
        self.config = cfg.ConfigParser()
        self.config.read('/etc/alignak_app/settings.cfg')

    def set_indicator(self):
        """
        Initialize a new Indicator and his notifications

        :return: indicator
        :rtype: Indicator
        """
        # Define ID and build Indicator
        app_id = 'appalignak'
        img = os.path.abspath(
            self.config.get('Config', 'path') +
            self.config.get('Config', 'img') +
            '/' +
            self.config.get('Config', 'icon'))

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

    def notify_change(self):
        """
        Send a notification if DOWN

        :return: True to continue process
        """
        hosts_states, services_states = self.get_state()

        message = "Info: all is OK.)"
        icon = 'ok'

        img = os.path.abspath(
            self.config.get('Config', 'path') +
            self.config.get('Config', 'img') +
            '/' +
            self.config.get('Config', 'ok'))

        if services_states['critical'] <= 0 and hosts_states['down'] <= 0:
            if services_states['unknown'] > 0 or services_states['warning'] > 0:
                icon = 'warning'
                message = "Warning: some Services are unknown or warning."
                img = os.path.abspath(
                    self.config.get('Config', 'path') +
                    self.config.get('Config', 'img') +
                    '/' +
                    self.config.get('Config', 'warning'))
        elif (services_states['critical'] > 0) or (hosts_states['down'] > 0):
            icon = 'alert'
            message = "Alert: Hosts or Services are DOWN !"
            img = os.path.abspath(
                self.config.get('Config', 'path') +
                self.config.get('Config', 'img') +
                '/' +
                self.config.get('Config', 'alert'))

        # If [notifications] is 'true' or 'false'
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
            print('Bad parameters in config file, [notifications]')

        return True

    def get_state(self):
        """
        Check the hosts states.

        :return: number of hosts and services UP, UNKNOWN and DOWN
        """

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
        for key, v in hosts_data.items():
            if 'UP' in v:
                hosts_states['up'] += 1
            if 'DOWN' in v:
                hosts_states['down'] += 1
            if 'UNREACHABLE' in v:
                hosts_states['unreachable'] += 1

        # Collect Services state
        services_data = self.backend_data.get_service_state()
        for key, v in services_data.items():
            if 'OK' in v:
                services_states['ok'] += 1
            if 'CRITICAL' in v:
                services_states['critical'] += 1
            if 'UNKNOWN' in v:
                services_states['unknown'] += 1
            if 'WARNING' in v:
                services_states['warning'] += 1

        return hosts_states, services_states

    def change_icon(self, state):
        if "ok" in state:
            icon = self.config.get('Config', 'ok')
        elif "alert" in state:
            icon = self.config.get('Config', 'alert')
        elif "warning" in state:
            icon = self.config.get('Config', 'warning')
        else:
            icon = self.config.get('Config', 'alignak')

        img = os.path.abspath(
            self.config.get('Config', 'path') +
            self.config.get('Config', 'img') +
            '/' +
            icon)

        self.indicator.set_icon(img)

    def run(self):
        """
        Run application
        """

        # Read settings.cfg
        self.read_configuration()

        # Run main to initialize app
        self.main()

        # Start loop process
        self.start_process()

        # Start main Gtk
        Gtk.main()
        signal.signal(signal.SIGINT, signal.SIG_DFL)
