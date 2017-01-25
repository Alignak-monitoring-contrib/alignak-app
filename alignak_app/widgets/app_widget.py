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
    Title manage creation of widgets title.
"""

import sys

from alignak_app.core.utils import get_image_path, init_config

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QStyle  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QLabel, QStyleOption  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QIcon  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import Qt  # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QPixmap, QPainter, QSizePolicy  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QApplication  # pylint: disable=import-error
    from PyQt4.Qt import QWidget, QStyle, QVBoxLayout  # pylint: disable=import-error
    from PyQt4.Qt import QLabel, QStyleOption  # pylint: disable=import-error
    from PyQt4.Qt import QHBoxLayout, QPushButton, QIcon  # pylint: disable=import-error
    from PyQt4.QtCore import Qt  # pylint: disable=import-error
    from PyQt4.QtGui import QPixmap, QPainter, QSizePolicy  # pylint: disable=import-error


class AppQWidget(QWidget):
    """
    Class who create popup title.
    """

    def __init__(self, parent=None):
        super(AppQWidget, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(get_image_path('icon')))

    def initialize(self, title):
        """
        TODO
        :param title:
        :return:
        """

        self.setWindowTitle(title)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

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
        minimize_btn.clicked.connect(self.showMinimized)
        logo_layout.addStretch(self.width())
        logo_layout.addWidget(minimize_btn, 1)

        maximize_btn = QPushButton()
        maximize_btn.setIcon(QIcon(get_image_path('maximize')))
        maximize_btn.setFixedSize(24, 24)
        maximize_btn.clicked.connect(self.showMaximized)
        logo_layout.addWidget(maximize_btn, 2)

        close_btn = QPushButton()
        close_btn.setIcon(QIcon(get_image_path('exit')))
        close_btn.setFixedSize(24, 24)
        close_btn.clicked.connect(self.close)
        logo_layout.addWidget(close_btn, 3)

        main_layout.addWidget(logo_widget)
        main_layout.addStretch()

        title_label = QLabel('<h2>%s</h2>' % title)
        title_label.setStyleSheet(
            """
                background-color: #1a5b7b;
                color: white;
            """
        )
        title_label.setFixedHeight(50)
        title_label.setContentsMargins(self.width() / 2, 0, 0, 0)
        main_layout.addWidget(title_label, 1)
        main_layout.addStretch(self.width())

    def add_widget(self, widget):
        """
        TODO
        :param widget:
        :return:
        """

        self.layout().addWidget(widget, 2)

    def mousePressEvent(self, event):
        """ QWidget.mousePressEvent(QMouseEvent) """

        self.offset = event.pos()
        QApplication.setOverrideCursor(Qt.DragMoveCursor)

    def mouseMoveEvent(self, event):
        """ QWidget.mousePressEvent(QMouseEvent) """

        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)

    def mouseReleaseEvent(self, _):
        """ QWidget.mouseReleaseEvent(QMouseEvent) """

        QApplication.restoreOverrideCursor()

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

    app_widget.show()

    sys.exit(app.exec_())
