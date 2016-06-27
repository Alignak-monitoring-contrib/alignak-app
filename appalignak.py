import signal, os, webbrowser, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator
gi.require_version('Notify', '0.7')
from gi.repository import Notify as notify
import alignak_data as ad

# Alignak Variables
APPINDICATOR_ID = 'appalignak'
img = os.path.abspath('images/alignak.png')
auth = ad.alignak_backend_auth()
url = 'http://94.76.229.155:91'
# Gtk Object
menu = gtk.Menu()
up_item = gtk.MenuItem('')
down_item = gtk.MenuItem('')
menu.append(up_item)
menu.append(down_item)

def main():
    app = set_indicator()
    gtk.main()

def build_menu():
    # Add menu for hosts
    build_hosts_menu()

    # Add menu for Refresh
    build_check_menu()

    # Add menu for Quit
    build_menu_quit()

    menu.show_all()
    return menu

def set_indicator():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, img, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    return indicator

def build_hosts_menu():
    UP, DOWN = check()
    if UP > 0:
        str_UP = 'Hosts UP (' + str(UP) + ')'
        up_item.set_label(str_UP)
        # menu.append(up_item)
    if DOWN > 0:
        str_NOK = 'Hosts DOWN (' + str(DOWN) + ')'
        down_item.set_label(str_NOK)
        # menu.append(down_item)

def update_menu(source):
    notify.Notification.new("<b>Update Alignak Data..</b>", build_hosts_menu(), None).show()

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

def build_check_menu():
    check_item = gtk.MenuItem('Check')
    check_item.connect('activate', update_menu)
    menu.append(check_item)

def build_menu_quit():
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit_app)
    menu.append(item_quit)

def open_url(source):
    webbrowser.open(url + '/hosts')

up_item.connect("activate", open_url)
down_item.connect("activate", open_url)

def print_hello():
    print('hello world')

def quit_app(source):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()

