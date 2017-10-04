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
    Dock manage creation of Alignak-app Dock
"""

import sys
import time

from alignak_app.core.utils import init_config, get_css, get_image_path
from alignak_app.core.data_manager import data_manager
from alignak_app.core.backend import app_backend
from alignak_app.threads.thread_manager import thread_manager
from alignak_app.dock.buttons_widget import ButtonsQWidget
from alignak_app.dock.status_widget import DockStatusQWidget
from alignak_app.dock.backend_widget import BackendQWidget
from alignak_app.dock.events_widget import EventsQListWidget
from alignak_app.dock.spy_widget import SpyQListWidget
from alignak_app.widgets.app_widget import AppQWidget
from alignak_app.widgets.host_widget import HostQWidget

from PyQt5.Qt import QApplication, QWidget, QGridLayout, QFrame, Qt  # pylint: disable=no-name-in-module
from PyQt5.Qt import QListWidget, QSplashScreen, QPixmap, QProgressBar  # pylint: disable=no-name-in-module


class DockQWidget(QWidget):
    """
        Class who create QWidgets for dock
    """

    def __init__(self, parent=None):
        super(DockQWidget, self).__init__(parent)
        self.setStyleSheet(get_css())
        # Fields
        self.app_widget = AppQWidget()
        self.events_widget_list = QListWidget()
        self.spy_widgetlist = QListWidget()
        self.host_widget = None
        self.resume_status_widget = DockStatusQWidget()
        self.buttons_widget = ButtonsQWidget()
        self.backend_widget = BackendQWidget()
        self.events_widget = EventsQListWidget()
        self.spy_widget = SpyQListWidget()

    def initialize(self):
        """
        Iniitalize dock QWidget

        """

        layout = QGridLayout()
        self.setLayout(layout)

        # Add dock widgets
        self.resume_status_widget.initialize()
        layout.addWidget(self.resume_status_widget)
        layout.addWidget(self.get_frame_separator())

        self.buttons_widget.initialize()
        layout.addWidget(self.buttons_widget)
        layout.addWidget(self.get_frame_separator())

        self.backend_widget.initialize()
        layout.addWidget(self.backend_widget)
        layout.addWidget(self.get_frame_separator())

        self.events_widget.initialize()
        layout.addWidget(self.events_widget)

        self.spy_widget.initialize()
        layout.addWidget(self.spy_widget)

        # Define size and position of dock
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        desktop = QApplication.desktop().screenGeometry(screen)

        pos_size = self.get_position_and_size(desktop)

        self.app_widget.initialize('')
        self.app_widget.add_widget(self)
        self.app_widget.resize(pos_size['size'][0], pos_size['size'][1])
        self.app_widget.move(pos_size['pos'][0], pos_size['pos'][1])

    @staticmethod
    def get_frame_separator():
        """
        Return a frame separator

        :return: frame separator
        :rtype: QFrame
        """

        line = QFrame()
        line.setObjectName('separator')
        line.setFrameShape(QFrame.HLine)

        return line

    def show_host_view(self):
        """
        TODO: Show the host view, should be temp here

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
        Return position and size of dock to "stick" on right side

        :return: size and postion
        :rtype: dict
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

    splash_icon = QPixmap(get_image_path('alignak'))
    splash = QSplashScreen(splash_icon)

    progressBar = QProgressBar(splash)
    progressBar.setTextVisible(False)
    progressBar.setStyleSheet('border-top: none; color: none;')
    progressBar.setFixedSize(splash_icon.width(), splash_icon.height())
    progressBar.setAlignment(Qt.AlignCenter)

    splash.setMask(splash_icon.mask())
    splash.show()

    while not data_manager.is_ready():
        for i in range(0, 100):
            progressBar.setValue(i)
            t = time.time()
            while time.time() < t + 0.02:
                app.processEvents()

    dock = DockQWidget()
    splash.finish(dock)
    dock.initialize()

    dock.app_widget.show()
    sys.exit(app.exec_())
