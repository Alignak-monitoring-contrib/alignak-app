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
    Status manage creation of QDialog for daemons status
"""

from logging import getLogger

from PyQt5.Qt import Qt, QDialog, QGridLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from alignak_app.backend.datamanager import data_manager
from alignak_app.utils.config import settings
from alignak_app.utils.time import get_diff_since_last_timestamp

from alignak_app.qobjects.common.labels import get_icon_pixmap
from alignak_app.qobjects.common.widgets import center_widget, get_logo_widget
from alignak_app.qobjects.events.events import send_event

logger = getLogger(__name__)


class StatusQDialog(QDialog):
    """
        Class who create QWidget for Daemons status.
    """

    def __init__(self, parent=None):
        super(StatusQDialog, self).__init__(parent)
        self.setStyleSheet(settings.css_style)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName('dialog')
        # Fields
        self.offset = None
        self.daemons_layout = QGridLayout()
        self.labels = {}
        self.no_status_lbl = QLabel()

    def initialize(self):
        """
        Initialize QDialog

        """

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(get_logo_widget(self, _('User View')))

        # Daemons QWidget
        daemons_widget = QWidget(self)
        daemons_widget.setLayout(self.daemons_layout)

        daemons = data_manager.database['alignakdaemon']

        # Init QLabels
        self.init_daemons_labels(daemons)

        # Add daemons label
        line = 0
        self.add_daemon_titles_labels(line)

        for daemon_item in daemons:
            line += 1
            self.add_daemon_labels(daemon_item, line)

        line += 1

        # Ok QPushButton
        ok_btn = QPushButton(_('OK'))
        ok_btn.setObjectName('ok')
        ok_btn.setFixedSize(120, 30)
        ok_btn.clicked.connect(self.accept)
        self.daemons_layout.addWidget(ok_btn, line, 0, 1, 7)
        self.daemons_layout.setAlignment(ok_btn, Qt.AlignCenter)

        main_layout.addWidget(daemons_widget)
        center_widget(self)

    def init_daemons_labels(self, daemons):
        """
        Initialize the daemon QLabels for each daemons

        :param daemons: list of daemon items
        :type daemons: list
        """

        daemons_attributes = [
            'alive', 'name', 'reachable', 'spare', 'address', 'passive', 'last_check'
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
        self.daemons_layout.addWidget(icon_title, line, 0, 1, 1)
        self.daemons_layout.setAlignment(icon_title, Qt.AlignCenter)

        name_title = QLabel(_('Daemon name'))
        name_title.setObjectName('title')
        self.daemons_layout.addWidget(name_title, line, 1, 1, 1)

        address_title = QLabel(_('Address'))
        address_title.setObjectName('title')
        self.daemons_layout.addWidget(address_title, line, 2, 1, 1)

        reachable_title = QLabel(_('Reachable'))
        reachable_title.setObjectName('title')
        self.daemons_layout.addWidget(reachable_title, line, 3, 1, 1)
        self.daemons_layout.setAlignment(reachable_title, Qt.AlignCenter)

        spare_title = QLabel(_('Spare'))
        spare_title.setObjectName('title')
        self.daemons_layout.addWidget(spare_title, line, 4, 1, 1)
        self.daemons_layout.setAlignment(spare_title, Qt.AlignCenter)

        passive_title = QLabel(_('Passive daemon'))
        passive_title.setObjectName('title')
        self.daemons_layout.addWidget(passive_title, line, 5, 1, 1)
        self.daemons_layout.setAlignment(passive_title, Qt.AlignCenter)

        check_title = QLabel(_('Last check'))
        check_title.setObjectName('title')
        self.daemons_layout.addWidget(check_title, line, 6, 1, 1)

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
        self.daemons_layout.addWidget(self.labels[daemon_item.name]['alive'], line, 0, 1, 1)
        self.daemons_layout.setAlignment(self.labels[daemon_item.name]['alive'], Qt.AlignCenter)

        # Name
        self.daemons_layout.addWidget(self.labels[daemon_item.name]['name'], line, 1, 1, 1)

        # Address
        self.daemons_layout.addWidget(self.labels[daemon_item.name]['address'], line, 2, 1, 1)

        # Reachable
        self.labels[daemon_item.name]['reachable'].setFixedSize(14, 14)
        self.labels[daemon_item.name]['reachable'].setScaledContents(True)
        self.daemons_layout.addWidget(self.labels[daemon_item.name]['reachable'], line, 3, 1, 1)
        self.daemons_layout.setAlignment(self.labels[daemon_item.name]['reachable'], Qt.AlignCenter)

        # Spare
        self.labels[daemon_item.name]['spare'].setFixedSize(14, 14)
        self.labels[daemon_item.name]['spare'].setScaledContents(True)
        self.daemons_layout.addWidget(self.labels[daemon_item.name]['spare'], line, 4, 1, 1)
        self.daemons_layout.setAlignment(self.labels[daemon_item.name]['spare'], Qt.AlignCenter)

        # Passive
        self.labels[daemon_item.name]['passive'].setFixedSize(14, 14)
        self.labels[daemon_item.name]['passive'].setScaledContents(True)
        self.daemons_layout.addWidget(self.labels[daemon_item.name]['passive'], line, 5, 1, 1)
        self.daemons_layout.setAlignment(self.labels[daemon_item.name]['passive'], Qt.AlignCenter)

        # Last check
        self.daemons_layout.addWidget(self.labels[daemon_item.name]['last_check'], line, 6, 1, 1)

    def update_dialog(self):
        """
        Update StatusQDialog labels and return if all daemons are ok or not

        :return: if status of daemons is ok or not
        :rtype: bool
        """

        daemons = data_manager.database['alignakdaemon']
        status_ok = True

        for daemon_item in daemons:
            if daemon_item.name in self.labels:
                # Connected icon
                self.labels[daemon_item.name]['alive'].setPixmap(
                    get_icon_pixmap(daemon_item.data['alive'], ['connected', 'disconnected'])
                )

                # Labels
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
                last_check = get_diff_since_last_timestamp(daemon_item.data['last_check'])
                self.labels[daemon_item.name]['last_check'].setText(last_check)

                # Check if daemon is a problem
                if self.daemon_is_problem(daemon_item):
                    status_ok = False
            else:
                logger.error('KeyError: %s', daemon_item.name)
                logger.error('\tLabel keys : %s', self.labels.keys())

        return status_ok

    @staticmethod
    def daemon_is_problem(daemon_item):
        """
        Check Daemon Refresh and if daemon is alive. Send a message if needed

        :param daemon_item: Daemon item
        :type daemon_item: alignak_app.items.daemon.Daemon
        :return: if daemon is a problem True, else False
        :rtype: bool
        """

        is_problem = False

        actual_freshness = get_diff_since_last_timestamp(
            daemon_item.data['last_check'], 'minutes'
        )
        freshness = settings.get_config('Alignak-app', 'daemons_freshness')
        if int(actual_freshness) > int(freshness):
            send_event(
                'CRITICAL' if 'arbiter' in daemon_item.name else 'WARNING',
                _('Freshness expired for %s') % daemon_item.name,
                timer=True
            )
            is_problem = True
            logger.warning('Daemon freshness expired: %s(%dmn)', daemon_item.name, actual_freshness)

        if not daemon_item.data['alive']:
            send_event(
                'CRITICAL' if 'arbiter' in daemon_item.name else 'WARNING',
                _('Daemon %s is dead !') % daemon_item.name,
                timer=True
            )
            logger.warning('Daemon %s is dead...', daemon_item.name)
            is_problem = True

        return is_problem

    def mousePressEvent(self, event):  # pragma: no cover
        """ QWidget.mousePressEvent(QMouseEvent) """

        self.offset = event.pos()

    def mouseMoveEvent(self, event):  # pragma: no cover
        """ QWidget.mousePressEvent(QMouseEvent) """

        try:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)
        except AttributeError as e:
            logger.warning('Move Event %s: %s', self.objectName(), str(e))
