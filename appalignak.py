import signal, os, webbrowser, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator
gi.require_version('Notify', '0.7')
from gi.repository import Notify as notify
from gi.repository import GLib as glib

import alignak_data as ad

# Alignak Variables
APPINDICATOR_ID = 'appalignak'
img = os.path.abspath('images/alignak.png')
auth = ad.alignak_backend_auth()
webui_url = 'http://94.76.229.155:91'
check_interval = 30

# Gtk Objects
menu = gtk.Menu()

img_up = gtk.Image()
img_up.set_from_stock(gtk.STOCK_YES, 2)
up_item = gtk.ImageMenuItem('')
up_item.set_image(img_up)
up_item.set_always_show_image(True)

img_down = gtk.Image()
img_down.set_from_stock(gtk.STOCK_CANCEL, 2)
down_item = gtk.ImageMenuItem('')
down_item.set_image(img_down)
down_item.set_always_show_image(True)

menu.append(up_item)
menu.append(down_item)

def main():
    app = set_indicator()

    # Start Process
    update_menu()

    gtk.main()

def build_menu():
    # Add menu for hosts
    UP, DOWN = check()
    update_hosts_menu(UP, DOWN)

    # Add menu for Quit
    build_menu_quit()

    menu.show_all()
    return menu

def open_url(source):
    webbrowser.open(webui_url + '/hosts')

up_item.connect("activate", open_url)
down_item.connect("activate", open_url)

def set_indicator():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, img, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    return indicator

def update_menu():
    glib.timeout_add_seconds(check_interval, notify_change)

def notify_change():
    UP, DOWN = check()
    if DOWN > 0:
        message = "ALERT : Hosts are DOWN !"
    else:
        message = "All is OK :)"
    notify.Notification.new(str(message), update_hosts_menu(UP, DOWN), None).show()
    return True

def update_hosts_menu(UP,DOWN):
    if UP > 0:
        str_UP = 'Hosts UP (' + str(UP) + ')'
        up_item.set_label(str_UP)

    if DOWN > 0:
        str_NOK = 'Hosts DOWN (' + str(DOWN) + ')'
        down_item.set_label(str_NOK)

def check():
    UP = 0
    DOWN = 0
    data = ad.get_host_state(auth)

    for key, v in data.items():
        if 'UP' in v:
            UP += 1
        if 'DOWN' in v:
            DOWN += 1
    return UP, DOWN

def build_menu_quit():
    item_quit = gtk.ImageMenuItem('Quit')
    img_quit = gtk.Image()
    img_quit.set_from_stock(gtk.STOCK_CLOSE, 2)
    item_quit.connect('activate', quit_app)
    item_quit.set_image(img_quit)
    item_quit.set_always_show_image(True)
    menu.append(item_quit)

def quit_app(source):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()

