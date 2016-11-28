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
    Popup build notifications.
"""

from logging import getLogger

from alignak_app import __application__
from alignak_app.utils import get_template
from alignak_app.utils import get_app_config, get_image_path
from alignak_app.popup_factory import PopupFactory

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication, QWidget  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QLabel, QPushButton  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import QTimer, Qt  # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QPixmap, QIcon  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QApplication, QWidget  # pylint: disable=import-error
    from PyQt4.Qt import QLabel, QPushButton  # pylint: disable=import-error
    from PyQt4.Qt import QHBoxLayout, QVBoxLayout  # pylint: disable=import-error
    from PyQt4.QtCore import QTimer, Qt  # pylint: disable=import-error
    from PyQt4.QtGui import QPixmap, QIcon  # pylint: disable=import-error


logger = getLogger(__name__)


class AppPopup(QWidget):
    """
    Class who create notifications.
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # General settings
        self.setWindowTitle(__application__)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumSize(450, 340)
        self.setMaximumSize(450, 340)
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # Fields
        self.main_layout = QVBoxLayout(self)
        self.notification_type = None
        self.state_factory = None
        self.button = None

    def initialize_notification(self):
        """
        Initialize Notification

        """

        # Create and add Layout for notification title
        layout_title = self.create_layout_title()
        self.main_layout.addLayout(layout_title, 0)

        # Create Label for notification type
        self.notification_type = QLabel(self)
        self.notification_type.setAlignment(Qt.AlignCenter)
        self.notification_type.setObjectName('state')
        self.notification_type.setMinimumSize(450, 20)

        self.main_layout.addWidget(self.notification_type, 1)
        self.main_layout.setAlignment(self.notification_type, Qt.AlignCenter)

        # Create and add StateFactory
        self.fill_state_factory()
        self.main_layout.addWidget(self.state_factory, 2)

        # Create and add button
        self.create_button()
        self.main_layout.addWidget(self.button, 3)
        self.main_layout.setAlignment(self.button, Qt.AlignCenter)

    def fill_state_factory(self):
        """
        Populate the factory so that it can be modified later

        """

        self.state_factory = PopupFactory()

        # Hosts
        self.state_factory.create_state('hosts_up')
        self.state_factory.create_state('hosts_down')
        self.state_factory.create_state('hosts_unreach')

        # Services
        self.state_factory.create_state('services_ok')
        self.state_factory.create_state('services_warning')
        self.state_factory.create_state('services_critical')
        self.state_factory.create_state('services_unknown')

    def create_layout_title(self):
        """
        Build title QLabel, with logo

        :return: QHBoxLayout of title
        :rtype: :class:`~PyQt5.QtWidgets.QHBoxLayout`
        """

        # Logo Label
        pixmap = QPixmap(get_image_path('icon'))

        logo_label = QLabel(self)
        logo_label.setPixmap(pixmap)
        logo_label.setScaledContents(True)
        logo_label.setMaximumHeight(32)

        # Title Label
        title_label = QLabel(self)
        title_label.setText("Alignak-app")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName('title')
        title_label.setMaximumHeight(32)

        # Create title Layout
        tbox = QHBoxLayout()
        tbox.addWidget(logo_label, 0)
        tbox.addWidget(title_label, 1)

        return tbox

    def create_button(self):
        """
        Create valid button for popup

        """

        self.button = QPushButton(self)
        self.button.setIcon(QIcon(get_image_path('checked')))
        self.button.setMinimumSize(30, 30)
        self.button.setMaximumSize(40, 40)

        self.button.setStyleSheet(get_template('button.tpl', None))
        self.button.clicked.connect(self.close)

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
            logger.debug('Position top:right : ' + str(top_right))
        elif 'top' in points and 'left' in points:  # pragma: no cover - not fully testable
            screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
            top_left = QApplication.desktop().screenGeometry(screen).topLeft()
            self.move(top_left)
            logger.debug('Position top:left : ' + str(top_left))
        elif 'bottom' in points and 'right' in points:  # pragma: no cover - not fully testable
            screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
            bottom_right = QApplication.desktop().screenGeometry(screen).bottomRight()
            self.move(bottom_right.x() - self.width(), bottom_right.y() - self.height())
            logger.debug('Position bottom:right : ' + str(bottom_right))
        elif 'bottom' in points and 'left' in points:  # pragma: no cover - not fully testable
            screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
            bottom_left = QApplication.desktop().screenGeometry(screen).bottomLeft()
            self.move(bottom_left.x(), bottom_left.y() - self.height())
            logger.debug('Position top:right : ' + str(bottom_left))
        else:  # pragma: no cover - not fully testable
            screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
            center = QApplication.desktop().screenGeometry(screen).center()
            self.move(center.x() - (self.width() / 2), center.y() - (self.height() / 2))
            logger.debug('Position center : ' + str(center))

    def send_notification(self, title, hosts_states, services_states, diff):
        """
        Send notification.

        :param title: state to display in label_state.
        :type title: str
        :param hosts_states: dict of hosts states
        :type hosts_states: dict
        :param services_states: dict of services states.
        :type services_states: dict
        :param diff: dict of changes since the last check of notifier.
        :type diff: dict
        """

        # Set position of popup
        self.set_position()

        # Check if services and hosts are positive
        if services_states['ok'] < 0 or hosts_states['up'] < 0:
            title = 'CRITICAL'

        # Prepare notification
        self.notification_type.setText(title)
        self.setStyleSheet(self.get_style_sheet(title))

        # Update content of PopupFactory
        self.create_content(hosts_states, services_states, diff)

        # Retrieve duration
        duration = int(get_app_config('Alignak-App', 'duration'))
        duration *= 1000
        logger.debug('Position Duration : ' + str(duration))

        logger.info('Send notification...')

        # Start notification...
        self.show()

        # ...until the end of the term
        QTimer.singleShot(duration, self.close)

    def create_content(self, hosts_states, services_states, diff):
        """
        Create notification content

        :param hosts_states: states of hosts
        :type hosts_states: dict
        :param services_states: states of services
        :type services_states: dict
        :param diff: dict of changes since the last check of notifier.
        :type diff: dict
        """

        if services_states['ok'] < 0 or hosts_states['up'] < 0:
            self.state_factory = QLabel(
                'AlignakApp has something broken... \nPlease Check your logs !'
            )
        else:
            # Hosts
            self.state_factory.update_states(
                'hosts_up',
                hosts_states['up'],
                diff['hosts']['up'],
                10
            )
            self.state_factory.update_states(
                'hosts_down',
                hosts_states['down'],
                diff['hosts']['down'],
                20
            )
            self.state_factory.update_states(
                'hosts_unreach',
                hosts_states['unreachable'],
                diff['hosts']['unreachable'],
                30
            )

            # Services
            self.state_factory.update_states(
                'services_ok',
                services_states['ok'],
                diff['services']['ok'],
                20
            )
            self.state_factory.update_states(
                'services_warning',
                services_states['warning'],
                diff['services']['warning'],
                40
            )
            self.state_factory.update_states(
                'services_critical',
                services_states['critical'],
                diff['services']['critical'],
                60
            )
            self.state_factory.update_states(
                'services_unknown',
                services_states['unknown'],
                diff['services']['unknown'],
                80
            )

    @staticmethod
    def get_style_sheet(title):
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

        css = get_template('popup_title_css.tpl', dict(color_title=color_title))

        return css
