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
    User Options
    ++++++++++++
    User Options manage creation options of QDialogs for user notifications options
"""

from logging import getLogger

from PyQt5.Qt import QGridLayout, QLabel, QWidget, Qt, QDialog, QVBoxLayout, QPushButton, QIcon

from alignak_app.utils.config import settings

from alignak_app.qobjects.common.labels import get_icon_pixmap
from alignak_app.qobjects.common.widgets import get_logo_widget, center_widget

logger = getLogger(__name__)


class UserOptionsQDialog(QDialog):
    """
        Class who create options QDialog
    """

    def __init__(self, parent=None):
        super(UserOptionsQDialog, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(settings.css_style)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        self.setFixedSize(350, 300)
        self.setObjectName('dialog')
        # Fields
        self.options_labels = {
            'host': {
                'd': QLabel(),
                'u': QLabel(),
                'r': QLabel(),
                'f': QLabel(),
                's': QLabel(),
                'n': QLabel()
            },
            'service': {
                'w': QLabel(),
                'u': QLabel(),
                'c': QLabel(),
                'r': QLabel(),
                'f': QLabel(),
                's': QLabel(),
                'n': QLabel()
            }
        }
        self.titles_labels = {
            'host': {
                'd': QLabel('DOWN'),
                'u': QLabel('UNREACHABLE'),
                'r': QLabel('RECOVERY'),
                'f': QLabel('FLAPPING'),
                's': QLabel('DOWNTIME'),
                'n': QLabel('NONE')
            },
            'service': {
                'w': QLabel('WARNING'),
                'u': QLabel('UNKNOWN'),
                'c': QLabel('CRITICAL'),
                'r': QLabel('RECOVERY'),
                'f': QLabel('FLAPPING'),
                's': QLabel('DOWNTIME'),
                'n': QLabel('NONE')
            }
        }

    def initialize(self, item_type, options):
        """
        Initialize QDialog with App widget logo and options QWidget

        :param item_type: define item type for options: host or service
        :type item_type: str
        :param options: list of notification options
        :type options: list
        """

        center_widget(self)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        if item_type == 'host':
            logo_widget_title = _('Host Notifications')
        else:
            logo_widget_title = _('Service Notifications')
        main_layout.addWidget(
            get_logo_widget(self, logo_widget_title)
        )
        main_layout.addWidget(self.get_notifications_widget(item_type, options))

    def get_notifications_widget(self, item_type, options):
        """
        Create QWidget with options and their icons

        :param item_type: define item type for options: host or service
        :type item_type: str
        :param options: list of notification options
        :type options: list
        :return: QWidget with options and icons
        :rtype: QWidget
        """

        options_widget = QWidget()
        options_widget.setObjectName('dialog')
        options_layout = QGridLayout(options_widget)

        options_title = QLabel(_("Options:"))
        options_title.setObjectName("itemtitle")
        options_layout.addWidget(options_title, 0, 0, 1, 2)
        options_layout.setAlignment(options_title, Qt.AlignCenter)

        line = 1
        selected_options = self.get_selected_options(item_type, options)
        for opt in selected_options:
            # Title
            object_name = 'option' + str(selected_options[opt])
            self.titles_labels[item_type][opt].setObjectName(object_name)
            options_layout.addWidget(self.titles_labels[item_type][opt], line, 0, 1, 1)
            # Icon
            self.options_labels[item_type][opt].setPixmap(
                get_icon_pixmap(selected_options[opt], ['checked', 'error'])
            )
            self.options_labels[item_type][opt].setFixedSize(14, 14)
            self.options_labels[item_type][opt].setScaledContents(True)
            options_layout.addWidget(self.options_labels[item_type][opt], line, 1, 1, 1)
            line += 1

        # Login button
        accept_btn = QPushButton(_('OK'), self)
        accept_btn.clicked.connect(self.accept)
        accept_btn.setObjectName('ok')
        accept_btn.setMinimumHeight(30)
        options_layout.addWidget(accept_btn, line, 0, 1, 2)

        return options_widget

    @staticmethod
    def get_selected_options(item_type, options):
        """
        Return the options who are selected or not

        :param item_type: type of item we want options
        :type item_type: str
        :param options: options for the wanted item type
        :type options: list
        :return: dict of options selected
        :rtype: dict
        """

        items_options = {
            'host': ['d', 'u', 'r', 'f', 's', 'n'],
            'service': ['w', 'u', 'c', 'r', 'f', 's', 'n']
        }

        available_options = items_options[item_type]

        selected_options = {}
        for opt in available_options:
            selected_options[opt] = bool(opt in options)

        return selected_options


def show_options_dialog(item_type, notification_options):
    """
    Show the UserOptionsQDialog

    :param item_type: type of item we want options
    :type item_type: str
    :param notification_options: options for the wanted item type
    :type notification_options: list
    """

    option_widget = UserOptionsQDialog()
    option_widget.initialize(item_type, notification_options)
    option_widget.exec_()
