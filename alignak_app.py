import signal, os, webbrowser, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator
gi.require_version('Notify', '0.7')
from gi.repository import Notify as notify
from gi.repository import GLib as glib
import configparser as cfg

import alignakdata as ad

# TODO : make a class
# TODO : add services to app

# Read config
Config = cfg.ConfigParser()
Config.read('etc/settings.cfg')

# General Variables
img = os.path.abspath('images/' + Config.get('Alignak-App', 'icon'))
backend = ad.login_backend(Config)

# Up and Down Items
up_item = gtk.ImageMenuItem('')
down_item = gtk.ImageMenuItem('')

def main():
    # Set Indicator
    app = set_indicator()

    # Update Menu
    update_menu()

    # Main Gtk
    gtk.main()

def open_url(source):
    # Function to make link on Items
    webui_url = Config.get('Webui', 'webui_url')
    webbrowser.open(webui_url + '/hosts')

def build_menu_item():
    # Decorate items
    img_up = gtk.Image()
    img_up.set_from_stock(gtk.STOCK_YES, 2)
    up_item.set_image(img_up)
    up_item.set_always_show_image(True)

    img_down = gtk.Image()
    img_down.set_from_stock(gtk.STOCK_CANCEL, 2)
    down_item.set_image(img_down)
    down_item.set_always_show_image(True)

    # Create Quit item
    item_quit = gtk.ImageMenuItem('Quit')
    img_quit = gtk.Image()
    img_quit.set_from_stock(gtk.STOCK_CLOSE, 2)
    item_quit.connect('activate', quit_app)
    item_quit.set_image(img_quit)
    item_quit.set_always_show_image(True)

    up_item.connect("activate", open_url)
    down_item.connect("activate", open_url)

    return up_item, down_item, item_quit


def build_menu():
    # Get first states
    UP, DOWN = get_state()
    update_hosts_menu(UP, DOWN)

    # Create Menu with Items
    menu = gtk.Menu()
    up_item, down_item, item_quit = build_menu_item()

    menu.append(up_item)
    menu.append(down_item)
    menu.append(item_quit)
    menu.show_all()

    return menu

def set_indicator():
    # Define ID
    APPINDICATOR_ID = 'appalignak'

    # TODO : change icon if hosts are down
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, img, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

    # Create Menu
    indicator.set_menu(build_menu())

    # Init notify
    notify.init(APPINDICATOR_ID)
    return indicator

def update_menu():
    check_interval = int(Config.get('Alignak-App', 'check_interval'))
    glib.timeout_add_seconds(check_interval, notify_change)

def get_state():
    UP = 0
    DOWN = 0
    data = ad.get_host_state(backend)

    for key, v in data.items():
        if 'UP' in v:
            UP += 1
        if 'DOWN' in v:
            DOWN += 1
    return UP, DOWN

def notify_change():
    UP, DOWN = get_state()
    if DOWN > 0:
        message = "ALERT : Hosts are DOWN !"
    else:
        message = "All is OK :)"
    # TODO : let notifications optional with configuration.
    notify.Notification.new(str(message), update_hosts_menu(UP, DOWN), None).show()
    return True

def update_hosts_menu(UP, DOWN):
    if UP > 0:
        str_UP = 'Hosts UP (' + str(UP) + ')'
        up_item.set_label(str_UP)

    if DOWN > 0:
        str_NOK = 'Hosts DOWN (' + str(DOWN) + ')'
        down_item.set_label(str_NOK)

def quit_app(source):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()

