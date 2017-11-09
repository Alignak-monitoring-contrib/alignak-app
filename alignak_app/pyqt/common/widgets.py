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
    Utils QWidget manage global QWidgets used by Alignak-app
"""

from PyQt5.Qt import QPushButton, QHBoxLayout, QApplication, QWidget, QIcon, QLabel
from PyQt5.Qt import QStyleOption, QStyle, QPainter

from alignak_app.core.utils.config import get_image, app_css


class LogoQWidget(QWidget):
    """
        Class who manage creation of Logo QWidget
    """

    def __init__(self):
        super(LogoQWidget, self).__init__()
        self.setFixedHeight(45)
        self.setObjectName('app_widget')
        self.setStyleSheet(app_css)

    def initialize(self, child_widget, title):
        """
        Initialize QWidget

        :param child_widget: widget child of LogoQWidget, needed for action button and layout
        :type child_widget: QWidget
        :param title: title of widget
        :type title: str
        """

        logo_layout = QHBoxLayout()
        self.setLayout(logo_layout)

        logo_label = QLabel()
        logo_label.setObjectName('widget_title')
        logo_label.setText('<h4>%s</h4>' % title)
        logo_layout.addWidget(logo_label, 0)

        minimize_btn = QPushButton()
        minimize_btn.setIcon(QIcon(get_image('minimize')))
        minimize_btn.setFixedSize(24, 24)
        minimize_btn.setObjectName('app_widget')
        minimize_btn.clicked.connect(child_widget.showMinimized)
        logo_layout.addStretch(child_widget.width())
        logo_layout.addWidget(minimize_btn, 1)

        maximize_btn = QPushButton()
        maximize_btn.setIcon(QIcon(get_image('maximize')))
        maximize_btn.setFixedSize(24, 24)
        maximize_btn.setObjectName('app_widget')
        maximize_btn.clicked.connect(child_widget.showMaximized)
        logo_layout.addWidget(maximize_btn, 2)

        close_btn = QPushButton()
        close_btn.setIcon(QIcon(get_image('exit')))
        close_btn.setObjectName('app_widget')
        close_btn.setFixedSize(24, 24)
        close_btn.clicked.connect(child_widget.close)
        logo_layout.addWidget(close_btn, 3)

    def paintEvent(self, _):  # pragma: no cover
        """Override to apply "background-color" property of QWidget"""

        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)


def get_logo_widget(child_widget, title):
    """
    Return LogoQWidget with alignak logo

    :param child_widget: widget child of LogoQWidget, needed for action button and layout
    :type child_widget: QWidget
    :param title: title of widget
    :type title: str
    :return: Logo QWidget with buttons and child QWidget
    :rtype: QWidget
    """

    logo_widget = LogoQWidget()
    logo_widget.initialize(child_widget, title)

    return logo_widget


def center_widget(widget):
    """
    Center QWidget

    :param widget: widget to center
    :type widget: QWidget
    """

    screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
    center = QApplication.desktop().screenGeometry(screen).center()
    widget.move(center.x() - (widget.width() / 2), center.y() - (widget.height() / 2))
