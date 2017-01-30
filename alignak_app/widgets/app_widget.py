#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016:
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

import sys

from logging import getLogger
from alignak_app.core.utils import get_image_path, init_config, get_css

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QStyle, QVBoxLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QLabel, QStyleOption  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QHBoxLayout, QPushButton  # pylint: disable=no-name-in-module
    from PyQt5.Qt import Qt, QIcon, QPixmap  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QApplication  # pylint: disable=import-error
    from PyQt4.Qt import QWidget, QStyle, QVBoxLayout  # pylint: disable=import-error
    from PyQt4.Qt import QLabel, QStyleOption  # pylint: disable=import-error
    from PyQt4.Qt import QHBoxLayout, QPushButton  # pylint: disable=import-error
    from PyQt4.Qt import Qt, QIcon, QPixmap  # pylint: disable=import-error


logger = getLogger(__name__)


class AppQWidget(QWidget):
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
        self.setObjectName(title)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        main_layout.addWidget(self.get_logo_widget())
        main_layout.addWidget(self.get_title_widget(title))

    def get_logo_widget(self):
        """
        Return the logo QWidget

        :return: logo QWidget
        :rtype: QWidget
        """

        logo_widget = QWidget()
        logo_widget.setFixedHeight(45)
        logo_layout = QHBoxLayout()
        logo_widget.setLayout(logo_layout)

        logo_label = QLabel()
        logo_label.setPixmap(QPixmap(get_image_path('alignak')))
        logo_label.setFixedSize(121, 35)
        logo_label.setScaledContents(True)

        logo_layout.addWidget(logo_label, 0)

        minimize_btn = QPushButton()
        minimize_btn.setIcon(QIcon(get_image_path('minimize')))
        minimize_btn.setFixedSize(24, 24)
        minimize_btn.clicked.connect(self.minimize)
        if self.objectName() == 'Notification':
            minimize_btn.setEnabled(False)
        logo_layout.addStretch(self.width())
        logo_layout.addWidget(minimize_btn, 1)

        maximize_btn = QPushButton()
        maximize_btn.setIcon(QIcon(get_image_path('maximize')))
        maximize_btn.setFixedSize(24, 24)
        maximize_btn.clicked.connect(self.minimize_maximize)
        if self.objectName() == 'Notification':
            maximize_btn.setEnabled(False)
        logo_layout.addWidget(maximize_btn, 2)

        close_btn = QPushButton()
        close_btn.setIcon(QIcon(get_image_path('exit')))
        close_btn.setFixedSize(24, 24)
        close_btn.clicked.connect(self.close)
        logo_layout.addWidget(close_btn, 3)

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

    @staticmethod
    def get_title_widget(title):
        """
        Return the title QWidget

        :return: title QWidget
        :rtype: QWidget
        """

        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_widget.setAttribute(Qt.WA_TransparentForMouseEvents)
        title_widget.setFixedHeight(50)
        title_widget.setObjectName('title')

        title_label = QLabel('<h2>%s</h2>' % title)
        title_label.setObjectName('title')

        title_layout.addWidget(title_label)
        title_layout.setAlignment(title_label, Qt.AlignCenter)

        return title_widget

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

    def add_widget(self, widget):
        """
        Add the main QWidget of AppQWidget

        :param widget: QWidget to add
        :type widget: QWidget
        """

        self.setMinimumSize(widget.size())
        self.layout().addWidget(widget, 2)

    def mousePressEvent(self, event):
        """ QWidget.mousePressEvent(QMouseEvent) """

        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        """ QWidget.mousePressEvent(QMouseEvent) """

        try:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)
        except AttributeError as e:
            logger.warning('Move Event %s: %s', self.objectName(), str(e))


if __name__ == '__main__':
    init_config()

    app = QApplication(sys.argv)

    app_widget = AppQWidget()
    app_widget.initialize('Alignak Status')

    widget_test = QWidget()
    widget_test.setMinimumSize(800, 600)
    layout_test = QVBoxLayout()
    widget_test.setLayout(layout_test)

    label_text = QLabel('This is a text')
    layout_test.addWidget(label_text)

    app_widget.add_widget(widget_test)

    app_widget.show_widget()

    sys.exit(app.exec_())
