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
    App Widget manage creation of a QWidget to make a tempalte for all QWidgets of Alignak-app
"""


from logging import getLogger
from alignak_app.core.utils import get_image_path, get_app_config, get_css

from PyQt5.QtWidgets import QApplication  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget, QVBoxLayout  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QLabel  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QHBoxLayout, QPushButton  # pylint: disable=no-name-in-module
from PyQt5.Qt import Qt, QIcon, QPixmap, QFrame  # pylint: disable=no-name-in-module


logger = getLogger(__name__)


class AppQWidget(QFrame):
    """
        Class who create a QWidget template.
    """

    def __init__(self, parent=None):
        super(AppQWidget, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(get_image_path('icon')))
        self.setStyleSheet(get_css())
        self.offset = None

    def initialize(self, title):
        """
        Initialize the QWidget, with its "title"

        :param title: title of the QWidget
        :type title: str
        """

        self.setWindowTitle(title)
        self.setObjectName('app_widget')

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        main_layout.addWidget(self.get_logo_widget(title))

        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def get_logo_widget(self, title):
        """
        Return the logo QWidget

        :return: logo QWidget
        :rtype: QWidget
        """

        logo_widget = QWidget()
        logo_widget.setFixedHeight(45)
        logo_widget.setObjectName('logo')
        logo_layout = QHBoxLayout()
        logo_widget.setLayout(logo_layout)

        logo_label = QLabel()
        logo_label.setPixmap(QPixmap(get_image_path('alignak')))
        logo_label.setFixedSize(121, 35)
        logo_label.setScaledContents(True)

        logo_layout.addWidget(logo_label, 0)

        title_label = QLabel('<h3>%s</h3>' % title)
        title_label.setObjectName('title')
        title_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        logo_layout.addWidget(title_label, 1)
        logo_layout.setAlignment(title_label, Qt.AlignHCenter)

        minimize_btn = QPushButton()
        minimize_btn.setIcon(QIcon(get_image_path('minimize')))
        minimize_btn.setFixedSize(22, 22)
        minimize_btn.setObjectName('app_widget')
        minimize_btn.clicked.connect(self.minimize)
        logo_layout.addWidget(minimize_btn, 2)

        maximize_btn = QPushButton()
        maximize_btn.setIcon(QIcon(get_image_path('maximize')))
        maximize_btn.setFixedSize(22, 22)
        maximize_btn.setObjectName('app_widget')
        maximize_btn.clicked.connect(self.minimize_maximize)
        logo_layout.addWidget(maximize_btn, 3)

        close_btn = QPushButton()
        close_btn.setIcon(QIcon(get_image_path('exit')))
        close_btn.setFixedSize(22, 22)
        close_btn.setObjectName('app_widget')
        close_btn.clicked.connect(self.close)
        logo_layout.addWidget(close_btn, 4)

        return logo_widget

    def minimize(self):
        """
        Minimize QWidget

        """

        if self.windowState() == Qt.WindowMinimized:
            self.setWindowState(Qt.WindowNoState)
        else:
            self.setWindowState(Qt.WindowMinimized)

    def minimize_maximize(self):
        """
        Minimize / Maximize QWidget

        """

        if self.windowState() == Qt.WindowMaximized:
            self.setWindowState(Qt.WindowNoState)
        else:
            self.setWindowState(Qt.WindowMaximized)

    def center(self):
        """
        Center QWidget

        """

        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center = QApplication.desktop().screenGeometry(screen).center()
        self.move(center.x() - (self.width() / 2), center.y() - (self.height() / 2))

    def show_widget(self):
        """
        Show and center AppQWidget

        """

        self.center()
        self.show()
        QWidget.activateWindow(self)

    def add_widget(self, widget):
        """
        Add the main QWidget of AppQWidget

        :param widget: QWidget to add
        :type widget: QWidget
        """

        self.layout().addWidget(widget, 2)

    def mousePressEvent(self, event):
        """ QWidget.mousePressEvent(QMouseEvent) """

        sticky = False

        if 'Dashboard' in self.windowTitle():
            sticky = bool(get_app_config('Dashboard', 'sticky', boolean=True))

        if not sticky:
            self.offset = event.pos()
        else:
            pass

    def mouseMoveEvent(self, event):
        """ QWidget.mousePressEvent(QMouseEvent) """

        sticky = False

        if 'Dashboard' in self.windowTitle():
            sticky = bool(get_app_config('Dashboard', 'sticky', boolean=True))

        if not sticky:
            try:
                x = event.globalX()
                y = event.globalY()
                x_w = self.offset.x()
                y_w = self.offset.y()
                self.move(x - x_w, y - y_w)
            except AttributeError as e:
                logger.warning('Move Event %s: %s', self.objectName(), str(e))
        else:
            pass
