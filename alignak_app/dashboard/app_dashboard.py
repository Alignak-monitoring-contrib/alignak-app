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

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication, QWidget  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QLabel  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QVBoxLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import QTimer, Qt  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QApplication, QWidget  # pylint: disable=import-error
    from PyQt4.Qt import QLabel  # pylint: disable=import-error
    from PyQt4.Qt import QVBoxLayout  # pylint: disable=import-error
    from PyQt4.QtCore import QTimer, Qt  # pylint: disable=import-error


logger = getLogger(__name__)


class Dashboard(QWidget):
    """
        Class who manage Dashboard QWidget.
    """

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
        self.pin = False
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

    def fill_state_factory(self):
        """
        Populate the factory so that it can be modified later

        """

        # Hosts
        self.dashboard_factory.create_state_labels('hosts_up')
        self.dashboard_factory.create_state_labels('hosts_unreach')
        self.dashboard_factory.create_state_labels('hosts_down')
        self.dashboard_factory.create_state_labels('acknowledged', item_type='hosts')
        self.dashboard_factory.create_state_labels('downtime', item_type='hosts')

        self.dashboard_factory.add_separator()

        # Services
        self.dashboard_factory.create_state_labels('services_ok')
        self.dashboard_factory.create_state_labels('services_warning')
        self.dashboard_factory.create_state_labels('services_critical')
        self.dashboard_factory.create_state_labels('services_unknown')
        self.dashboard_factory.create_state_labels('services_unreachable')
        self.dashboard_factory.create_state_labels('acknowledged', item_type='services')
        self.dashboard_factory.create_state_labels('downtime', item_type='services')

    def update_dashboard(self, hosts_states, services_states, diff):
        """
        Update Dashboard widgets

        :param hosts_states: states of hosts
        :type hosts_states: dict
        :param services_states: states of services
        :type services_states: dict
        :param diff: dict of changes since the last check of notifier.
        :type diff: dict
        """

        percentages = self.dashboard_factory.get_percentages_states(hosts_states, services_states)

        if percentages:
            # Hosts
            self.dashboard_factory.update_states(
                'hosts_up',
                hosts_states['up'],
                diff['hosts']['up'],
                percentages['up']
            )
            self.dashboard_factory.update_states(
                'hosts_down',
                hosts_states['down'],
                diff['hosts']['down'],
                percentages['down']
            )
            self.dashboard_factory.update_states(
                'hosts_unreach',
                hosts_states['unreachable'],
                diff['hosts']['unreachable'],
                percentages['hosts_unreachable']
            )
            self.dashboard_factory.update_states(
                'hosts_acknowledged',
                hosts_states['acknowledge'],
                diff['hosts']['acknowledge'],
                percentages['hosts_acknowledge']
            )
            self.dashboard_factory.update_states(
                'hosts_downtime',
                hosts_states['downtime'],
                diff['hosts']['downtime'],
                percentages['hosts_downtime']
            )

            # Services
            self.dashboard_factory.update_states(
                'services_ok',
                services_states['ok'],
                diff['services']['ok'],
                percentages['ok']
            )
            self.dashboard_factory.update_states(
                'services_warning',
                services_states['warning'],
                diff['services']['warning'],
                percentages['warning']
            )
            self.dashboard_factory.update_states(
                'services_critical',
                services_states['critical'],
                diff['services']['critical'],
                percentages['critical']
            )
            self.dashboard_factory.update_states(
                'services_unknown',
                services_states['unknown'],
                diff['services']['unknown'],
                percentages['unknown']
            )
            self.dashboard_factory.update_states(
                'services_unreachable',
                services_states['unreachable'],
                diff['services']['unreachable'],
                percentages['services_unreachable']
            )
            self.dashboard_factory.update_states(
                'services_acknowledged',
                services_states['acknowledge'],
                diff['services']['acknowledge'],
                percentages['services_acknowledge']
            )
            self.dashboard_factory.update_states(
                'services_downtime',
                services_states['downtime'],
                diff['services']['downtime'],
                percentages['services_downtime']
            )

    def set_position(self):
        """
        Get screen, and return position choosen in settings.

        """

        # Get position choosed by user
        pos = get_app_config('Alignak-App', 'position')
        points = pos.split(':')

        # Move dashboard dashboard
        if 'top' in points and 'right' in points:
            screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
            top_right = QApplication.desktop().screenGeometry(screen).topRight()
            self.app_widget.move(top_right.x() - self.width(), top_right.y())
            msg = '[top:right] ' + str(top_right)
        elif 'top' in points and 'left' in points:  # pragma: no cover - not fully testable
            screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
            top_left = QApplication.desktop().screenGeometry(screen).topLeft()
            self.app_widget.move(top_left)
            msg = '[top:left] ' + str(top_left)
        elif 'bottom' in points and 'right' in points:  # pragma: no cover - not fully testable
            screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
            bottom_right = QApplication.desktop().screenGeometry(screen).bottomRight()
            self.app_widget.move(bottom_right.x() - self.width(), bottom_right.y() - self.height())
            msg = '[bottom:right] ' + str(bottom_right)
        elif 'bottom' in points and 'left' in points:  # pragma: no cover - not fully testable
            screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
            bottom_left = QApplication.desktop().screenGeometry(screen).bottomLeft()
            self.app_widget.move(bottom_left.x(), bottom_left.y() - self.height())
            msg = '[top:right] ' + str(bottom_left)
        else:  # pragma: no cover - not fully testable
            screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
            center = QApplication.desktop().screenGeometry(screen).center()
            self.app_widget.move(center.x() - (self.width() / 2), center.y() - (self.height() / 2))
            msg = '[center] ' + str(center)

        logger.debug('Position ' + msg)

    def display_dashboard(self, level_notif, hosts_states, services_states, diff):
        """
        Update dashboard and display it

        :param level_notif: state to display in label_state.
        :type level_notif: str
        :param hosts_states: dict of hosts states
        :type hosts_states: dict
        :param services_states: dict of services states.
        :type services_states: dict
        :param diff: dict of changes since the last check of notifier.
        :type diff: dict
        """

        # Set position of dashboard
        self.set_position()

        # Prepare dashboard
        self.dashboard_type.setText(level_notif)
        self.set_style_sheet(level_notif)

        # Update content of DashboardFactory
        self.update_dashboard(hosts_states, services_states, diff)
        send_diff_banners(diff)

        # Retrieve duration
        duration = int(get_app_config('Alignak-App', 'duration'))
        duration *= 1000
        logger.debug('Dashboard Duration : ' + str(duration))

        # Display dashboard...
        self.app_widget.show()
        logger.info('Display dashboard...')

        # ...until the end of the term
        self.timer.timeout.connect(self.close_pin)
        self.timer.setSingleShot(True)
        self.timer.start(duration)

    def close_pin(self):
        """
        Check if pin is set to True, else close

        """

        if not self.pin:
            self.app_widget.close()
        else:
            pass

    def mousePressEvent(self, _):
        """
        Reimplement Mouse press event

        """

        self.timer.stop()
        self.pin = True

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
