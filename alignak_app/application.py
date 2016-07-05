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
        self.hosts_up_item = self.create_items('up')
        self.hosts_down_item = self.create_items('down')
        self.services_up_item = self.create_items('up')
        self.services_down_item = self.create_items('down')
        self.services_unknown_item = self.create_items('unknown')
        self.quit_item = self.create_items(None)

    def main(self):
        """
        Create indicator, menu and main Gtk
        """
        # Get configuration
        self.read_configuration()

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
        img = os.path.abspath('/etc/alignak_app/images/' + self.Config.get('Alignak-App', 'icon'))

        indicator = AppIndicator.Indicator.new(
            app_id,
            img,
            AppIndicator.IndicatorCategory.APPLICATION_STATUS
        )
        indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)

        # Init notify
        Notify.init(app_id)

        return indicator

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
        menu.append(separator_host)
        menu.append(self.services_up_item)
        menu.append(self.services_down_item)
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
        if 'up' == style:
            # img.set_from_stock(Gtk.STOCK_OK, 2)
            img.set_from_file('../etc/images/host_up.png')
            item.connect("activate", self.open_url)
        elif 'down' == style:
            # img.set_from_stock(Gtk.STOCK_STOP, 2)
            img.set_from_file('../etc/images/host_down.png')
            item.connect("activate", self.open_url)
        elif 'unknown' == style:
            # img.set_from_stock(Gtk.STOCK_HELP, 2)
            img.set_from_file('../etc/images/service_unknown.png')
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
        hosts_states = [0, 0]
        services_states = [0, 0, 0]

        # Collect Hosts state
        hosts_data = self.backend_data.get_host_state()
        for key, v in hosts_data.items():
            if 'UP' in v:
                hosts_states[0] += 1
            if 'DOWN' in v:
                hosts_states[1] += 1

        # Collect Services state
        services_data = self.backend_data.get_service_state()
        for key, v in services_data.items():
            if 'OK' in v:
                services_states[0] += 1
            if 'CRITICAL' in v:
                services_states[1] += 1
            if 'UNKNOWN' in v:
                services_states[2] += 1

        return hosts_states, services_states

    def notify_change(self):
        """
        Send a notification if DOWN

        :return: True to continue process
        """
        hosts_states, services_states = self.get_state()

        if (services_states[1] > 0) or (services_states[1] > 0):
            message = "Alignak ALERT: Hosts or Services are DOWN !"
        else:
            message = "Alignak INFO: all is OK :)"

        Notify.Notification.new(
            str(message),
            self.update_hosts_menu(
                hosts_states,
                services_states
            ), None
        ).show()

        return True

    def update_hosts_menu(self, hosts_states, services_states):
        """
        Update items Menu

        :param hosts_states: number of hosts UP or DOWN
        :param services_states: number of services UP, UNKNOWN or DOWN
        """
        if hosts_states[0] > 0:
            str_host_up = 'Hosts UP (' + str(hosts_states[0]) + ')'
            self.hosts_up_item.set_label(str_host_up)
        if hosts_states[1] > 0:
            str_host_nok = 'Hosts DOWN (' + str(services_states[0]) + ')'
            self.hosts_down_item.set_label(str_host_nok)

        if services_states[0] > 0:
            str_service_up = 'Services UP (' + str(hosts_states[1]) + ')'
            self.services_up_item.set_label(str_service_up)
        if services_states[1] > 0:
            str_service_nok = 'Services DOWN (' + str(services_states[1]) + ')'
            self.services_down_item.set_label(str_service_nok)
        if services_states[2] > 0:
            str_service_unk = 'Services UNKNOWN (' + str(services_states[2]) + ')'
            self.services_unknown_item.set_label(str_service_unk)

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
