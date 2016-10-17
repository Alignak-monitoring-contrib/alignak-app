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

# TODO : update doc
"""
    TODO
"""

import threading
from logging import getLogger
from PyQt5.QtWidgets import QSystemTrayIcon
from PyQt5.QtCore import QTimer

logger = getLogger(__name__)


class AppNotifier(QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.thread()

    def send_notification(self, title, msg):
        self.show()
        final_title = 'Alignak-app : ' + title
        self.showMessage(final_title, msg, QSystemTrayIcon.Warning)
        self.hide()

    def say_hello(self):
        print('Hello')
        self.send_notification('Msg', 'Hello')

    def start_process(self):
        timer = QTimer(self)
        timer.start(30000)
        timer.timeout.connect(self.say_hello)
