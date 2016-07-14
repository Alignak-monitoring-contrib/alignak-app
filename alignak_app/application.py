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
import webbrowser
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


class AlignakApp(object):
    """
        App application

        This is the main class of Alignak-App.
    """

    def __init__(self):
        self.Config = None
        self.backend_data = None
        self.hosts_up_item = None
        self.hosts_down_item = None
        self.hosts_unreach_item = None
        self.services_up_item = None
        self.services_down_item = None
        self.services_unknown_item = None
        self.services_warning_item = None
        self.quit_item = None

    def main(self):
        """
        Create indicator, menu and main Gtk
        """
        # Get configuration
        self.read_configuration()
        self.build_items()

        # Connect to Backend
        self.backend_data = AlignakData()
        self.backend_data.log_to_backend(self.Config)

        # Build Menu
        indicator = self.set_indicator()
        indicator.set_menu(self.build_menu())

        self.start_process()

        # Main Gtk
        Gtk.main()

    def read_configuration(self):
        self.Config = cfg.ConfigParser()
        self.Config.read('/etc/alignak_app/settings.cfg')

    def set_indicator(self):
        """
        Initialize a new Indicator and his notifications

        :return: indicator
        :rtype: Indicator
        """
        # Define ID and build Indicator
        app_id = 'appalignak'
        img = os.path.abspath(
            self.Config.get('Config', 'path') +
            self.Config.get('Config', 'img') +
            '/' +
            self.Config.get('Config', 'icon'))

        indicator = AppIndicator.Indicator.new(
            app_id,
            img,
            AppIndicator.IndicatorCategory.APPLICATION_STATUS
        )
        indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)

        # Init notify
        Notify.init(app_id)

        return indicator

    def build_items(self):
        """
        Initialize and create each items
        """
        self.hosts_up_item = self.create_items('h_up')
        self.hosts_down_item = self.create_items('h_down')
        self.hosts_unreach_item = self.create_items('h_unreach')

        self.services_up_item = self.create_items('s_ok')
        self.services_down_item = self.create_items('s_critical')
        self.services_unknown_item = self.create_items('s_warning')
        self.services_warning_item = self.create_items('s_unknown')
        self.quit_item = self.create_items('')

    def build_menu(self):
        """
        Create Main Menu with its Items. Make a first check for Hosts

        :return: menu
        :rtype: gtk.Menu
        """
        separator_host = Gtk.SeparatorMenuItem()
        separator_service = Gtk.SeparatorMenuItem()

        # Building Menu
        menu = Gtk.Menu()
        menu.append(self.hosts_up_item)
        menu.append(self.hosts_down_item)
        menu.append(self.hosts_unreach_item)
        menu.append(separator_host)
        menu.append(self.services_up_item)
        menu.append(self.services_down_item)
        menu.append(self.services_warning_item)
        menu.append(self.services_unknown_item)
        menu.append(separator_service)
        menu.append(self.quit_item)

        menu.show_all()

        # Get first states
        hosts_states, services_states = self.get_state()
        self.update_hosts_menu(hosts_states, services_states)

        return menu

    def open_url(self, source):
        """
        Add a web link on every menu

        :param source: source of connector
        """
        webui_url = self.Config.get('Webui', 'webui_url')
        webbrowser.open(webui_url + '/hosts')

    def create_items(self, style):
        """
        Create each item for menu. Possible values: down, up, None
        :param style: style of menu to create
        :return: gtk.ImageMenuItem
        """
        item = Gtk.ImageMenuItem('')
        img = Gtk.Image()
        img_path = self.Config.get('Config', 'path') + self.Config.get('Config', 'img')

        if 'h_up' == style:
            img.set_from_file(img_path + '/' + self.Config.get('Config', 'host_up'))
            item.connect("activate", self.open_url)
        elif 'h_down' == style:
            img.set_from_file(img_path + '/' + self.Config.get('Config', 'host_down'))
            item.connect("activate", self.open_url)
        elif 'h_unreach' == style:
            img.set_from_file(img_path + '/' + self.Config.get('Config', 'host_unreach'))
            item.connect("activate", self.open_url)
        elif 's_ok' == style:
            img.set_from_file(img_path + '/' + self.Config.get('Config', 'service_ok'))
            item.connect("activate", self.open_url)
        elif 's_critical' == style:
            img.set_from_file(img_path + '/' + self.Config.get('Config', 'service_critical'))
            item.connect("activate", self.open_url)
        elif 's_warning' == style:
            img.set_from_file(img_path + '/' + self.Config.get('Config', 'service_warning'))
            item.connect("activate", self.open_url)
        elif 's_unknown' == style:
            img.set_from_file(img_path + '/' + self.Config.get('Config', 'service_unknown'))
            item.connect("activate", self.open_url)
        else:
            img.set_from_stock(Gtk.STOCK_CLOSE, 2)
            item.connect('activate', self.quit_app)
        item.set_image(img)
        item.set_always_show_image(True)

        return item

    def start_process(self):
        """
        Start process loop.
        """
        check_interval = int(self.Config.get('Alignak-App', 'check_interval'))
        GLib.timeout_add_seconds(check_interval, self.notify_change)

    def get_state(self):
        """
        Check the hosts states.

        :return: number of hosts and services UP, UNKNOWN and DOWN
        """
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

    def notify_change(self):
        """
        Send a notification if DOWN

        :return: True to continue process
        """
        hosts_states, services_states = self.get_state()

        message = "Info: all is OK.)"
        img = os.path.abspath(
            self.Config.get('Config', 'path') +
            self.Config.get('Config', 'img') +
            '/' +
            self.Config.get('Config', 'ok'))

        if services_states['critical'] <= 0 and hosts_states['down'] <= 0:
            if services_states['unknown'] > 0 or services_states['warning'] > 0:
                message = "Warning: some Services are unknown or warning."
                img = os.path.abspath(
                    self.Config.get('Config', 'path') +
                    self.Config.get('Config', 'img') +
                    '/' +
                    self.Config.get('Config', 'warning'))
        elif (services_states['critical'] > 0) or (hosts_states['down'] > 0):
            message = "Alert: Hosts or Services are DOWN !"
            img = os.path.abspath(
                self.Config.get('Config', 'path') +
                self.Config.get('Config', 'img') +
                '/' +
                self.Config.get('Config', 'alert'))

        Notify.Notification.new(
            str(message),
            self.update_hosts_menu(
                hosts_states,
                services_states
            ),
            img,
        ).show()

        return True

    def update_hosts_menu(self, hosts_states, services_states):
        """
        Update items Menu

        :param hosts_states: number of hosts UP or DOWN
        :param services_states: number of services UP, UNKNOWN or DOWN
        """
        self.hosts_up_item.set_label(
            'Hosts UP (' + str(hosts_states['up']) + ')')
        self.hosts_down_item.set_label(
            'Hosts DOWN (' + str(hosts_states['down']) + ')')
        self.hosts_unreach_item.set_label(
            'Hosts UNREACHABLE (' + str(hosts_states['unreachable']) + ')')

        self.services_up_item.set_label(
            'Services OK (' + str(services_states['ok']) + ')')
        self.services_down_item.set_label(
            'Services CRITICAL (' + str(services_states['critical']) + ')')
        self.services_warning_item.set_label(
            'Services WARNING (' + str(services_states['warning']) + ')')
        self.services_unknown_item.set_label(
            'Services UNKNOWN (' + str(services_states['unknown']) + ')')

    @staticmethod
    def quit_app(source):
        """
        Quit application

        :param source: source of connector
        """
        Notify.uninit()
        Gtk.main_quit()

    def run(self):
        """
        Run application
        """
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.main()
