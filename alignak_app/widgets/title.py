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

from alignak_app.core.utils import get_image_path, get_css

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QWidget, QStyle  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QLabel, QStyleOption  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QHBoxLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import Qt  # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QPixmap, QPainter  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QWidget, QStyle  # pylint: disable=import-error
    from PyQt4.Qt import QLabel, QStyleOption  # pylint: disable=import-error
    from PyQt4.Qt import QHBoxLayout  # pylint: disable=import-error
    from PyQt4.QtCore import Qt  # pylint: disable=import-error
    from PyQt4.QtGui import QPixmap, QPainter  # pylint: disable=import-error


class Title(QWidget):
    """
    Class who create popup title.
    """

    def __init__(self, parent=None):
        super(Title, self).__init__(parent)
        self.setObjectName('popup_title')
        self.setContentsMargins(0, -10, 0, 0)
        self.setStyleSheet(get_css())

    def create_title(self, name, parent=None):
        """
        Build title QLabel, with logo QLabel

        :param name: name of the title
        :type name: str
        :param parent: QWidget parent
        :type parent: QWidget
        """

        if 'notification' in name and parent:
            self.setFixedWidth(parent.width())

        # Logo Label
        pixmap = QPixmap(get_image_path('alignak'))

        logo_label = QLabel(self)
        logo_label.setFixedSize(132, 40)
        logo_label.setScaledContents(True)
        logo_label.setObjectName('logo')
        logo_label.setPixmap(pixmap)

        # Title Label
        title_label = QLabel(self)
        title_label.setText(name.title())
        title_label.setObjectName('title_label')
        title_label.setMaximumHeight(40)

        # Create title Layout
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(logo_label, 0)
        layout.addWidget(title_label, 1)
        layout.setAlignment(title_label, Qt.AlignCenter)

        self.setLayout(layout)

    # Reimplement paintEvent
    def paintEvent(self, event):  # pylint: disable=unused-argument
        """
        Paint QWidget title.

        :param event: event from QPainter
        :type event: QPaintEvent
        """

        opt = QStyleOption()
        opt.initFrom(self)

        painter = QPainter(self)

        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)


def get_widget_title(title, parent):
    """
    Create QWidget title and return it.

    :param title: name of title
    :type title: str
    :param parent: QWidget parent
    :type parent: QWidget
    :return: qwidget Title
    :rtype: Title
    """

    popup_title = Title(parent)
    popup_title.create_title(title, parent)

    return popup_title
