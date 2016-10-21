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

import sys
from string import Template

from alignak_app import __application__

from PyQt5.QtWidgets import QApplication, QDialog, QLabel  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout  # pylint: disable=no-name-in-module
from PyQt5.QtCore import QTimer, Qt  # pylint: disable=no-name-in-module
from PyQt5.QtGui import QPixmap  # pylint: disable=no-name-in-module


class AppPopup(QDialog):
    """
    Class who create notifications.
    """

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(self.define_css())
        self.setWindowTitle(__application__)
        self.setContentsMargins(0, 0, 0, 0)
        self.msg_label = None
        self.state = None
        self.setMinimumSize(425, 250)
        self.setMaximumSize(425, 250)

    def initialize_notification(self):
        """
        Initialize Notification

        """

        title = self.create_title_label()
        msg = self.create_message_label()

        self.state = QLabel(self)
        self.state.setAlignment(Qt.AlignCenter)
        self.state.setObjectName('state')
        self.state.setMaximumHeight(20)

        vbox = QVBoxLayout(self)
        vbox.addLayout(title, 0)
        vbox.addWidget(self.state, 1)
        vbox.addWidget(msg, 2)

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

        # Get coordinate and move to right, up screen corner
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        x = (centerPoint.x() * 2) - self.width()
        y = (centerPoint.y() / 2) - self.height()
        self.move(x, y)

        # Notify
        self.state.setText(state_label)
        self.create_content(hosts_states, services_states)
        self.show()
        QTimer.singleShot(8000, self.close)

    def create_message_label(self):
        """
        Build msg QLabel.

        :return: QLabel
        :rtype: :class:`~PyQt5.QtWidgets.QLabel`
        """

        self.msg_label = QLabel(self)
        self.msg_label.setObjectName('msg')
        self.msg_label.setMinimumHeight(150)
        self.msg_label.setMinimumWidth(400)

        return self.msg_label

    def create_title_label(self):
        """
        Build title QLabel, with logo

        :return: QHBoxLayout of title
        :rtype: :class:`~PyQt5.QtWidgets.QHBoxLayout`
        """

        # Logo Label
        logo_label = QLabel(self)
        pixmap = QPixmap('../etc/images/alignak.svg')
        pixmap.setDevicePixelRatio(1.5)
        logo_label.setPixmap(pixmap)
        logo_label.setScaledContents(True)
        logo_label.setMaximumHeight(60)

        # Title Label
        title_label = QLabel(self)
        title_label.setText("Alignak-app")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName('title')
        title_label.setMaximumHeight(40)

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

    @staticmethod
    def get_basic_template():
        """
        Give basic template (NOTE: temporary...).

        :return: template
        :rtype: str
        """
        return """
        <table>
          <tr>
            <td>Hosts UP :</td>
            <td>$hosts_up</td>
          </tr>
          <tr>
            <td>Hosts DOWN :</td>
            <td>$hosts_down</td>
          </tr>
        <tr>
            <td>Hosts UNREACH :</td>
            <td>$hosts_unreachable</td>
          </tr>
        </table>
        <br>
        <table>
          <tr>
            <td>Services OK :</td>
            <td>$services_ok</td>
          </tr>
          <tr>
            <td>Services WARNING :</td>
            <td>$services_warning</td>
          </tr>
          <tr>
            <td>Services CRITICAL :</td>
            <td>$services_critical</td>
          </tr>
          <tr>
            <td>Services UNKNOWN :</td>
            <td>$services_unknown</td>
          </tr>
        </table>
        """

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
                hosts_down=str(hosts_states['up']),
                hosts_unreachable=str(hosts_states['up']),
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
