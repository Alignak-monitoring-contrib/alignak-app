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

from PyQt5.Qt import QApplication, QWidget, QGridLayout  # pylint: disable=no-name-in-module
from PyQt5.Qt import QFrame, QSize  # pylint: disable=no-name-in-module
from PyQt5.Qt import QLabel, QPushButton, QAbstractItemView  # pylint: disable=no-name-in-module
from PyQt5.Qt import QListWidget, QIcon, QListWidgetItem  # pylint: disable=no-name-in-module
from PyQt5.Qt import QPixmap, QVBoxLayout, QHBoxLayout, Qt  # pylint: disable=no-name-in-module

from alignak_app.core.utils import init_config, get_image_path
from alignak_app.dock.buttons_widget import ButtonsQWidget
from alignak_app.dock.dock_status_widget import DockStatusQWidget
from alignak_app.widgets.app_widget import AppQWidget
from alignak_app.widgets.host_widget import HostQWidget

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

        layout.addWidget(self.get_backend_resume_widget())

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

    @staticmethod
    def get_status_resume():
        """
        TODO
        :return:
        """

        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)

        status_label = QLabel('Alignak status:')
        layout.addWidget(status_label)

        status = QLabel('<span style="color:#27ae60;">online</span>')
        layout.addWidget(status)

        status_btn = QPushButton()
        status_btn.setIcon(QIcon(get_image_path('icon')))
        status_btn.setFixedSize(32, 32)
        layout.addWidget(status_btn)

        status_label = QLabel('Backend:')
        layout.addWidget(status_label)

        status = QLabel('<span style="color:#27ae60;">connected</span>')
        layout.addWidget(status)

        return widget

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

    def get_backend_resume_widget(self):
        """
        TODO
        :return:
        """

        resume_widget = QWidget()
        layout = QHBoxLayout()
        resume_widget.setLayout(layout)

        host_widget = self.get_resume_item_widget(3, 'host', 37)
        layout.addWidget(host_widget)

        service_widget = self.get_resume_item_widget(36, 'service', 416)
        layout.addWidget(service_widget)

        problem_widget = self.get_resume_item_widget(39, 'problem', 453)
        layout.addWidget(problem_widget)

        return resume_widget

    @staticmethod
    def get_resume_item_widget(problem_nb, item_type, item_nb):
        """
        TODO
        :param problem_nb:
        :param item_type:
        :param item_nb:
        :return:
        """

        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)

        problem_label = QLabel('<span style="color: red;">%d</span>' % problem_nb)
        layout.addWidget(problem_label)
        layout.setAlignment(problem_label, Qt.AlignCenter)

        item_label = QLabel()
        item_label.setPixmap(QPixmap(get_image_path(item_type)))
        layout.addWidget(item_label)
        layout.setAlignment(item_label, Qt.AlignCenter)

        item_nb_label = QLabel(
            '<span style="background: #ccc; color: #607d8b;">%d</span>' % item_nb
        )
        layout.addWidget(item_nb_label)
        layout.setAlignment(item_nb_label, Qt.AlignCenter)

        return widget

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
