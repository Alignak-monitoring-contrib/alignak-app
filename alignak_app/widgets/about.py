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
    About manage QWidget who display About window.
"""

from alignak_app import __application__
from alignak_app import __releasenotes__, __version__, __copyright__
from alignak_app import __doc_url__, __project_url__, __alignak_url__
from alignak_app.core.utils import get_css
from alignak_app.widgets.app_widget import AppQWidget

from PyQt5.QtWidgets import QVBoxLayout, QLabel  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget  # pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt  # pylint: disable=no-name-in-module


class AppAbout(QWidget):
    """
        Class who create QWidget for Alignak about.
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # General settings
        self.setToolTip('About')
        # Fields
        self.setStyleSheet(get_css())
        self.app_widget = AppQWidget()

    def create_window(self):
        """
        Create About layout and content

        """

        layout = QVBoxLayout()

        about_label = QLabel(self.get_about_text())
        about_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        about_label.setOpenExternalLinks(True)
        layout.addWidget(about_label)
        layout.setAlignment(about_label, Qt.AlignHCenter)

        self.setLayout(layout)

        # Add to AppQWidget
        self.app_widget.initialize('About %s' % __application__)
        self.app_widget.add_widget(self)
        self.app_widget.setMinimumSize(400, 400)

    @staticmethod
    def get_about_text():
        """
        Return about text

        :return: about text
        :rtype: str
        """

        text_replacement = (
            __application__,
            __version__,
            __copyright__,
            __project_url__,
            __project_url__,
            __doc_url__,
            __doc_url__,
            __releasenotes__,
            __alignak_url__,
            __alignak_url__,
        )

        about_text = \
            """
            <h4>Application version</h4>
            %s, version: %s
            <h4>Copyright</h4>
            %s
            <h4>Home page</h4>
            <p><a href="%s">%s</a></p>
            <h4>User documentation</h4>
            <p><a href="%s">%s</a></p>
            <h4>Release notes</h4>
            %s
            <h4>About Alignak Solution</h4>
            <p><a href="%s">%s</a></p>
            """ % text_replacement

        return about_text

    def show_about(self):
        """
        Show QWidget

        """

        self.app_widget.show_widget()
