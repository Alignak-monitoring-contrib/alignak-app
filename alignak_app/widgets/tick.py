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

from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton, QLabel
from PyQt5.Qt import Qt, QIcon, QRect, QPoint, QSize
from PyQt5.QtCore import QPropertyAnimation


OK = '#27ae60'
WARNING = '#e67e22'
CRITICAL = '#e74c3c'


class TickManager(object):
    """
    TODO
    """

    def __init__(self):
        self.ticks = []

    def send(self, color, text):
        """
        TODO
        :return:
        """

        tick = Tick()
        tick.create_tick(color, text)

        self.ticks.append(tick)


class Tick(QWidget):
    """
    TODO
    """

    def __init__(self, parent=None):
        super(Tick, self).__init__(parent)
        self.setMinimumSize(400, 50)
        self.setWindowFlags(Qt.SplashScreen)
        self.animation = QPropertyAnimation(self, b'geometry')

    def create_tick(self, color, text):
        """
        TODO
        :return:
        """

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
        valid_btn.clicked.connect(self.close)
        valid_btn.setIcon(QIcon('../../etc/images/tick.svg'))

        layout.addWidget(valid_btn)

        ticker_txt = QLabel(text)
        layout.addWidget(ticker_txt)

        self.show()

        # Animation
        start_value = QRect(0, 0, self.width(), self.height())
        self.animation.setStartValue(start_value)

        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        end_position = QApplication.desktop().screenGeometry(screen).topRight()
        end_value = QRect(
            end_position.x() - self.width(),
            end_position.y(),
            self.width(),
            self.height()
        )
        self.animation.setEndValue(end_value)
        self.animation.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    tick_manager = TickManager()

    tick_manager.send(OK, 'All daemons are alive.')
    tick_manager.send(WARNING, 'Some daemons are not alive !')
    tick_manager.send(CRITICAL, 'All daemons are down !')

    sys.exit(app.exec_())