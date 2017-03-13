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
    App Dashboard create, update and display Dashboard QWidget.
"""

from logging import getLogger

from alignak_app import __application__
from alignak_app.core.utils import get_app_config, get_css
from alignak_app.dashboard.dashboard_factory import DashboardFactory
from alignak_app.widgets.app_widget import AppQWidget
from alignak_app.widgets.banner import send_diff_banners

from PyQt5.QtWidgets import QApplication, QWidget  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QLabel  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QVBoxLayout  # pylint: disable=no-name-in-module
from PyQt5.QtCore import QTimer, Qt  # pylint: disable=no-name-in-module
from PyQt5.Qt import pyqtSignal  # pylint: disable=no-name-in-module

logger = getLogger(__name__)


class Dashboard(QWidget):
    """
        Class who manage Dashboard QWidget.
    """

    dashboard_updated = pyqtSignal(dict, dict, name='dashboard')

    def __init__(self, parent=None):
        super(Dashboard, self).__init__(parent)
        # General settings
        self.setWindowTitle(__application__)
        self.setMaximumWidth(455)
        self.setStyleSheet(get_css())
        # Fields
        self.main_layout = QVBoxLayout(self)
        self.dashboard_type = None
        self.dashboard_factory = DashboardFactory(self)
        self.button = None
        self.timer = QTimer(self)
        self.app_widget = AppQWidget()

    def initialize(self):
        """
        Initialize Dashboard QWidget

        """

        self.app_widget.setWindowFlags(
            self.app_widget.windowFlags() | Qt.SplashScreen | Qt.WindowStaysOnTopHint
        )

        # Create Label for dashboard type
        self.dashboard_type = QLabel(self)
        self.dashboard_type.setAlignment(Qt.AlignCenter)
        self.dashboard_type.setObjectName('state')
        self.dashboard_type.setMinimumSize(425, 40)

        self.main_layout.addWidget(self.dashboard_type, 0)

        # Fill and add StateFactory
        self.fill_state_factory()
        self.main_layout.addWidget(self.dashboard_factory, 1)

        self.app_widget.initialize('Dashboard')
        self.app_widget.add_widget(self)

        self.dashboard_updated.connect(self.update_dashboard)

        # Set position of dashboard
        self.set_position()

    def fill_state_factory(self):
        """
        Inititalize each state in factory so that it can be modified later

        """

        # Hosts
        self.dashboard_factory.create_state_labels('hosts_up')
        self.dashboard_factory.create_state_labels('hosts_unreachable')
        self.dashboard_factory.create_state_labels('hosts_down')
        self.dashboard_factory.create_state_labels('hosts_acknowledge')
        self.dashboard_factory.create_state_labels('hosts_downtime')

        self.dashboard_factory.add_separator()

        # Services
        self.dashboard_factory.create_state_labels('services_ok')
        self.dashboard_factory.create_state_labels('services_warning')
        self.dashboard_factory.create_state_labels('services_critical')
        self.dashboard_factory.create_state_labels('services_unknown')
        self.dashboard_factory.create_state_labels('services_unreachable')
        self.dashboard_factory.create_state_labels('services_acknowledge')
        self.dashboard_factory.create_state_labels('services_downtime')

    def update_dashboard(self, synthesis, diff_synthesis):
        """
        Update Dashboard widgets

        :param synthesis: backend synthesis data
        :type synthesis: dict
        :param diff_synthesis: synthesis diff since last notifier check
        :type diff_synthesis: dict
        """

        logger.info('Update DashBoard...')

        # Dashboard title
        self.dashboard_type.setText(self.get_dashboard_title(synthesis))
        self.set_style_sheet(self.get_dashboard_title(synthesis))

        # Update content of DashboardFactory
        percentages = self.dashboard_factory.get_percentages_states(synthesis)

        if percentages['hosts'] and synthesis['hosts']:
            # Hosts
            for state in synthesis['hosts']:
                self.dashboard_factory.update_states(
                    'hosts_%s' % state,
                    synthesis['hosts'][state],
                    diff_synthesis['hosts'][state],
                    percentages['hosts'][state]
                )

            for state in synthesis['services']:
                self.dashboard_factory.update_states(
                    'services_%s' % state,
                    synthesis['services'][state],
                    diff_synthesis['services'][state],
                    percentages['services'][state]
                )

            if get_app_config('Dashboard', 'pop', boolean=True):
                self.display_dashboard()

            if get_app_config('Banners', 'changes', boolean=True):
                send_diff_banners(diff_synthesis)
        else:
            logger.error('Backend synthesis is empty: %s', synthesis['hosts'])

    def set_position(self):
        """
        Get screen, and return position choosen in settings.

        """

        # Get position choosed by user
        pos = get_app_config('Dashboard', 'position')
        points = pos.split(':')
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())

        # Move dashboard dashboard
        if 'top' in points and 'right' in points:
            top_right = QApplication.desktop().screenGeometry(screen).topRight()
            self.app_widget.move(top_right.x() - self.width(), top_right.y())
            log_msg = '[top:right] ' + str(top_right)
        elif 'top' in points and 'left' in points:  # pragma: no cover - not fully testable
            top_left = QApplication.desktop().screenGeometry(screen).topLeft()
            self.app_widget.move(top_left)
            log_msg = '[top:left] ' + str(top_left)
        elif 'bottom' in points and 'right' in points:  # pragma: no cover - not fully testable
            bottom_right = QApplication.desktop().screenGeometry(screen).bottomRight()
            self.app_widget.move(bottom_right.x() - self.width(), bottom_right.y() - self.height())
            log_msg = '[bottom:right] ' + str(bottom_right)
        elif 'bottom' in points and 'left' in points:  # pragma: no cover - not fully testable
            bottom_left = QApplication.desktop().screenGeometry(screen).bottomLeft()
            self.app_widget.move(bottom_left.x(), bottom_left.y() - self.height())
            log_msg = '[top:right] ' + str(bottom_left)
        else:  # pragma: no cover - not fully testable
            center = QApplication.desktop().screenGeometry(screen).center()
            self.app_widget.move(center.x() - (self.width() / 2), center.y() - (self.height() / 2))
            log_msg = '[center] ' + str(center)

        logger.debug('Dashboard Position %s', log_msg)

    def display_dashboard(self):
        """
        Update dashboard and display it

        """

        # Retrieve duration
        duration = int(get_app_config('Dashboard', 'duration'))
        duration *= 1000
        logger.debug('Dashboard Duration : %s', str(duration))

        # Display dashboard...
        self.app_widget.show()
        logger.info('Display dashboard...')

        # ...until the end of the term
        self.timer.timeout.connect(self.app_widget.close)
        self.timer.setSingleShot(True)
        self.timer.start(duration)

    @staticmethod
    def get_dashboard_title(synthesis):
        """
        Return dashboard title

        :param synthesis: backend synthesis data
        :type synthesis: dict
        :return: dashboard title
        :rtype: str
        """

        if synthesis['services']['critical'] > 0 or synthesis['hosts']['down'] > 0:
            dashboard_title = 'CRITICAL'
        elif synthesis['services']['unknown'] > 0 or \
                synthesis['services']['warning'] > 0 or \
                synthesis['hosts']['unreachable'] > 0:
            dashboard_title = 'WARNING'
        else:
            dashboard_title = 'OK'

        logger.debug('Dashboard title : %s', dashboard_title)

        return dashboard_title

    def set_style_sheet(self, title):
        """
        Define css for QWidgets.

        :return: css
        :rtype: str
        """

        if 'OK' in title:
            color_title = '#27ae60'
        elif 'WARNING' in title:
            color_title = '#e67e22'
        elif 'CRITICAL' in title:
            color_title = '#e74c3c'
        else:
            color_title = '#EEE'

        self.setStyleSheet(
            """
            QLabel#state{
                Background-color: %s;
                font-size: 16px bold;
            }
            """ % color_title
        )
