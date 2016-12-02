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
    Popup Title manage creation of .
"""

from logging import getLogger

from alignak_app.core.utils import get_image_path

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


logger = getLogger(__name__)


class PopupTitle(QWidget):
    """
    Class who create popup title.
    """

    def __init__(self, parent=None):
        super(PopupTitle, self).__init__(parent)
        self.setObjectName('popup_title')
        self.setContentsMargins(0, -10, 0, 0)
        self.setFixedWidth(parent.width())
        self.setStyleSheet("""
            QWidget#popup_title {
                background-color: #4d788e;
            }
            QLabel#title {
                background-color: #4d788e;
                font-size: 20px;
                margin-top: 5px;
                color: white;
            }
        """)
        self.setAutoFillBackground(True)

    def create_title(self, name):
        """
        Build title QLabel, with logo QLabel

        """

        # Logo Label
        pixmap = QPixmap(get_image_path('icon'))

        logo_label = QLabel(self)
        logo_label.setFixedSize(35, 35)
        logo_label.setPixmap(pixmap)

        # Title Label
        title_label = QLabel(self)
        title_label.setText(name)
        title_label.setObjectName('title')
        title_label.setMaximumHeight(40)

        # Create title Layout
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(logo_label, 0)
        layout.setAlignment(logo_label, Qt.AlignBottom)
        layout.addStretch()
        layout.addWidget(title_label, 1)
        layout.setAlignment(title_label, Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

    # Reimplement paintEvent
    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)

        painter = QPainter(self)

        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
