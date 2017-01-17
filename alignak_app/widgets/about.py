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

from alignak_app import __application__
from alignak_app import __releasenotes__, __version__, __copyright__, __doc_url__, __project_url__
from alignak_app.core.utils import get_image_path, get_template, get_css
from alignak_app.widgets.title import get_widget_title

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


class AppAbout(QWidget):
    """
        Class who create QWidget for Alignak about.
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # General settings
        self.setWindowTitle(__application__ + ': About')
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowIcon(QIcon(get_image_path('icon')))
        self.setToolTip('About')
        self.setWindowFlags(Qt.FramelessWindowHint)
        # Fields
        self.button = None
        self.setStyleSheet(get_css())

    def center(self):
        """
        Center QWidget

        """

        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center = QApplication.desktop().screenGeometry(screen).center()
        self.move(center.x() - (self.width() / 2), center.y() - (self.height() / 2))

    def create_window(self):
        """
        Create About layout and content

        """

        layout = QVBoxLayout()
        self.setWindowIcon(QIcon(get_image_path('icon')))

        # Popup title
        title = get_widget_title('about ' + __application__, self)
        layout.addWidget(title)

        # About infos
        about_dict = dict(
            application=__application__,
            version=__version__,
            copyright=__copyright__,
            project_url=__project_url__,
            doc_url=__doc_url__,
            releasenotes=__releasenotes__
        )

        msg = get_template('about.tpl', about_dict)

        about_label = QLabel(msg)
        about_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        about_label.setOpenExternalLinks(True)
        layout.addWidget(about_label)

        # Button
        self.create_button()
        layout.addWidget(self.button)
        layout.setAlignment(self.button, Qt.AlignCenter)

        self.setLayout(layout)

    def create_button(self):
        """
        Create valid button for About

        """

        self.button = QPushButton(self)
        self.button.setIcon(QIcon(get_image_path('checked')))
        self.button.setFixedSize(30, 30)
        self.button.setObjectName('valid')

        self.button.clicked.connect(self.close)

    def show_about(self):
        """
        Show QWidget

        """
        self.center()
        self.show()
