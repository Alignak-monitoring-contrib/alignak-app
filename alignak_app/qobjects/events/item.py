#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2018:
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
    Event Item
    ++++++++++
    Event item manage creation of ``QListWidgetItem`` for events
"""

import time

from PyQt5.Qt import QTimer, QColor, QListWidgetItem


class EventItem(QListWidgetItem):
    """
        Class who create an event QListWidgetItem
    """

    def __init__(self):
        super(EventItem, self).__init__()
        self.timer = None
        self.spied_on = False
        self.host = None

    # pylint: disable=too-many-arguments
    def initialize(self, event_type, msg, timer=False, spied_on=False, host=None):
        """
        Initialize QListWidgetItem

        :param event_type: the type of event: OK, DOWN, ACK, ...
        :type event_type: str
        :param msg: message of event
        :type msg: str
        :param timer: timer to hide event at end of time
        :param spied_on: make event spy able
        :type spied_on: bool
        :param host: _id of host. Only necessary if "be_spied" is True
        :type host: str
        """

        self.spied_on = spied_on
        self.host = host

        if timer:
            self.timer = QTimer()

        self.setText("%s" % msg)
        send_at = time.strftime("%a, %d %b %Y %H:%M:%S")
        msg_to_send = '%s. (Send at %s)' % (msg, send_at)
        self.setToolTip(msg_to_send)

        self.setForeground(QColor(self.get_foreground_color(event_type)))

    def close_item(self):
        """
        Hide items when timer is finished

        """

        self.setHidden(True)

    @staticmethod
    def get_foreground_color(event_type):
        """
        Return corresponding color of event type

        :param event_type: the type of event
        :type event_type: str
        :return: the associated color with the event
        :rtype: str
        """

        available_colors = {
            '#27ae60': ['OK', 'UP'],
            '#2980b9': ['UNKNOWN', 'INFO'],
            '#e67e22': ['WARNING', 'UNREACHABLE', 'WARN'],
            '#e74c3c': ['DOWN', 'CRITICAL', 'ALERT'],
            '#f39c12': ['ACK'],
            '#f1c40f': ['DOWNTIME', 'DOWNTIMESTART (DOWN)'],
            '#fd9205': ['TODO']
        }

        for key, _ in available_colors.items():
            if event_type in available_colors[key]:
                return key

        return '#e74c3c'