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
    Tick send some stick notifications for small informations.
"""

from alignak_app.core.utils import get_image_path

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QHBoxLayout, QApplication  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QPushButton, QLabel  # pylint: disable=no-name-in-module
    from PyQt5.Qt import Qt, QIcon, QTimer, QPoint  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QObject, pyqtSignal  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import QPropertyAnimation  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QHBoxLayout, QApplication  # pylint: disable=import-error
    from PyQt4.Qt import QWidget, QPushButton, QLabel, QIcon  # pylint: disable=import-error
    from PyQt4.QtCore import Qt, QTimer, QPoint, pyqtSignal  # pylint: disable=import-error
    from PyQt4.QtCore import QObject, pyqtSignal  # pylint: disable=import-error
    from PyQt4.QtCore import QPropertyAnimation  # pylint: disable=import-error


class TickManager(object):
    """
        Class who send and manage ticks
    """

    def __init__(self):
        self.ticks = []
        self.ticks_to_send = []
        self.timer = None

    def start(self):
        """
        Start manager. Manager checks if there is tick to send or not.

        """

        self.timer = QTimer()
        self.timer.start(4000)
        self.timer.timeout.connect(self.check_ticks)

    def check_ticks(self):
        """
        Check ticks to send

        """

        if self.ticks_to_send:
            for old_tick in self.ticks:
                pos = old_tick.pos()
                old_tick.move(pos.x(), pos.y() + old_tick.height())

            tick = self.ticks_to_send[0]
            tick.animation.start()
            tick.closed.connect(self.tick_listener)

            tick.show()

            self.ticks_to_send.remove(tick)
            self.ticks.append(tick)

    def send_tick(self, level, message):
        """
        Send a tick with text

        :param level: OK, WARN, or ALERT
        :type level: str
        :param message: message to display
        :type message: str
        """

        tick = Tick()
        tick.create_tick(level, message)
        self.ticks_to_send.append(tick)

    def tick_listener(self, sender):
        """
        Listener who listen if tick is closed

        :param sender: the tick who emit closed signal
        :type sender: Tick
        """

        self.remove_tick(sender)

    def remove_tick(self, tick):
        """
        Close and remove a tick. Move leaving ticks
        :param tick: tick to remove
        :type tick: Tick
        """

        # Shift ticks when one is removed
        self.ticks.remove(tick)

        for old_tick in self.ticks:
            if (old_tick.pos().y() - tick.pos().y()) >= 50:
                pos = old_tick.pos()
                old_tick.move(pos.x(), pos.y() - old_tick.height())

        tick.close()


class Tick(QWidget):
    """
        Class who create a tick.
    """

    closed = pyqtSignal(QObject)

    def __init__(self, parent=None):
        super(Tick, self).__init__(parent)
        self.setFixedSize(400, 50)
        self.setWindowFlags(Qt.SplashScreen)
        # Animation
        self.animation = QPropertyAnimation(self, b'pos')
        # Color model
        self.color_levels = {
            'OK': {
                'color': '#27ae60',
                'title': 'INFO'
            },
            'WARN': {
                'color': '#e67e22',
                'title': 'WARN'
            },
            'ALERT': {
                'color': '#e74c3c',
                'title': 'ALERT'
            }
        }

    def create_tick(self, level, message):
        """
        Create tick QWidget and QPropertyAnimation

        :param level: OK, WARN, or ALERT defines color of tick
        :type level: str
        :param message: message to display in tick
        :type message: str
        """

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.setToolTip(message)

        try:
            color = self.color_levels[level]['color']
        except KeyError:
            color = 'black'

        self.setStyleSheet(
            """
            QWidget {
                background-color: %s;
                color: white;
                border: 1px solid #d2d2d2;
                font-size: 14px;
            }
            QToolTip {
                background-color: black;
                color: white;
            }
            """ % color)

        valid_btn = QPushButton()
        valid_btn.setMaximumSize(50, 50)
        valid_btn.setStyleSheet(
            """
                border: 1px solid #d2d2d2;
                border-radius: 0px;
            """
        )
        valid_btn.clicked.connect(self.close_tick)
        valid_btn.setIcon(QIcon(get_image_path('tick')))

        layout.addWidget(valid_btn)

        if len(message) > 76:
            message = message[:76] + '...'

        tick_msg = QLabel('<b>%s</b>: ' % self.color_levels[level]['title'] + message)
        tick_msg.setWordWrap(True)
        layout.addWidget(tick_msg)

        # Animation
        start_value = QPoint(0, 0)
        self.animation.setDuration(1000)
        self.animation.setStartValue(start_value)

        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        end_position = QApplication.desktop().screenGeometry(screen).topRight()
        end_value = QPoint(
            end_position.x() - self.width(),
            end_position.y()
        )
        self.animation.setEndValue(end_value)

    def close_tick(self):
        """
        Send signal to manager to close tick

        """

        self.closed.emit(self)

# Main instance of TickManager()
tickManager = TickManager()


def send_tick(level, message):
    """
    Direct access to send a tick

    :param level: OK, WARNING or CRITICAL defines color of tick
    :type level: str
    :param message: message to display in tick
    :type message: str
    """

    tickManager.send_tick(level, message)
