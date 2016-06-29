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

from alignak_app import alignak_data as ad

class alignak_app(object):
    """
        App application
    """

    def __init__(self):
        # Read config
        self.Config = cfg.ConfigParser()
        self.Config.read('etc/settings.cfg')

        # General Variables
        self.img = os.path.abspath('images/' + self.Config.get('Alignak-App', 'icon'))
        self.backend = ad.login_backend(self.Config)

        # Menu Items
        self.up_item = gtk.ImageMenuItem('')
        self.down_item = gtk.ImageMenuItem('')
        self.item_quit = gtk.ImageMenuItem('Quit')

    def main(self):
        """
        Create indicator, menu and main Gtk
        """
        # Set Indicator
        app = self.set_indicator()

        # Update Menu
        self.start_process()

        # Main Gtk
        gtk.main()

    def set_indicator(self):
        """
        Initialize a new Indicator and his notifications

        :return: indicator
        :rtype: Indicator
        """
        # Define ID and build Indicator
        APPINDICATOR_ID = 'appalignak'
        indicator = appindicator.Indicator.new(APPINDICATOR_ID, self.img, appindicator.IndicatorCategory.SYSTEM_SERVICES)
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
        # Get first states
        UP, DOWN = self.get_state()
        self.update_hosts_menu(UP, DOWN)

        # Create Menu with Items
        menu = gtk.Menu()
        self.build_menu_item(self.up_item, self.down_item, self.item_quit)

        menu.append(self.up_item)
        menu.append(self.down_item)
        menu.append(self.item_quit)
        menu.show_all()

        return menu

    def open_url(self, source):
        """
        Add a web link on menu

        :param source: source of connector
        """

        webui_url = self.Config.get('Webui', 'webui_url')
        webbrowser.open(webui_url + '/hosts')

    def build_menu_item(self, up_item, down_item, item_quit):
        """
        Decorate each Menu items and add connectors.

        :param up_item: menu for hosts who are UP
        :param down_item: menu for hosts who are DOWN
        :param item_quit: menu to quit application
        """
        # UP Item
        img_up = gtk.Image()
        img_up.set_from_stock(gtk.STOCK_YES, 2)
        up_item.set_image(img_up)
        up_item.set_always_show_image(True)

        # Down Item
        img_down = gtk.Image()
        img_down.set_from_stock(gtk.STOCK_CANCEL, 2)
        down_item.set_image(img_down)
        down_item.set_always_show_image(True)

        # Quit item
        img_quit = gtk.Image()
        img_quit.set_from_stock(gtk.STOCK_CLOSE, 2)
        item_quit.connect('activate', self.quit_app)
        item_quit.set_image(img_quit)
        item_quit.set_always_show_image(True)

        up_item.connect("activate", self.open_url)
        down_item.connect("activate", self.open_url)

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
        data = ad.get_host_state(self.backend)

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
        # Launch the app
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.main()

