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
    About QDialog manage application about data
"""


from PyQt5.Qt import Qt, QVBoxLayout, QLabel, QDialog  # pylint: disable=no-name-in-module

from alignak_app import __doc_url__, __project_url__, __alignak_url__, __application__
from alignak_app import __releasenotes__, __version__, __copyright__
from alignak_app.core.utils import get_css
from alignak_app.frames.app_frame import AppQWidget


class AboutQDialog(QDialog):
    """
        Class who create QDialog to display about data
    """

    def __init__(self, parent=None):
        super(AboutQDialog, self).__init__(parent)
        # General settings
        self.setToolTip(_('About'))
        self.setStyleSheet(get_css())
        # Fields
        self.app_widget = AppQWidget()

    def initialize(self):
        """
        Initialize QDialog

        """

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Version
        version_title = QLabel(_('Application version:'))
        version_title.setObjectName('title')
        layout.addWidget(version_title)
        version_data = QLabel(_('%s, version %s') % (__application__, __version__))
        layout.addWidget(version_data)

        # Copyright
        copyright_title = QLabel(_('Copyright:'))
        copyright_title.setObjectName('title')
        layout.addWidget(copyright_title)
        copyright_data = QLabel(__copyright__)
        layout.addWidget(copyright_data)

        # Homepage
        home_title = QLabel(_('Home page:'))
        home_title.setObjectName('title')
        layout.addWidget(home_title)
        layout.addWidget(self.get_external_link_label(__project_url__))

        # User Doc
        doc_title = QLabel(_('User documentation'))
        doc_title.setObjectName('title')
        layout.addWidget(doc_title)
        layout.addWidget(self.get_external_link_label(__doc_url__))

        # Release notes
        release_title = QLabel(_('Release notes:'))
        release_title.setObjectName('title')
        layout.addWidget(release_title)
        release_data = QLabel(__releasenotes__)
        layout.addWidget(release_data)

        # Alignak
        alignak_title = QLabel(_('About Alignak solution:'))
        alignak_title.setObjectName('title')
        layout.addWidget(alignak_title)
        layout.addWidget(self.get_external_link_label(__alignak_url__))

        # Add to AppQWidget
        self.app_widget.initialize(_('About %s') % __application__)
        self.app_widget.add_widget(self)
        self.app_widget.setMinimumSize(400, 400)

    @staticmethod
    def get_external_link_label(link):
        """
        Return QLabel with clickable text

        :param link: link to make clickable
        :type link: str
        :return: QLabel with clickable link
        :rtype: QLabel
        """

        link_label = QLabel('<a href="%s">%s</a>' % (link, link))
        link_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        link_label.setOpenExternalLinks(True)

        return link_label

    def show_about(self):
        """
        Show QWidget

        """

        self.app_widget.show_widget()
