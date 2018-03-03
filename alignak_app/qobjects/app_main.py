#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2018:
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
    App Main
    ++++++++
    App Main manage creation of QMainWindow for:

    * :class:`Dock <alignak_app.qobjects.dock.dock.DockQWidget>` (Right part)
    * :class:`Panel <alignak_app.qobjects.panel.panel.PanelQWidget>` (Left part)
"""

from logging import getLogger

from PyQt5.Qt import QMainWindow, QWidget, QGridLayout, QIcon, Qt

from alignak_app.utils.config import settings

from alignak_app.qobjects.common.widgets import get_logo_widget, center_widget
from alignak_app.qobjects.common.frames import get_frame_separator
from alignak_app.qobjects.dock.dock import DockQWidget
from alignak_app.qobjects.panel.panel import PanelQWidget

logger = getLogger(__name__)


class AppQMainWindow(QMainWindow):
    """
        Class who create QMainWindow of Alignak-app
    """

    def __init__(self, parent=None):
        super(AppQMainWindow, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(settings.css_style)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        self.dock = DockQWidget()
        self.panel_widget = PanelQWidget()
        self.offset = None

    def initialize(self):
        """
        Initialize QMainWindow for App

        """

        logger.info('Display Alignak-App...')

        app_widget = QWidget()
        app_widget.setObjectName('dialog')
        app_layout = QGridLayout()
        app_layout.setContentsMargins(0, 0, 0, 0)
        app_widget.setLayout(app_layout)

        self.dock.initialize()
        self.dock.setFixedWidth(330)
        self.panel_widget.initialize(self.dock.spy_widget)

        app_layout.addWidget(get_logo_widget(self, 'Alignak-App'), 0, 0, 1, 3)
        app_layout.addWidget(self.panel_widget, 1, 0, 1, 1)
        app_layout.addWidget(get_frame_separator(True), 1, 1, 1, 1)
        app_layout.addWidget(self.dock, 1, 2, 1, 1)

        self.connect_dock_buttons()

        self.setCentralWidget(app_widget)
        self.setMinimumSize(1440, 900)
        center_widget(self)

        display = settings.get_config('Alignak-app', 'display')
        if "min" in display:
            self.show()
        elif "max" in display:
            self.showMaximized()
        else:
            pass

    def connect_dock_buttons(self):
        """
        Connect dock QWidget buttons to host and problems tab

        """

        self.dock.buttons_widget.host_btn.clicked.connect(self.open_host_widget)
        self.dock.buttons_widget.problems_btn.clicked.connect(self.open_problems_widget)

    def open_host_widget(self):
        """
        Show HostQWidget

        """

        self.panel_widget.show()
        self.panel_widget.tab_widget.setCurrentIndex(0)

    def open_problems_widget(self):
        """
        Show ProblemsQWidget

        """

        self.panel_widget.show()
        self.panel_widget.tab_widget.setCurrentIndex(1)

    def mousePressEvent(self, event):  # pragma: no cover - not testable
        """ QWidget.mousePressEvent(QMouseEvent) """

        self.offset = event.pos()

    def mouseMoveEvent(self, event):  # pragma: no cover - not testable
        """ QWidget.mousePressEvent(QMouseEvent) """

        try:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)
        except AttributeError as e:
            logger.warning('Move Event %s: %s', self.objectName(), str(e))
