import sys
from PyQt5.QtWidgets import QSystemTrayIcon
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon


class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QMenu(parent)
        host_action = QAction(QIcon('../etc/images/host_up.svg'), 'Host UP', self)
        exit_action = QAction(QIcon('../etc/images/error.svg'), 'Quit', self)
        exit_action.triggered.connect(self.quit_fun)
        self.menu.addAction(host_action)
        self.menu.addAction(exit_action)
        self.setContextMenu(self.menu)

    @staticmethod
    def quit_fun():
        sys.exit(0)


class AlignakApp(object):

    def __init__(self):
        self.app = None

    def main(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        icon = QIcon('../etc/images/alignak.svg')
        tray_icon = SystemTrayIcon(icon)

        tray_icon.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    AlignakApp().main()
