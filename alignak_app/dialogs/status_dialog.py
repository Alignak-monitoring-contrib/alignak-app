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

from PyQt5.QtCore import Qt, QTimer  # pylint: disable=no-name-in-module
from PyQt5.QtGui import QPixmap  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGridLayout, QAction  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QLabel  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget  # pylint: disable=no-name-in-module

from alignak_app import __application__
from alignak_app.app_widget import AppQWidget
from alignak_app.dock.events_widget import events_widget
from alignak_app.core.data_manager import data_manager
from alignak_app.core.utils import get_image_path, get_css, get_app_config
from alignak_app.items.item_daemon import Daemon

logger = getLogger(__name__)


class AlignakStatus(QWidget):
    """
        Class who create QWidget for Daemons status.
    """

    def __init__(self, parent=None):
        super(AlignakStatus, self).__init__(parent)
        # General settings
        self.setWindowTitle(__application__)
        self.setToolTip(_('Alignak Status'))
        self.setStyleSheet(get_css())
        # Fields
        self.daemons_labels = {}
        self.info = None
        self.old_bad_daemons = 0
        self.app_widget = AppQWidget()
        self.first_start = True

    def create_status(self):
        """
        Create grid layout for status QWidget

        """

        # Add Layout
        layout = QGridLayout()
        self.setLayout(layout)

        self.create_daemons_labels(layout)

        # Default text and color
        self.info.setText(_('All daemons are alive.'))
        self.info.setStyleSheet('color: #27ae60;')

        # Update status for first start
        self.check_status()

        # Start checks
        daemon_interval = int(get_app_config('Alignak-App', 'daemon_interval'))
        if bool(daemon_interval) and daemon_interval > 0:
            logger.debug('Alignak Daemons will be checked in %ss', str(daemon_interval))
            daemon_interval *= 1000
        else:
            logger.error(
                '"daemon_interval" option must be greater than 0. Replace by default: 60s'
            )
            daemon_interval = 60000
        timer = QTimer(self)
        timer.start(daemon_interval)
        timer.timeout.connect(self.check_status)

        # Use AppQWidget
        self.app_widget.initialize(_('Alignak Status'))
        self.app_widget.add_widget(self)
        self.app_widget.setMinimumSize(400, 400)

    def create_daemons_labels(self, layout):
        """
        Create QLabels and Pixmaps for each daemons

        """

        help_txt = QLabel(_('(Hover your mouse over each daemon to learn more)'))
        help_txt.setObjectName('help')
        layout.addWidget(help_txt, 0, 0, 1, 2)
        layout.setAlignment(help_txt, Qt.AlignCenter)

        layout.addWidget(QLabel(_('<b>Daemons Types</b> ')), 1, 0, 1, 1)
        status_title = QLabel(_('<b>Status</b>'))
        status_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(status_title, 1, 1, 1, 1)

        line = 2

        for daemon in Daemon.get_daemons_names():
            # Initialize dict for each daemon type
            self.daemons_labels[daemon] = {
                'label': QLabel(daemon.capitalize() + 's'),
                'icon': QLabel(),
            }

            self.daemons_labels[daemon]['icon'].setFixedSize(24, 24)
            self.daemons_labels[daemon]['icon'].setScaledContents(True)

            layout.addWidget(
                self.daemons_labels[daemon]['label'], line, 0
            )
            layout.addWidget(
                self.daemons_labels[daemon]['icon'], line, 1
            )
            layout.setAlignment(self.daemons_labels[daemon]['icon'], Qt.AlignCenter)
            line += 1

        self.info = QLabel()
        layout.addWidget(self.info, line, 0, 1, 2)
        layout.setAlignment(self.info, Qt.AlignCenter)
        line += 1

    def check_status(self):
        """
        Check daemons states, update icons and display banner if changes.

        """

        total_bad_daemons = 0
        total_daemons = 0
        arbiter_down = False

        daemon_msg = dict((element, '') for element in Daemon.get_daemons_names())
        bad_daemons = dict((element, 0) for element in Daemon.get_daemons_names())

        alignak_daemons = data_manager.database['alignakdaemon']
        if alignak_daemons:
            for daemon in alignak_daemons:
                if not daemon.data['alive']:
                    bad_daemons[daemon.data['type']] += 1
                    total_bad_daemons += 1
                    daemon_msg[daemon.data['type']] += \
                        _('<p>%s is not alive</p>') % daemon.name.capitalize()
                    if daemon == 'arbiter':
                        arbiter_down = True

                if not bad_daemons[daemon.data['type']]:
                    self.daemons_labels[daemon.data['type']]['icon'].setPixmap(
                        QPixmap(get_image_path('valid'))
                    )
                    self.daemons_labels[daemon.data['type']]['icon'].setToolTip(
                        _('All %ss are alive ') % daemon.data['type']
                    )
                    self.daemons_labels[daemon.data['type']]['label'].setToolTip(
                        _('All %ss are alive ') % daemon.data['type']
                    )
                else:
                    self.daemons_labels[daemon.data['type']]['icon'].setPixmap(
                        QPixmap(get_image_path('error'))
                    )
                    self.daemons_labels[daemon.data['type']]['icon'].setToolTip(
                        daemon_msg[daemon.data['type']]
                    )
                    self.daemons_labels[daemon.data['type']]['label'].setToolTip(
                        daemon_msg[daemon.data['type']]
                    )

                total_daemons += 1
        else:
            arbiter_down = True

        # Update text
        if not total_bad_daemons:
            self.info.setText(_('All daemons are alive.'))
            self.info.setStyleSheet('color: #27ae60;')
            if self.first_start:
                self.first_start = False
                events_widget.add_event('INFO', _('All daemons are alive.'))
            logger.info('All daemons are alive.')
        else:
            self.info.setText(_('%d on %d daemons are down !') % (total_bad_daemons, total_daemons))
            self.info.setStyleSheet('color: #e74c3c;')
            logger.warning('%d on %d daemons are down !', total_bad_daemons, total_daemons)

        # Send Banners if sender is QTimer
        if not isinstance(self.sender(), QAction):  # pragma: no cover
            if not total_bad_daemons and (self.old_bad_daemons != 0):
                events_widget.add_event('OK', _('All daemons are alive again.'))
            if total_bad_daemons:
                events_widget.add_event(
                    'WARN',
                    _('%d on %d daemons are down !') % (total_bad_daemons, total_daemons)
                )
                if arbiter_down:
                    self.info.setText(
                        _('Arbiter daemons are DOWN ! %d on %d daemons are down.') % (
                            total_bad_daemons, total_daemons
                        )
                    )
                    self.info.setStyleSheet('color: #e74c3c;')
                    events_widget.add_event('ALERT', _('Arbiter daemons are down !'))
                    logger.critical('Arbiter daemons are down !')

        self.old_bad_daemons = total_bad_daemons

    def show_states(self):
        """
        Show AlignakStatus

        """

        self.check_status()
        self.app_widget.show_widget()
