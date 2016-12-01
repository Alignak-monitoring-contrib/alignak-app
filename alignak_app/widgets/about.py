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
    About manage QWidget who display About window.
"""

from logging import getLogger

from alignak_app import __application__
from alignak_app import __releasenotes__, __version__, __copyright__, __doc_url__, __project_url__
from alignak_app.core.utils import get_image_path, get_template

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QVBoxLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QLabel, QPushButton  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QApplication  # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QIcon  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import Qt  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    __import__('PyQt4')
    from PyQt4.Qt import QVBoxLayout  # pylint: disable=import-error
    from PyQt4.Qt import QLabel, QPushButton  # pylint: disable=import-error
    from PyQt4.Qt import QWidget, QApplication  # pylint: disable=import-error
    from PyQt4.QtGui import QIcon  # pylint: disable=import-error
    from PyQt4.QtCore import Qt  # pylint: disable=import-error

logger = getLogger(__name__)


class AppAbout(QWidget):
    """
        Class who create QWidget for Alignak about.
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # General settings
        self.setWindowTitle(__application__ + ': About')
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumSize(425, 400)
        self.setMaximumSize(425, 400)
        self.setWindowIcon(QIcon(get_image_path('icon')))
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        self.setWindowFlags(Qt.FramelessWindowHint)
        # Fields
        self.button = None

    def create_window(self):
        """
        Create About layout and content

        """

        about_layout = QVBoxLayout()
        self.setWindowIcon(QIcon(get_image_path('icon')))

        about_dict = dict(
            application=__application__,
            version=__version__,
            copyright=__copyright__,
            project_url=__project_url__,
            doc_url=__doc_url__,
            releasenotes=__releasenotes__
        )

        msg = get_template('about.tpl', about_dict)
        logger.debug('About Message : ' + str(msg))

        about_label = QLabel(msg)
        about_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        about_label.setOpenExternalLinks(True)
        about_layout.addWidget(about_label)

        self.create_button()
        about_layout.addWidget(self.button)
        about_layout.setAlignment(self.button, Qt.AlignCenter)

        self.setLayout(about_layout)

    def create_button(self):
        """
        Create valid button for About

        """

        self.button = QPushButton(self)
        self.button.setIcon(QIcon(get_image_path('checked')))
        self.button.setFixedSize(30, 30)

        self.button.setStyleSheet(
            """
QPushButton{
    Background-color: #eee;
    border: 2px solid #78909C;
    border-radius: 15px;
    text-align: center;
}
QPushButton:hover{
    Background-color: #ddd;
}"""
        )
        self.button.clicked.connect(self.close)

    def show_about(self):
        """
        Show QWidget

        """

        self.show()
