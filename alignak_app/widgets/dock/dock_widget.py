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

from PyQt5.Qt import QApplication, QWidget, QGridLayout, QIcon  # pylint: disable=no-name-in-module
from PyQt5.Qt import QListWidget, QLabel, Qt  # pylint: disable=no-name-in-module

from alignak_app.core.utils import get_css, get_image_path
from alignak_app.frames.app_frame import AppQFrame, get_frame_separator
from alignak_app.widgets.dock.buttons_widget import ButtonsQWidget
from alignak_app.widgets.dock.status_widget import DockStatusQWidget
from alignak_app.widgets.dock.livestate_widget import LivestateQWidget
from alignak_app.widgets.dock.spy_widget import SpyQListWidget
from alignak_app.widgets.dock.events_widget import events_widget


class DockQWidget(QWidget):
    """
        Class who create QWidgets for dock
    """

    def __init__(self, parent=None):
        super(DockQWidget, self).__init__(parent)
        self.setStyleSheet(get_css())
        self.setWindowIcon(QIcon(get_image_path('icon')))
        # Fields
        self.app_widget = AppQFrame()
        self.status_widget = DockStatusQWidget()
        self.buttons_widget = ButtonsQWidget()
        self.livestate_widget = LivestateQWidget()
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

        # Add Alignak status
        status = QLabel(_('Alignak'))
        status.setObjectName('title')
        layout.addWidget(status)
        layout.setAlignment(status, Qt.AlignCenter)
        layout.addWidget(get_frame_separator())
        self.status_widget.initialize()
        layout.addWidget(self.status_widget)
        self.buttons_widget.initialize()
        layout.addWidget(self.buttons_widget)

        # Livestate
        livestate = QLabel(_('Livestate'))
        livestate.setObjectName('title')
        layout.addWidget(livestate)
        layout.setAlignment(livestate, Qt.AlignCenter)
        layout.addWidget(get_frame_separator())
        self.livestate_widget.initialize()
        layout.addWidget(self.livestate_widget)

        # Last Events
        last_event_label = QLabel(_('Last Events'))
        last_event_label.setObjectName('title')
        layout.addWidget(last_event_label)
        layout.setAlignment(last_event_label, Qt.AlignCenter)
        layout.addWidget(get_frame_separator())
        layout.addWidget(events_widget)

        self.spy_widget.initialize()
        layout.addWidget(self.spy_widget)

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

    def show_dock(self):
        """
        Show the dock by making AppQWidget window active

        """

        self.app_widget.show()
        QWidget.activateWindow(self.app_widget)
