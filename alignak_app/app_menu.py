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
    App_menu manage menu of application and update values.
"""

import webbrowser
from logging import getLogger
from alignak_app.utils import get_alignak_home

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk  # pylint: disable=wrong-import-position
from gi.repository import Notify  # pylint: disable=wrong-import-position


logger = getLogger(__name__)


class AppMenu(object):
    """
        Class who build items, menus and update them.
    """

    def __init__(self, config):
        """

        :param config: parser config who contains settings
        :type config: :class:`~configparser.ConfigParser`
        """
        self.hosts_up_item = None
        self.hosts_down_item = None
        self.hosts_unreach_item = None
        self.services_up_item = None
        self.services_down_item = None
        self.services_unknown_item = None
        self.services_warning_item = None
        self.quit_item = None
        self.config = config

    def build_items(self):
        """
        Initialize and create each item of menu.

        """
        logger.info('Create menu items ...')
        self.hosts_up_item = self.create_items('h_up')
        self.hosts_down_item = self.create_items('h_down')
        self.hosts_unreach_item = self.create_items('h_unreach')

        self.services_up_item = self.create_items('s_ok')
        self.services_down_item = self.create_items('s_critical')
        self.services_unknown_item = self.create_items('s_warning')
        self.services_warning_item = self.create_items('s_unknown')
        self.quit_item = self.create_items('')

    def create_items(self, style):
        """
        Create each item for menu. Possible values: down, up, None

        :param style: style of menu to create
        :type style: str
        :return: **gi.repository.gtk.ImageMenuItem**
        """
        item = Gtk.ImageMenuItem('')
        img = Gtk.Image()
        img_path = get_alignak_home() \
            + self.config.get('Config', 'path') \
            + self.config.get('Config', 'img') \
            + '/'

        if style == 'h_up':
            img.set_from_file(img_path + self.config.get('Config', 'host_up'))
            item.connect("activate", self.open_url)
        elif style == 'h_down':
            img.set_from_file(img_path + self.config.get('Config', 'host_down'))
            item.connect("activate", self.open_url)
        elif style == 'h_unreach':
            img.set_from_file(img_path + self.config.get('Config', 'host_unreach'))
            item.connect("activate", self.open_url)
        elif style == 's_ok':
            img.set_from_file(img_path + self.config.get('Config', 'service_ok'))
            item.connect("activate", self.open_url)
        elif style == 's_critical':
            img.set_from_file(img_path + self.config.get('Config', 'service_critical'))
            item.connect("activate", self.open_url)
        elif style == 's_warning':
            img.set_from_file(img_path + self.config.get('Config', 'service_warning'))
            item.connect("activate", self.open_url)
        elif style == 's_unknown':
            img.set_from_file(img_path + self.config.get('Config', 'service_unknown'))
            item.connect("activate", self.open_url)
        else:
            img.set_from_stock(Gtk.STOCK_CLOSE, 2)
            item.connect('activate', self.quit_app)

        item.set_image(img)
        item.set_always_show_image(True)

        return item

    def build_menu(self, menu):
        """
        Create Main Menu with its Items. Make a first check for Hosts

        :param menu: Gtk Menu
        :type menu: :class:`~gi.repository.Gtk.Menu`
        :return: menu with all items.
        :rtype: **gi.repository.gtk.Menu**
        """
        # Separators
        separator_host = Gtk.SeparatorMenuItem()
        separator_service = Gtk.SeparatorMenuItem()

        # Building Menu
        logger.info('Add menus to application...')
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

    def open_url(self, item):
        """
        Add a link to WebUI on every menu

        :param item: items of Gtk menu
        :type item: **gi.repository.Gtk.ImageMenuItem**
        """
        assert isinstance(item, Gtk.ImageMenuItem)

        webui_url = self.config.get('Webui', 'webui_url')

        # Define each filter for items
        if "UP" in item.get_label():
            endurl = '/hosts/table?search=ls_state:UP'
        elif "DOWN" in item.get_label():
            endurl = '/hosts/table?search=ls_state:DOWN'
        elif "UNREACHABLE" in item.get_label():
            endurl = '/hosts/table?search=ls_state:UNREACHABLE'
        elif 'OK' in item.get_label():
            endurl = '/services/table?search=ls_state:OK'
        elif 'CRITICAL' in item.get_label():
            endurl = '/services/table?search=ls_state:CRITICAL'
        elif 'WARNING' in item.get_label():
            endurl = '/services/table?search=ls_state:WARNING'
        elif 'UNKNOWN' in item.get_label():
            endurl = '/services/table?search=ls_state:UNKNOWN'
        else:
            endurl = '/dashboard'

        webbrowser.open(webui_url + endurl)

    @staticmethod
    def quit_app(item):
        """
        Quit application

        :param item: item of Gtk menu. Required by **connect**.
        :type item: :class:`~Gtk.ImageMenuItem`
        """
        assert isinstance(item, Gtk.ImageMenuItem)

        logger.warn('Alignak-App stop.')
        Notify.uninit()
        Gtk.main_quit()

    def update_hosts_menu(self, hosts_states, services_states):
        """
        Update items Menu

        :param hosts_states: number of hosts UP, DOWN or UNREACHABLE
        :type hosts_states: dict
        :param services_states: number of services OK, CRITICAL, WARNING or UNKNOWN
        :type services_states: dict
        """

        logger.info('Update menus...')
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
