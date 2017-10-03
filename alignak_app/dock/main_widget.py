#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2017:
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
    TODO
"""

import sys

from alignak_app.core.utils import init_config, get_image_path
from alignak_app.core.data_manager import data_manager
from alignak_app.core.backend import app_backend
from alignak_app.threads.thread_manager import thread_manager
from alignak_app.dock.buttons_widget import ButtonsQWidget
from alignak_app.dock.status_widget import DockStatusQWidget
from alignak_app.widgets.app_widget import AppQWidget
from alignak_app.widgets.host_widget import HostQWidget
from alignak_app.dock.backend_widget import BackendQWidget

from PyQt5.Qt import QApplication, QWidget, QGridLayout, QLabel  # pylint: disable=no-name-in-module
from PyQt5.Qt import QFrame, QVBoxLayout, Qt, QAbstractItemView  # pylint: disable=no-name-in-module
from PyQt5.Qt import QSize, QListWidget, QIcon, QListWidgetItem  # pylint: disable=no-name-in-module


class NotificationItem(QListWidgetItem):
    """
        TODO
    """

    def initialize(self, state, msg):
        """
        TODO
        :return:
        """

        self.setText("Host is %s: %s" % (state, msg))
        self.setIcon(QIcon(get_image_path(self.get_icon(state))))

        self.setSizeHint(QSize(self.sizeHint().width(), 35))

    @staticmethod
    def get_icon(state):
        """

        :param state:
        :return:
        """

        states = {
            'UP': 'hosts_up',
            'DOWN': 'hosts_down',
            'UNREACHABLE': 'hosts_unreachable',
        }

        return states[state]


class AppQMain(QWidget):
    """
        TODO
    """

    def __init__(self, parent=None):
        super(AppQMain, self).__init__(parent)
        self.app_widget = AppQWidget()
        self.events_widget_list = QListWidget()
        self.spy_widgetlist = QListWidget()
        self.host_widget = None
        self.resume_status_widget = DockStatusQWidget()
        self.buttons_widget = ButtonsQWidget()
        self.backend_widget = BackendQWidget()

    def initialize(self):
        """
        TODO
        :return:
        """

        layout = QGridLayout()
        self.setLayout(layout)

        self.resume_status_widget.initialize()
        layout.addWidget(self.resume_status_widget)
        layout.addWidget(self.get_frame_separator())

        self.buttons_widget.initialize()
        layout.addWidget(self.buttons_widget)
        layout.addWidget(self.get_frame_separator())

        self.backend_widget.initialize()
        layout.addWidget(self.backend_widget)
        layout.addWidget(self.get_frame_separator())

        layout.addWidget(self.get_events_list_widget())

        layout.addWidget(self.get_spy_list_widget())

        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        desktop = QApplication.desktop().screenGeometry(screen)

        pos_size = self.get_position_and_size(desktop)

        self.app_widget.initialize('')
        self.app_widget.add_widget(self)
        self.app_widget.resize(pos_size['size'][0], pos_size['size'][1])
        self.app_widget.move(pos_size['pos'][0], pos_size['pos'][1])

    def get_events_list_widget(self):
        """
        TODO
        :return:
        """

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        event_title = QLabel("Last events...")
        layout.addWidget(event_title)
        layout.setAlignment(event_title, Qt.AlignCenter)

        self.events_widget_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.events_widget_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.events_widget_list.setAcceptDrops(True)
        self.events_widget_list.setSortingEnabled(True)
        self.events_widget_list.doubleClicked.connect(self.item_menu)
        self.events_widget_list.setWordWrap(True)
        layout.addWidget(self.events_widget_list)

        return widget

    def get_spy_list_widget(self):
        """
        TODO
        :return:
        """

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        event_title = QLabel("Spied hosts... Coming soon !")
        layout.addWidget(event_title)
        layout.setAlignment(event_title, Qt.AlignCenter)

        self.spy_widgetlist.setDragDropMode(QAbstractItemView.InternalMove)
        self.spy_widgetlist.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.spy_widgetlist.setAcceptDrops(True)
        self.spy_widgetlist.setSortingEnabled(True)
        self.spy_widgetlist.doubleClicked.connect(self.item_menu)
        self.spy_widgetlist.setWordWrap(True)
        layout.addWidget(self.spy_widgetlist)

        return widget

    def item_menu(self):
        """
        TODO
        :param pos:
        :return:
        """

        self.events_widget_list.takeItem(self.events_widget_list.currentRow())

    @staticmethod
    def get_frame_separator():
        """
        TODO
        :return:
        """

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #607d8b; color: #607d8b;")

        return line

    def show_host_view(self):
        """
        TODO
        :return:
        """

        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        desktop = QApplication.desktop().availableGeometry(screen)

        self.host_widget = HostQWidget()
        self.host_widget.initialize()

        x_size = desktop.width() - self.width()
        y_size = 64

        pos_x = 0
        pos_y = 0

        self.host_widget.resize(x_size, y_size)
        self.host_widget.move(pos_x, pos_y)
        self.host_widget.show()

    def get_position_and_size(self, desktop):
        """
        TODO
        :return:
        """

        x_size = desktop.width() * 0.2
        y_size = desktop.height()

        pos_x = desktop.width() - self.width() * 0.5
        pos_y = desktop.height() - self.height() * 0.5

        return {
            'size': [x_size, y_size],
            'pos': [pos_x, pos_y]
        }


if __name__ == '__main__':
    app = QApplication(sys.argv)

    init_config()
    app_backend.login()
    thread_manager.start()
    while not data_manager.is_ready():
        continue

    m = AppQMain()
    m.initialize()

    notifications = {
        "UP": "Host is UP since 2017-09-22 17:58:36",
        "DOWN": "Host is DOWN since 2017-09-22 17:58:36, please fix the problem",
        "UNREACHABLE": "never seen",
    }

    for key, value in notifications.items():
        notif = NotificationItem()
        notif.initialize(key, value)
        m.events_widget_list.addItem(notif)

    m.app_widget.show()
    sys.exit(app.exec_())
