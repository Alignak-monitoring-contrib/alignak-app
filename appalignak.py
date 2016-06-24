import signal, os
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator


APPINDICATOR_ID = 'appalignak'
img = os.path.abspath('images/alignak.png')

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, img, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit_app)
    menu.append(item_quit)
    menu.show_all()
    return menu

def quit_app(source):
    gtk.main_quit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()

