#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016:
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
    Notification build notifications QWidgets.
"""

from logging import getLogger

from alignak_app import __application__
from alignak_app.core.utils import get_app_config
from alignak_app.core.utils import get_css
from alignak_app.popup.notification_factory import NotificationFactory
from alignak_app.widgets.title import get_widget_title

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication, QWidget  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QLabel  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QVBoxLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import QTimer, Qt  # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QPixmap  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QApplication, QWidget  # pylint: disable=import-error
    from PyQt4.Qt import QLabel  # pylint: disable=import-error
    from PyQt4.Qt import QVBoxLayout  # pylint: disable=import-error
    from PyQt4.QtCore import QTimer, Qt  # pylint: disable=import-error
    from PyQt4.QtGui import QPixmap  # pylint: disable=import-error


logger = getLogger(__name__)


class AppNotification(QWidget):
    """
        Class who create QWidget notifications.
    """

    def __init__(self, parent=None):
        super(AppNotification, self).__init__(parent)
        # General settings
        self.setWindowTitle(__application__)
        self.setMaximumWidth(455)
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # Fields
        self.main_layout = QVBoxLayout(self)
        self.notification_type = None
        self.popup_factory = NotificationFactory(self)
        self.button = None
        self.timer = QTimer(self)
        self.pin = False
        self.setStyleSheet(get_css())

    def initialize_notification(self):
        """
        Initialize Notification

        """

        # Create and add Layout for notification title
        popup_title = get_widget_title('notification', self)
        self.main_layout.addWidget(popup_title, 0)
        self.main_layout.setAlignment(popup_title, Qt.AlignCenter)

        # Create Label for notification type
        self.notification_type = QLabel(self)
        self.notification_type.setAlignment(Qt.AlignCenter)
        self.notification_type.setObjectName('state')
        self.notification_type.setMinimumSize(425, 40)

        self.main_layout.addWidget(self.notification_type, 1)

        # Fill and add StateFactory
        self.fill_state_factory()
        self.main_layout.addWidget(self.popup_factory, 2)

        # Create and add button
        button = self.popup_factory.add_valid_button()
        button.clicked.connect(self.close_notification)

    def close_notification(self):
        """
        Close notification and set pin at False

        """

        self.pin = False
        self.close()

    def fill_state_factory(self):
        """
        Populate the factory so that it can be modified later

        """

        # self.popup_factory = PopupFactory(self)

        # Hosts
        self.popup_factory.create_state_labels('hosts_up')
        self.popup_factory.create_state_labels('hosts_unreach')
        self.popup_factory.create_state_labels('hosts_down')
        self.popup_factory.create_state_labels('acknowledged', item_type='hosts')
        self.popup_factory.create_state_labels('downtime', item_type='hosts')

        self.popup_factory.add_separator()

        # Services
        self.popup_factory.create_state_labels('services_ok')
        self.popup_factory.create_state_labels('services_warning')
        self.popup_factory.create_state_labels('services_critical')
        self.popup_factory.create_state_labels('services_unknown')
        self.popup_factory.create_state_labels('services_unreachable')
        self.popup_factory.create_state_labels('acknowledged', item_type='services')
        self.popup_factory.create_state_labels('downtime', item_type='services')

    def update_popup(self, hosts_states, services_states, diff):
        """
        Create notification content

        :param hosts_states: states of hosts
        :type hosts_states: dict
        :param services_states: states of services
        :type services_states: dict
        :param diff: dict of changes since the last check of notifier.
        :type diff: dict
        """

        percentages = self.popup_factory.get_percentages_states(hosts_states, services_states)

        if percentages:
            # Hosts
            self.popup_factory.update_states(
                'hosts_up',
                hosts_states['up'],
                diff['hosts']['up'],
                percentages['up']
            )
            self.popup_factory.update_states(
                'hosts_down',
                hosts_states['down'],
                diff['hosts']['down'],
                percentages['down']
            )
            self.popup_factory.update_states(
                'hosts_unreach',
                hosts_states['unreachable'],
                diff['hosts']['unreachable'],
                percentages['hosts_unreachable']
            )
            self.popup_factory.update_states(
                'hosts_acknowledged',
                hosts_states['acknowledge'],
                diff['hosts']['acknowledge'],
                percentages['hosts_acknowledge']
            )
            self.popup_factory.update_states(
                'hosts_downtime',
                hosts_states['downtime'],
                diff['hosts']['downtime'],
                percentages['hosts_downtime']
            )

            # Services
            self.popup_factory.update_states(
                'services_ok',
                services_states['ok'],
                diff['services']['ok'],
                percentages['ok']
            )
            self.popup_factory.update_states(
                'services_warning',
                services_states['warning'],
                diff['services']['warning'],
                percentages['warning']
            )
            self.popup_factory.update_states(
                'services_critical',
                services_states['critical'],
                diff['services']['critical'],
                percentages['critical']
            )
            self.popup_factory.update_states(
                'services_unknown',
                services_states['unknown'],
                diff['services']['unknown'],
                percentages['unknown']
            )
            self.popup_factory.update_states(
                'services_unreachable',
                services_states['unreachable'],
                diff['services']['unreachable'],
                percentages['services_unreachable']
            )
            self.popup_factory.update_states(
                'services_acknowledged',
                services_states['acknowledge'],
                diff['services']['acknowledge'],
                percentages['services_acknowledge']
            )
            self.popup_factory.update_states(
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

        # Move notification popup
        if 'top' in points and 'right' in points:
            screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
            top_right = QApplication.desktop().screenGeometry(screen).topRight()
            self.move(top_right.x() - self.width(), top_right.y())
            msg = '[top:right] ' + str(top_right)
        elif 'top' in points and 'left' in points:  # pragma: no cover - not fully testable
            screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
            top_left = QApplication.desktop().screenGeometry(screen).topLeft()
            self.move(top_left)
            msg = '[top:left] ' + str(top_left)
        elif 'bottom' in points and 'right' in points:  # pragma: no cover - not fully testable
            screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
            bottom_right = QApplication.desktop().screenGeometry(screen).bottomRight()
            self.move(bottom_right.x() - self.width(), bottom_right.y() - self.height())
            msg = '[bottom:right] ' + str(bottom_right)
        elif 'bottom' in points and 'left' in points:  # pragma: no cover - not fully testable
            screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
            bottom_left = QApplication.desktop().screenGeometry(screen).bottomLeft()
            self.move(bottom_left.x(), bottom_left.y() - self.height())
            msg = '[top:right] ' + str(bottom_left)
        else:  # pragma: no cover - not fully testable
            screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
            center = QApplication.desktop().screenGeometry(screen).center()
            self.move(center.x() - (self.width() / 2), center.y() - (self.height() / 2))
            msg = '[center] ' + str(center)

        logger.debug('Position ' + msg)

    def send_notification(self, level_notif, hosts_states, services_states, diff):
        """
        Send notification.

        :param level_notif: state to display in label_state.
        :type level_notif: str
        :param hosts_states: dict of hosts states
        :type hosts_states: dict
        :param services_states: dict of services states.
        :type services_states: dict
        :param diff: dict of changes since the last check of notifier.
        :type diff: dict
        """

        # Set position of popup
        self.set_position()

        # Prepare notification
        self.notification_type.setText(level_notif)
        self.set_style_sheet(level_notif)

        # Update content of PopupFactory
        self.update_popup(hosts_states, services_states, diff)

        # Retrieve duration
        duration = int(get_app_config('Alignak-App', 'duration'))
        duration *= 1000
        logger.debug('Notification Duration : ' + str(duration))

        logger.info('Send notification...')

        # Start notification...
        self.show()

        # ...until the end of the term
        self.timer.timeout.connect(self.close_pin)
        self.timer.setSingleShot(True)
        self.timer.start(duration)

    def close_pin(self):
        """
        Check if pin is set to True, else close

        """

        if not self.pin:
            self.close()
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
