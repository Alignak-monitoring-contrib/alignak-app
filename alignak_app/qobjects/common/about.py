#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2018:
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
    About
    +++++
    About manage creation of QDialog to display data about Alignak-app
"""


from PyQt5.Qt import Qt, QVBoxLayout, QLabel, QDialog, QWidget

from alignak_app import __doc_url__, __project_url__, __alignak_url__, __application__
from alignak_app import __releasenotes__, __version__, __copyright__

from alignak_app.utils.config import settings


class AboutQDialog(QDialog):
    """
        Class who create QDialog to display about data
    """

    def __init__(self, parent=None):
        super(AboutQDialog, self).__init__(parent)
        self.setObjectName('about')
        self.setStyleSheet(settings.css_style)
        self.setFixedSize(500, 450)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.setToolTip(_('About %s') % __application__)

    def initialize(self):
        """
        Initialize QDialog

        """

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        about_widget = QWidget()
        about_widget.setObjectName('about')
        about_layout = QVBoxLayout(about_widget)

        # QDialog Title
        about_title = QLabel(_('About'))
        about_title.setFixedHeight(40)
        about_title.setObjectName('aboutheader')
        main_layout.addWidget(about_title)

        # Main About
        about_text = "%s\nVersion %s\nCopyright: %s" % \
            (__application__, __version__, __copyright__)
        main_about = QLabel(about_text)
        main_about.setObjectName('aboutmain')
        main_about.setToolTip(__application__)
        about_layout.addWidget(main_about)
        about_layout.setAlignment(main_about, Qt.AlignCenter)

        # Release notes
        release_data = QLabel(__releasenotes__)
        release_data.setObjectName('about')
        release_data.setToolTip(_('Release notes'))
        release_data.setWordWrap(True)
        about_layout.addWidget(release_data)

        # Homepage
        home_title = QLabel(_('Home page:'))
        home_title.setObjectName('abouttitle')
        home_title.setToolTip(_('Home page'))
        about_layout.addWidget(home_title)
        about_layout.addWidget(self.get_external_link_label(__project_url__))

        # User Doc
        doc_title = QLabel(_('User documentation'))
        doc_title.setObjectName('abouttitle')
        doc_title.setToolTip(_('User documentation'))
        about_layout.addWidget(doc_title)
        about_layout.addWidget(self.get_external_link_label(__doc_url__))

        # Alignak
        alignak_title = QLabel(_('About Alignak solution:'))
        alignak_title.setObjectName('abouttitle')
        alignak_title.setToolTip(_('About Alignak solution'))
        about_layout.addWidget(alignak_title)
        about_layout.addWidget(self.get_external_link_label(__alignak_url__))

        # Powered
        powered_title = QLabel(_('Powered by:'))
        powered_title.setObjectName('abouttitle')
        powered_title.setToolTip(_('PyQt5'))
        about_layout.addWidget(powered_title)
        powered_data = self.get_external_link_label('https://www.riverbankcomputing.com/', 'PyQt5')
        about_layout.addWidget(powered_data)

        main_layout.addWidget(about_widget)

    def show_about(self):
        """
        Show about dialog

        """

        # Exec_ to make sure that dialog popup is displayed under Win32
        self.exec_()
        self.show()

    @staticmethod
    def get_external_link_label(link, title=''):
        """
        Return QLabel with clickable text

        :param link: link to make clickable
        :type link: str
        :param title: title of link
        :type title: str
        :return: QLabel with clickable link
        :rtype: QLabel
        """

        if not title:
            title = link

        link_label = QLabel('<a href="%s" style="color: white;">%s</a>' % (link, title))
        link_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        link_label.setOpenExternalLinks(True)
        link_label.setObjectName('about')
        link_label.setToolTip(link)
        link_label.setWordWrap(True)

        return link_label
