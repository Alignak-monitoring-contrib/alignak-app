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
    App Main manage creation of Alignak-app Dock QMainWindow
"""

from logging import getLogger

from PyQt5.Qt import QMainWindow, QWidget, QGridLayout, QIcon, Qt

from alignak_app.core.utils.config import app_css, get_image

from alignak_app.pyqt.common.widgets import get_logo_widget, center_widget
from alignak_app.pyqt.dock.widgets.dock import DockQWidget
from alignak_app.pyqt.panel.widgets.panel import PanelQWidget

logger = getLogger(__name__)


class AppMain(QMainWindow):
    """
        Class who create QMainWindow of Alignak-app
    """

    def __init__(self, parent=None):
        super(AppMain, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(app_css)
        self.setWindowIcon(QIcon(get_image('icon')))
        self.dock = DockQWidget()
        self.panel_widget = PanelQWidget()
        self.offset = None

    def initialize(self):
        """
        Initialize QMainWindow for App

        """

        app_widget = QWidget()
        app_layout = QGridLayout()
        app_layout.setContentsMargins(0, 0, 0, 0)
        app_widget.setLayout(app_layout)

        self.dock.initialize()
        self.dock.setFixedWidth(330)
        self.panel_widget.initialize(self.dock.spy_widget)

        app_layout.addWidget(get_logo_widget(self, 'Alignak-App'), 0, 0, 1, 2)
        app_layout.addWidget(self.panel_widget, 1, 0, 1, 1)
        app_layout.addWidget(self.dock, 1, 1, 1, 1)

        self.connect_dock_buttons()

        self.setCentralWidget(app_widget)
        self.setMinimumSize(1300, 800)
        center_widget(self)

        self.show()

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
