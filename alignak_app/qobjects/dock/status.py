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
    Status
    ++++++
    Status manage creation of QWidget and QDialog for Alignak status:

    * Alignak daemons status: status of each daemons
    * Alignak backend status: status of backend connection

"""

from logging import getLogger

from PyQt5.Qt import QLabel, QPushButton, QIcon, QStyleOption, QPainter, QStyle, QDialog
from PyQt5.Qt import QWidget, QHBoxLayout, QTimer, QPixmap, Qt, QGridLayout

from alignak_app.backend.backend import app_backend
from alignak_app.backend.datamanager import data_manager
from alignak_app.items.daemon import Daemon
from alignak_app.utils.config import settings
from alignak_app.utils.time import get_time_diff_since_last_timestamp

from alignak_app.qobjects.common.widgets import center_widget
from alignak_app.qobjects.common.frames import AppQFrame
from alignak_app.qobjects.common.labels import get_icon_pixmap

logger = getLogger(__name__)


class StatusQDialog(QDialog):
    """
        Class who create QWidget for Daemons status.
    """

    def __init__(self, parent=None):
        super(StatusQDialog, self).__init__(parent)
        self.setStyleSheet(settings.css_style)
        # Fields
        self.app_widget = AppQFrame()
        self.layout = QGridLayout()
        self.labels = {}
        self.no_status_lbl = QLabel()

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
        refresh_btn.setObjectName('ok')
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


class StatusQWidget(QWidget):
    """
        Class who display daemons and backend status
    """

    def __init__(self):
        super(StatusQWidget, self).__init__()
        # Fields
        self.status_btn = QPushButton()
        self.daemons_status = QLabel('pending...')
        self.backend_connected = QLabel('pending...')
        self.status_dialog = StatusQDialog()
        self.refresh_timer = QTimer()

    def initialize(self):
        """
        Initialize QWidget

        """

        self.update_status()

        layout = QHBoxLayout()
        self.setLayout(layout)

        # Daemons
        daemons_title = QLabel(_('Status:'))
        daemons_title.setObjectName('subtitle')
        layout.addWidget(daemons_title)
        layout.setAlignment(daemons_title, Qt.AlignCenter)

        self.daemons_status.setFixedSize(16, 16)
        self.daemons_status.setScaledContents(True)
        layout.addWidget(self.daemons_status)
        layout.setAlignment(self.daemons_status, Qt.AlignCenter)

        # Status button
        self.status_dialog.initialize()
        self.status_btn.setIcon(QIcon(settings.get_image('icon')))
        self.status_btn.setFixedSize(32, 32)
        self.status_btn.clicked.connect(self.show_status_dialog)
        layout.addWidget(self.status_btn)
        layout.setAlignment(self.status_btn, Qt.AlignCenter)

        # Backend state
        connected_title = QLabel(_('Backend:'))
        connected_title.setObjectName('subtitle')
        layout.addWidget(connected_title)
        layout.setAlignment(connected_title, Qt.AlignCenter)

        self.backend_connected.setFixedSize(16, 16)
        self.backend_connected.setScaledContents(True)
        layout.addWidget(self.backend_connected)
        layout.setAlignment(self.backend_connected, Qt.AlignCenter)

        update_status = int(settings.get_config('Alignak-app', 'update_status')) * 1000
        self.refresh_timer.setInterval(update_status)
        self.refresh_timer.start()
        self.refresh_timer.timeout.connect(self.update_status)

    def show_status_dialog(self):
        """
        Update and show StatusQDialog

        """

        self.status_dialog.update_dialog()
        self.status_dialog.app_widget.show_widget()

    def update_status(self):
        """
        Update daemons and backend status

        """

        self.backend_connected.setPixmap(
            QPixmap(settings.get_image(app_backend.get_backend_status_icon()))
        )

        self.status_btn.setEnabled(bool(data_manager.database['alignakdaemon']))

        self.daemons_status.setPixmap(
            QPixmap(settings.get_image(Daemon.get_daemons_status_icon()))
        )

    def paintEvent(self, _):
        """Override to paint background"""

        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
