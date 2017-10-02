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
import datetime

from alignak_app.core.utils import init_config, get_image_path
from alignak_app.widgets.app_widget import AppQWidget

from PyQt5.Qt import QApplication, QWidget, QGridLayout  # pylint: disable=no-name-in-module
from PyQt5.Qt import QLabel, QPushButton, QAbstractItemView  # pylint: disable=no-name-in-module
from PyQt5.Qt import QListWidget, QIcon, QListWidgetItem, QMenu  # pylint: disable=no-name-in-module


init_config()


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
        self.host_widget = None
        self.notif_widget_list = None
        self.listMenu = QMenu()

    def initialize(self):
        """
        TODO
        :return:
        """

        layout = QGridLayout()
        self.setLayout(layout)

        buttons_widget = self.get_buttons_widget()
        layout.addWidget(buttons_widget)

        notif_button = QPushButton("Show messages")
        notif_button.clicked.connect(self.add_message)
        layout.addWidget(notif_button)

        self.notif_widget_list = QListWidget()
        self.notif_widget_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.notif_widget_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # self.notif_widget_list.setDragEnabled(True)
        self.notif_widget_list.setAcceptDrops(True)
        # self.notif_widget_list.setSortingEnabled(True)

        self.notif_widget_list.clicked.connect(self.item_menu)
        layout.addWidget(self.notif_widget_list)

        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        desktop = QApplication.desktop().screenGeometry(screen)

        pos_size = self.get_position_and_size(desktop)

        self.app_widget.initialize('Alignak-App')
        self.app_widget.add_widget(self)
        self.app_widget.resize(pos_size['size'][0], pos_size['size'][1])
        self.app_widget.move(pos_size['pos'][0], pos_size['pos'][1])

    def item_menu(self):
        """
        TODO
        :param pos:
        :return:
        """
        print('Item moved')

    def get_buttons_widget(self):
        """
        TODO
        :return:
        """

        buttons_widget = QWidget()
        layout = QGridLayout()
        buttons_widget.setLayout(layout)

        status_label = QLabel('Alignak status')
        layout.addWidget(status_label, 0, 0, 1, 3)

        status = QLabel('<span style="color:#27ae60;">online</span>')
        layout.addWidget(status, 0, 3, 1, 2)

        dashboard_btn = QPushButton()
        dashboard_btn.setIcon(QIcon(get_image_path('dashboard')))
        layout.addWidget(dashboard_btn, 1, 0, 1, 1)

        host_btn = QPushButton()
        host_btn.setIcon(QIcon(get_image_path('host')))
        layout.addWidget(host_btn, 1, 1, 1, 1)

        services_btn = QPushButton()
        services_btn.setIcon(QIcon(get_image_path('service')))
        layout.addWidget(services_btn, 1, 2, 1, 1)

        status_btn = QPushButton()
        status_btn.setIcon(QIcon(get_image_path('icon')))
        layout.addWidget(status_btn, 1, 3, 1, 1)

        profile_btn = QPushButton()
        profile_btn.setIcon(QIcon(get_image_path('user')))
        layout.addWidget(profile_btn, 1, 4, 1, 1)

        return buttons_widget

    def add_message(self):
        """
        TODO
        :return:
        """

        self.notif_widget_list.appendPlainText("Message at %s " % datetime.datetime.now())

    def show_host_view(self):
        """

        :return:
        """

        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        desktop = QApplication.desktop().availableGeometry(screen)

        self.host_widget = QWidget()
        layout = QGridLayout()
        self.host_widget.setLayout(layout)

        label = QLabel("Host View")
        layout.addWidget(label)

        x_size = desktop.width() - self.width()
        y_size = desktop.height()

        pos_x = 0
        pos_y = 0

        self.host_widget.resize(x_size, y_size)
        self.host_widget.move(pos_x, pos_y)
        self.host_widget.show()
        print(self.size())

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
    m = AppQMain()
    m.initialize()

    notifications = {
        "UP": "everything is fine",
        "DOWN": "nothing goes",
        "UNREACHABLE": "never seen",
    }

    for key, value in notifications.items():
        notif = NotificationItem()
        notif.initialize(key, value)
        m.notif_widget_list.addItem(notif)

    m.app_widget.show()
    sys.exit(app.exec_())
