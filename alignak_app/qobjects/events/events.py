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
    Events
    ++++++
    Events manage creation of QWidget for events
"""

from logging import getLogger

from PyQt5.Qt import QWidget, QAbstractItemView, QListWidget, QTimer, QSize, QVBoxLayout, Qt

from alignak_app.backend.datamanager import data_manager
from alignak_app.utils.config import settings
from alignak_app.utils.time import get_current_time

from alignak_app.qobjects.events.item import EventItem

logger = getLogger(__name__)


class EventsQWidget(QWidget):
    """
        Class who create QWidget for events
    """

    def __init__(self):
        super(EventsQWidget, self).__init__()
        self.setObjectName('events')
        # Fields
        self.events_list = QListWidget()
        self.timer = QTimer()

    def initialize(self):
        """
        Intialize QWidget

        """

        self.timer.setInterval(30000)
        self.timer.start()
        self.timer.timeout.connect(self.send_datamanager_events)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.events_list.setDragDropMode(QAbstractItemView.DragOnly)
        self.events_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.events_list.setDropIndicatorShown(True)
        self.events_list.doubleClicked.connect(self.remove_event)
        self.events_list.setWordWrap(True)
        self.events_list.setIconSize(QSize(16, 16))

        self.add_event(
            'OK',
            _('Welcome %s, you are connected to Alignak Backend') %
            data_manager.database['user'].name,
            timer=True
        )

        layout.addWidget(self.events_list)

    def send_datamanager_events(self):
        """
        Add events stored in DataManager

        """

        events = data_manager.get_events()

        if events:
            for event in events:
                self.add_event(
                    event['event_type'],
                    event['message'],
                    timer=False,
                    spied_on=True,
                    host=event['host']
                )

    # pylint: disable=too-many-arguments
    def add_event(self, event_type, msg, timer=False, spied_on=False, host=None):
        """
        Add event to events list

        :param event_type: the type of event: OK, DOWN, ACK, ...
        :type event_type: str
        :param msg: message of event
        :type msg: str
        :param timer: timer to hide event at end of time
        :param spied_on: make event spy able
        :type spied_on: bool
        :param host: data of host. Only necessary if "be_spied" is True
        :type host: None | str
        """

        if not self.event_exist(msg):
            logger.debug(
                'Add Event: msg: %s, timer: %s, spied_on: %s, host: %s', msg, timer, spied_on, host
            )
            event = EventItem()
            event.initialize(event_type, msg, timer=timer, spied_on=spied_on, host=host)

            self.events_list.insertItem(0, event)
            if timer:
                event_duration = int(
                    settings.get_config('Alignak-app', 'notification_duration')
                ) * 1000
                QTimer.singleShot(
                    event_duration,
                    lambda: self.remove_timer_event(event)
                )
        else:
            logger.debug(
                'Event with msg: %s already exist.', msg
            )

    def event_exist(self, msg):
        """
        Check if event already displayed, move it to top and update tooltip.
        Only for EventItem who are spied on.

        :param msg: message of event
        :type msg: str
        :return: if message exist or not in events QWidgetList
        :rtype: bool
        """

        for i in range(0, self.events_list.count()):
            if self.events_list.item(i).data(Qt.DisplayRole) == msg:
                if self.events_list.item(i).spied_on:
                    item = self.events_list.takeItem(i)
                    msg_to_send = '%s. (Send at %s)' % (msg, get_current_time())
                    item.setToolTip(msg_to_send)
                    self.events_list.insertItem(0, item)
                    return True

        return False

    def remove_timer_event(self, event):
        """
        Remove EventItem with timer

        :param event: EventItem with timer
        :type event: EventItem
        """

        logger.debug('Remove Timer Event: %s', event.text())
        self.events_list.takeItem(self.events_list.row(event))

    def remove_event(self, item=None):
        """
        Remove item when user double click on an item

        :param item: item to remove, else remove the current row
        :type item: EventItem
        """

        if isinstance(item, EventItem):
            row = self.events_list.row(item)
            self.events_list.takeItem(row)
        else:
            item = self.events_list.takeItem(self.events_list.currentRow())

        logger.debug('Remove Event: %s', item.text())


events_widget = None


def init_event_widget():
    """
    Initialize the global EventsQWidget. Used for drag & drop and send events

    """

    global events_widget  # pylint: disable=global-statement

    events_widget = EventsQWidget()
    events_widget.initialize()


def get_events_widget():
    """
    Return EventsQWidget instance

    :return: EventsQWidget instance
    :rtype: alignak_app.qobjects.events.events.EventsQWidget
    """

    return events_widget


def send_event(event_type, msg, timer=False, spied_on=False, host=None):
    """
    Add event to Events QWidget (access function to make event sendable in whole application. Event
    type define icon and color of :class:`EventItem <alignak_app.qobjects.events.item.EventItem>`.

    * **green**: [``OK``, ``UP``]
    * **blue**: [``UNKNOWN``, ``INFO``, ``SPY``]
    * **orange**: [``WARNING``, ``UNREACHABLE``, ``WARN``]
    * **red'**: [``DOWN``, ``CRITICAL``, ``ALERT``]
    * **yellow**: [``ACK``]
    * **yellow**: [``DOWNTIME``]

    :param event_type: type of event to send
    :type event_type: str
    :param msg: message of event
    :type msg: str
    :param timer: timer to hide event at end of time
    :param spied_on: make event spy able
    :type spied_on: bool
    :param host: _id of host. Only necessary if "spied_on" is True
    :type host: None | str
    """

    events_widget.add_event(event_type, msg, timer=timer, spied_on=spied_on, host=host)
