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
    TODO
"""

import sys

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QHBoxLayout, QApplication  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QPushButton, QLabel  # pylint: disable=no-name-in-module
    from PyQt5.Qt import Qt, QIcon, QTimer, QPoint  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import QPropertyAnimation  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QHBoxLayout, QApplication  # pylint: disable=import-error
    from PyQt4.Qt import QWidget, QPushButton, QLabel  # pylint: disable=import-error
    from PyQt4.QtCore import Qt, QIcon, QTimer, QPoint  # pylint: disable=import-error
    from PyQt4.QtCore import QPropertyAnimation  # pylint: disable=import-error


OK = '#27ae60'
WARNING = '#e67e22'
CRITICAL = '#e74c3c'


class TickManager(object):
    """
    TODO
    """

    def __init__(self):
        self.ticks = []
        self.timer = None

    def send(self, color, text):
        """
        TODO
        :return:
        """

        tick = Tick()
        tick.create_tick(color, text, ticks=self.ticks)

        self.ticks.append(tick)

    def test_process(self):
        """
        TEST
        """
        print("timer")
        self.timer = QTimer()
        self.timer.start(5000)
        self.timer.timeout.connect(self.test_tick)

    def test_tick(self):
        """
        TEST
        """
        print('send tick')
        self.send(OK, 'All daemons are Alive !')


class Tick(QWidget):
    """
    TODO
    """

    def __init__(self, parent=None):
        super(Tick, self).__init__(parent)
        self.setMinimumSize(400, 50)
        self.setWindowFlags(Qt.SplashScreen)
        self.animation = QPropertyAnimation(self, b'pos')
        self.ticks = None

    def create_tick(self, color, text, ticks):
        """
        TODO
        :return:
        """

        self.ticks = ticks

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.setStyleSheet(
            """
                background-color: %s;
                color: white;
                border: 1px solid #d2d2d2;
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
        valid_btn.setIcon(QIcon('../../etc/images/tick.svg'))

        layout.addWidget(valid_btn)

        ticker_txt = QLabel(text)
        layout.addWidget(ticker_txt)

        self.show()

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
        self.animation.start()

        for tick in self.ticks:
            pos = tick.pos()
            tick.move(pos.x(), pos.y() + tick.height())

    def close_tick(self):
        """
        TODO
        :return:
        """

        self.ticks.remove(self)
        old_tick = self
        for tick in self.ticks:
            if (tick.pos().y() - old_tick.pos().y()) >= 50:
                pos = tick.pos()
                tick.move(pos.x(), pos.y() - tick.height())
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    tick_manager = TickManager()
    tick_manager.test_process()

    sys.exit(app.exec_())
