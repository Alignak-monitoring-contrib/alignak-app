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

    def create_notification(self, level, content):
        """
        Initialize Notification

        :param level: level of notif
        :param content: content of notif
        """

        title = self.notification_title()
        msg = self.notification_message(content)

        state = QLabel(self)
        state.setText(level)
        state.setAlignment(Qt.AlignCenter)
        state.setObjectName('state')
        state.setMaximumHeight(20)

        vbox = QVBoxLayout(self)
        vbox.addLayout(title, 0)
        vbox.addWidget(state, 1)
        vbox.addWidget(msg, 2)

    def notify(self):
        """
        Display notification.

        """

        ph = self.geometry().height()
        pw = self.geometry().width()
        px = self.geometry().x()
        py = self.geometry().y()
        dw = self.width()
        dh = self.height()
        print(ph, pw, px, py, dw, dh)
        # self.setGeometry(px, py + ph - dh, dw, dh)
        self.move(self.width() * 2, self.height() / 4)
        self.show()
        QTimer.singleShot(8000, self.close)

    def notification_message(self, msg):
        """
        Build msg QLabel.

        :param msg: msg to display.
        :return: QLabel
        :rtype: :class:`~PyQt5.QtWidgets.QLabel`
        """

        msg_label = QLabel(self)
        msg_label.setText(msg)
        msg_label.setObjectName('msg')
        msg_label.setMinimumHeight(150)
        msg_label.setMinimumWidth(400)

        return msg_label

    def notification_title(self):
        """
        Build title QLabel, with logo
        :param level:
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
    def create_content():
        """
        Create content and return with correct value.

        :return: tpl_content
        :rtype: str
        """

        tpl_content = """
        <table>
          <tr>
            <td>Hosts UP :</td>
            <td>N/A</td>
          </tr>
          <tr>
            <td>Hosts DOWN :</td>
            <td>N/A</td>
          </tr>
        <tr>
            <td>Hosts UNREACH :</td>
            <td>N/A</td>
          </tr>
        </table>
        <br>
        <table>
          <tr>
            <td>Services OK :</td>
            <td>N/A</td>
          </tr>
          <tr>
            <td>Services WARNING :</td>
            <td>N/A</td>
          </tr>
          <tr>
            <td>Services CRITICAL :</td>
            <td>N/A</td>
          </tr>
          <tr>
            <td>Services UNKNOWN :</td>
            <td>N/A</td>
          </tr>
        </table>
        """
        return tpl_content

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    notification = AppPopup()

    cur_level = "CRITICAL"
    cur_content = notification.create_content()

    notification.create_notification(cur_level, cur_content)
    notification.notify()

    QTimer.singleShot(8000, notification.close)

    sys.exit(app.exec_())
