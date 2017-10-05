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

from alignak_app.core.utils import get_css, get_image_path

from alignak_app.dock.buttons_widget import ButtonsQWidget
from alignak_app.dock.status_widget import DockStatusQWidget
from alignak_app.dock.backend_widget import BackendQWidget
from alignak_app.dock.events_widget import events_widget
from alignak_app.dock.spy_widget import SpyQListWidget

from alignak_app.widgets.app_widget import AppQWidget

from PyQt5.Qt import QApplication, QWidget, QGridLayout, QIcon  # pylint: disable=no-name-in-module
from PyQt5.Qt import QListWidget, QFrame  # pylint: disable=no-name-in-module


class DockQWidget(QWidget):
    """
        Class who create QWidgets for dock
    """

    def __init__(self, parent=None):
        super(DockQWidget, self).__init__(parent)
        self.setStyleSheet(get_css())
        self.setWindowIcon(QIcon(get_image_path('icon')))
        # Fields
        self.app_widget = AppQWidget()
        self.status_widget = DockStatusQWidget()
        self.buttons_widget = ButtonsQWidget()
        self.backend_widget = BackendQWidget()
        self.spy_widgetlist = QListWidget()
        self.spy_widget = SpyQListWidget()

    def initialize(self):
        """
        Initialize dock QWidget

        """

        layout = QGridLayout()
        self.setLayout(layout)

        # Define size and position of dock
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        desktop = QApplication.desktop().availableGeometry(screen)

        pos_size = self.get_position_and_size(desktop)

        self.app_widget.initialize('')
        self.app_widget.add_widget(self)
        self.app_widget.resize(pos_size['size'][0], pos_size['size'][1])
        self.app_widget.move(pos_size['pos'][0], pos_size['pos'][1])

        # Add dock widgets
        self.status_widget.initialize()
        layout.addWidget(self.status_widget)
        layout.addWidget(self.get_frame_separator())

        self.buttons_widget.initialize()
        layout.addWidget(self.buttons_widget)
        layout.addWidget(self.get_frame_separator())

        self.backend_widget.initialize()
        layout.addWidget(self.backend_widget)
        layout.addWidget(self.get_frame_separator())

        # self.events_widget.initialize()
        layout.addWidget(events_widget)

        self.spy_widget.initialize()
        layout.addWidget(self.spy_widget)

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


# Initialize dock var to None
dock = DockQWidget()
