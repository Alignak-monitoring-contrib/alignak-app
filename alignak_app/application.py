#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import signal
import webbrowser
import configparser as cfg
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator

gi.require_version('Notify', '0.7')
from gi.repository import Notify as notify

from gi.repository import GLib as glib

from alignak_app.alignak_data import AlignakData


class AlignakApp(object):
    """
        App application

        This is the main class of Alignak-App.
    """

    def __init__(self):
        self.Config = None
        self.backend_data = None
        self.up_item = self.create_items('down')
        self.down_item = self.create_items('up')
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

        # Set Indicator
        app = self.set_indicator()

        self.start_process()

        # Main Gtk
        gtk.main()

    def read_configuration(self):
        self.Config = cfg.ConfigParser()
        self.Config.read('etc/settings.cfg')

    def set_indicator(self):
        """
        Initialize a new Indicator and his notifications

        :return: indicator
        :rtype: Indicator
        """
        # Define ID and build Indicator
        APPINDICATOR_ID = 'appalignak'
        img = os.path.abspath('images/' + self.Config.get('Alignak-App', 'icon'))

        indicator = appindicator.Indicator.new(
            APPINDICATOR_ID,
            img,
            appindicator.IndicatorCategory.SYSTEM_SERVICES
        )
        indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

        # Create Menu
        indicator.set_menu(self.build_menu())

        # Init notify
        notify.init(APPINDICATOR_ID)

        return indicator

    def build_menu(self):
        """
        Create Main Menu with its Items. Make a first check for Hosts

        :return: menu
        :rtype: gtk.Menu
        """
        # Build Menu
        menu = gtk.Menu()
        menu.append(self.up_item)
        menu.append(self.down_item)
        menu.append(self.quit_item)
        menu.show_all()

        # Get first states
        UP, DOWN = self.get_state()
        self.update_hosts_menu(UP, DOWN)

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
        item = gtk.ImageMenuItem('')
        img = gtk.Image()
        if 'down' == style:
            img.set_from_stock(gtk.STOCK_YES, 2)
            item.connect("activate", self.open_url)
        elif 'up' == style:
            img.set_from_stock(gtk.STOCK_CANCEL, 2)
            item.connect("activate", self.open_url)
        else:
            img.set_from_stock(gtk.STOCK_CLOSE, 2)
            item.connect('activate', self.quit_app)

        item.set_image(img)
        item.set_always_show_image(True)

        return item

    def start_process(self):
        """
        Start process loop.
        """
        check_interval = int(self.Config.get('Alignak-App', 'check_interval'))
        glib.timeout_add_seconds(check_interval, self.notify_change)

    def get_state(self):
        """
        Check the hosts states.

        :return: number of UP and DOWN
        """
        UP = 0
        DOWN = 0
        data = self.backend_data.get_host_state()

        for key, v in data.items():
            if 'UP' in v:
                UP += 1
            if 'DOWN' in v:
                DOWN += 1
        return UP, DOWN

    def notify_change(self):
        """
        Send a notification if DOWN

        :return: True to continue process
        """
        UP, DOWN = self.get_state()

        if DOWN > 0:
            message = "Alignak ALERT: Hosts are DOWN !"
        else:
            message = "Alignak INFO: all is OK :)"

        notify.Notification.new(str(message), self.update_hosts_menu(UP, DOWN), None).show()

        return True

    def update_hosts_menu(self, UP, DOWN):
        """
        Update items Menu

        :param UP: number of hosts UP
        :param DOWN: number of hosts DOWN
        """
        if UP > 0:
            str_UP = 'Hosts UP (' + str(UP) + ')'
            self.up_item.set_label(str_UP)

        if DOWN > 0:
            str_NOK = 'Hosts DOWN (' + str(DOWN) + ')'
            self.down_item.set_label(str_NOK)

    @staticmethod
    def quit_app(source):
        """
        Quit application

        :param source: source of connector
        """
        notify.uninit()
        gtk.main_quit()

    def run(self):
        """
        Run application
        """
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.main()
