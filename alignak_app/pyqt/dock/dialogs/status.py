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
    Status manage QWidget who display Alignak Daemons status.
"""

from logging import getLogger

from PyQt5.Qt import QDialog, QLabel, QWidget, Qt, QPushButton, QGridLayout, QHBoxLayout

from alignak_app.core.backend.data_manager import data_manager
from alignak_app.core.utils.config import app_css
from alignak_app.core.utils.time import get_time_diff_since_last_timestamp

from alignak_app.pyqt.common.widgets import center_widget
from alignak_app.pyqt.common.frames import AppQFrame
from alignak_app.pyqt.common.labels import get_icon_pixmap

logger = getLogger(__name__)


class StatusQDialog(QDialog):
    """
        Class who create QWidget for Daemons status.
    """

    def __init__(self, parent=None):
        super(StatusQDialog, self).__init__(parent)
        self.setStyleSheet(app_css)
        # Fields
        self.app_widget = AppQFrame()
        self.layout = QGridLayout()
        self.labels = {}

    def initialize(self):
        """
        Initialize QDialog

        """

        self.setLayout(self.layout)

        daemons = data_manager.database['alignakdaemon']

        self.set_daemons_labels(daemons)

        line = 0
        self.add_daemon_titles_labels(line)

        for daemon_item in daemons:
            line += 1
            self.add_daemon_labels(daemon_item, line)

        line += 1
        buttons_widget = self.get_buttons_widget()
        self.layout.addWidget(buttons_widget, line, 0, 1, 7)
        self.layout.setAlignment(buttons_widget, Qt.AlignCenter)

        # Use AppQWidget
        self.app_widget.initialize(_('Alignak Status'))
        self.app_widget.add_widget(self)
        center_widget(self.app_widget)

    def get_buttons_widget(self):
        """
        Return QWidget with buttons

        :return: widget with ok and refresh buttons
        :rtype: QWidget
        """

        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)

        ok_btn = QPushButton(_('OK'))
        ok_btn.setObjectName('valid')
        ok_btn.setFixedSize(120, 30)
        ok_btn.clicked.connect(self.app_widget.close)
        layout.addWidget(ok_btn)

        refresh_btn = QPushButton(_('Refresh'))
        refresh_btn.setObjectName('search')
        refresh_btn.setFixedSize(120, 30)
        refresh_btn.clicked.connect(self.update_dialog)
        layout.addWidget(refresh_btn)

        return widget

    def set_daemons_labels(self, daemons):
        """
        Initialize the daemon QLabels for each daemons

        :param daemons: list of daemon items
        :type daemons: list
        """

        daemons_attributes = [
            'alive', 'name', 'reachable', 'spare', 'address', 'port', 'passive', 'last_check'
        ]

        for daemon in daemons:
            self.labels[daemon.name] = {}
            for attribute in daemons_attributes:
                self.labels[daemon.name][attribute] = QLabel()

    def add_daemon_titles_labels(self, line):
        """
        Add QLabels titles for daemons to layout

        :param line: current line of layout
        :type line: int
        """

        # Icon Name Address	Reachable	Spare	Passive daemon	Last check
        icon_title = QLabel(_('State'))
        icon_title.setObjectName('title')
        self.layout.addWidget(icon_title, line, 0, 1, 1)
        self.layout.setAlignment(icon_title, Qt.AlignCenter)

        name_title = QLabel(_('Daemon name'))
        name_title.setObjectName('title')
        self.layout.addWidget(name_title, line, 1, 1, 1)

        address_title = QLabel(_('Address'))
        address_title.setObjectName('title')
        self.layout.addWidget(address_title, line, 2, 1, 1)

        reachable_title = QLabel(_('Reachable'))
        reachable_title.setObjectName('title')
        self.layout.addWidget(reachable_title, line, 3, 1, 1)
        self.layout.setAlignment(reachable_title, Qt.AlignCenter)

        spare_title = QLabel(_('Spare'))
        spare_title.setObjectName('title')
        self.layout.addWidget(spare_title, line, 4, 1, 1)
        self.layout.setAlignment(spare_title, Qt.AlignCenter)

        passive_title = QLabel(_('Passive daemon'))
        passive_title.setObjectName('title')
        self.layout.addWidget(passive_title, line, 5, 1, 1)
        self.layout.setAlignment(passive_title, Qt.AlignCenter)

        check_title = QLabel(_('Last check'))
        check_title.setObjectName('title')
        self.layout.addWidget(check_title, line, 6, 1, 1)

    def add_daemon_labels(self, daemon_item, line):
        """
        Add daemon QLabels to layout

        :param daemon_item: daemon item
        :type daemon_item: alignak_app.items.item_daemon.Daemon
        :param line: current line of layout
        :type line: int
        """

        # Alive
        self.labels[daemon_item.name]['alive'].setFixedSize(18, 18)
        self.labels[daemon_item.name]['alive'].setScaledContents(True)
        self.layout.addWidget(self.labels[daemon_item.name]['alive'], line, 0, 1, 1)
        self.layout.setAlignment(self.labels[daemon_item.name]['alive'], Qt.AlignCenter)

        # Name

        self.layout.addWidget(self.labels[daemon_item.name]['name'], line, 1, 1, 1)

        # Address
        self.layout.addWidget(self.labels[daemon_item.name]['address'], line, 2, 1, 1)

        # Reachable
        self.labels[daemon_item.name]['reachable'].setFixedSize(14, 14)
        self.labels[daemon_item.name]['reachable'].setScaledContents(True)
        self.layout.addWidget(self.labels[daemon_item.name]['reachable'], line, 3, 1, 1)
        self.layout.setAlignment(self.labels[daemon_item.name]['reachable'], Qt.AlignCenter)

        # Spare
        self.labels[daemon_item.name]['spare'].setFixedSize(14, 14)
        self.labels[daemon_item.name]['spare'].setScaledContents(True)
        self.layout.addWidget(self.labels[daemon_item.name]['spare'], line, 4, 1, 1)
        self.layout.setAlignment(self.labels[daemon_item.name]['spare'], Qt.AlignCenter)

        # Passive
        self.labels[daemon_item.name]['passive'].setFixedSize(14, 14)
        self.labels[daemon_item.name]['passive'].setScaledContents(True)
        self.layout.addWidget(self.labels[daemon_item.name]['passive'], line, 5, 1, 1)
        self.layout.setAlignment(self.labels[daemon_item.name]['passive'], Qt.AlignCenter)

        # Last check
        self.layout.addWidget(self.labels[daemon_item.name]['last_check'], line, 6, 1, 1)

    def update_dialog(self):
        """
        Update StatusQDialog labels

        """

        daemons = data_manager.database['alignakdaemon']

        for daemon_item in daemons:
            self.labels[daemon_item.name]['alive'].setPixmap(
                get_icon_pixmap(daemon_item.data['alive'], ['connected', 'disconnected'])
            )
            self.labels[daemon_item.name]['name'].setText(daemon_item.name)
            self.labels[daemon_item.name]['address'].setText(
                '%s:%s' % (daemon_item.data['address'], daemon_item.data['port'])
            )
            self.labels[daemon_item.name]['reachable'].setPixmap(
                get_icon_pixmap(daemon_item.data['reachable'], ['checked', 'error'])
            )
            self.labels[daemon_item.name]['spare'].setPixmap(
                get_icon_pixmap(daemon_item.data['spare'], ['checked', 'error'])
            )
            self.labels[daemon_item.name]['passive'].setPixmap(
                get_icon_pixmap(daemon_item.data['passive'], ['checked', 'error'])
            )
            last_check = get_time_diff_since_last_timestamp(daemon_item.data['last_check'])
            self.labels[daemon_item.name]['last_check'].setText(last_check)
