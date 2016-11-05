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

from string import Template
from logging import getLogger

from alignak_app import __application__
from alignak_app.utils import get_alignak_home

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication, QDialog, QLabel  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import QTimer, Qt  # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QPixmap  # pylint: disable=no-name-in-module
except ImportError:
    from PyQt4.Qt import QApplication, QDialog, QLabel  # pylint: disable=import-error
    from PyQt4.Qt import QHBoxLayout, QVBoxLayout  # pylint: disable=import-error
    from PyQt4.QtCore import QTimer, Qt  # pylint: disable=import-error
    from PyQt4.QtGui import QPixmap  # pylint: disable=import-error


logger = getLogger(__name__)


class AppPopup(QDialog):
    """
    Class who create notifications.
    """

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        # Main settings
        self.setStyleSheet(self.define_css())
        self.setWindowTitle(__application__)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumSize(425, 250)
        self.setMaximumSize(425, 250)
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # Fields
        self.msg_label = None
        self.state = None
        self.config = None

    def initialize_notification(self, config):
        """
        Initialize Notification

        """

        self.config = config
        title = self.create_title_label()
        self.create_message_label()

        self.state = QLabel(self)
        self.state.setAlignment(Qt.AlignCenter)
        self.state.setObjectName('state')
        self.state.setMaximumHeight(20)

        vbox = QVBoxLayout(self)
        vbox.addLayout(title, 0)
        vbox.addWidget(self.state, 1)
        vbox.addWidget(self.msg_label, 2)

    def send_notification(self, state_label, hosts_states, services_states):
        """
        Send notification.

        :param state_label: state to display in label_state.
        :type state_label: str
        :param hosts_states: dict of hosts states
        :type hosts_states: dict
        :param services_states: dict of services states.
        :type services_states: dict
        """

        # Get coordinate and move to [right,up] screen corner
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        x = (center_point.x() * 2) - self.width()
        y = (center_point.y() / 2) - self.height()
        self.move(x, y)

        # Notify
        self.state.setText(state_label)
        self.create_content(hosts_states, services_states)

        logger.info('Send notification...')

        self.show()
        QTimer.singleShot(8000, self.close)

    def create_message_label(self):
        """
        Build msg QLabel.

        """

        self.msg_label = QLabel(self)
        self.msg_label.setObjectName('msg')
        self.msg_label.setMinimumHeight(150)
        self.msg_label.setMinimumWidth(400)

    def create_title_label(self):
        """
        Build title QLabel, with logo

        :return: QHBoxLayout of title
        :rtype: :class:`~PyQt5.QtWidgets.QHBoxLayout`
        """

        # Logo Label
        logo_label = QLabel(self)
        icon_path = get_alignak_home() \
            + self.config.get('Config', 'path') \
            + self.config.get('Config', 'img') \
            + '/'
        pixmap = QPixmap(icon_path + 'alignak.svg')
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

    def close_dialog(self):
        """
        Close notification.

        """

        self.hide()

    def get_basic_template(self):
        """
        Give basic template (NOTE: temporary...).

        :return: template
        :rtype: str
        """
        tpl_path = get_alignak_home() \
            + self.config.get('Config', 'path') \
            + self.config.get('Config', 'tpl') \
            + '/'

        tpl = open(tpl_path + 'basic.tpl')

        return tpl.read()

    def create_content(self, hosts_states, services_states):
        """
        Create content and return with correct value.

        :param hosts_states: states of hosts
        :type hosts_states: dict
        :param services_states: states of services
        :type services_states: dict
        """

        if services_states['ok'] < 0 or hosts_states['up'] < 0:
            tpl_content = 'AlignakApp has something broken... \nPlease Check your logs !'
        else:
            tpl = Template(self.get_basic_template())
            state_dict = dict(
                hosts_up=str(hosts_states['up']),
                hosts_down=str(hosts_states['down']),
                hosts_unreachable=str(hosts_states['unreachable']),
                services_ok=str(services_states['ok']),
                services_warning=str(services_states['warning']),
                services_critical=str(services_states['critical']),
                services_unknown=str(services_states['unknown']),
            )

            tpl_content = tpl.safe_substitute(state_dict)

        self.msg_label.setText(tpl_content)

    @staticmethod
    def define_css():
        """
        Define css for QWidgets.

        :return: css
        :rtype: str
        """

        css = """
        QWidget{
            Background: #eee;
            color:white;
        }
        QLabel#title{
            Background: #78909C;
            border: none;
            border-radius: 10px;
            font-size: 18px bold;
        }
        QLabel#msg{
            Background: #eee;
            color: black;
        }
        QLabel#state{
            Background-color: #e74c3c;
            font-size: 16px bold;

        }
        QToolButton{
            Background: #eee;
            border: none;
        }
        """
        return css
