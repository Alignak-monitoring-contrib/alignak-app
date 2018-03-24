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

from PyQt5.Qt import QTimer, QListWidgetItem, QIcon, Qt

from alignak_app.utils.config import settings
from alignak_app.utils.time import get_current_time


class EventItem(QListWidgetItem):
    """
        Class who create an event QListWidgetItem
    """

    def __init__(self):
        super(EventItem, self).__init__()
        self.timer = None
        self.host = None

    def initialize(self, event_type, msg, timer=False, host=None):
        """
        Initialize QListWidgetItem

        :param event_type: the type of event: OK, DOWN, ACK, ...
        :type event_type: str
        :param msg: message of event
        :type msg: str
        :param timer: timer to hide event at end of time
        :type timer: bool
        :param host: _id of host. Only necessary if "be_spied" is True
        :type host: None | str
        """

        self.host = host
        if host:
            self.setData(Qt.UserRole, host)

        if timer:
            self.timer = QTimer()

        self.setData(Qt.DisplayRole, "%s" % msg)
        msg_to_send = '%s. (Send at %s)' % (msg, get_current_time())
        self.setToolTip(msg_to_send)

        self.setData(
            Qt.DecorationRole, QIcon(settings.get_image(self.get_icon(event_type)))
        )

    def close_item(self):  # pragma: no cover
        """
        Hide items when timer is finished

        """

        self.setHidden(True)

    @staticmethod
    def get_icon(event_type):
        """
        Return name of icon event

        :param event_type: type of event
        :type event_type: str
        :return: name of icon
        :rtype: str
        """

        available_icons = {
            'event_ok': ['OK', 'UP'],
            'event_info': ['UNKNOWN', 'INFO', 'TODO'],
            'event_warn': ['WARNING', 'UNREACHABLE', 'WARN'],
            'event_alert': ['DOWN', 'CRITICAL', 'ALERT'],
            'acknowledge': ['ACK'],
            'downtime': ['DOWNTIME', 'DOWNTIMESTART (DOWN)'],
            'spy': ['SPY']
        }

        for key, _ in available_icons.items():
            if event_type in available_icons[key]:
                return key

        return 'error'

    @staticmethod
    def get_event_type(data):
        """
        Return event type depending of data content

        :param data: data of backend item
        :type data: dict
        :return: event type for item
        :rtype: str
        """

        event_type = ''
        if data['ls_acknowledged']:
            event_type = 'ACK'
        if data['ls_downtimed']:
            event_type = 'DOWNTIME'

        if not event_type:
            event_type = data['ls_state']

        return event_type
