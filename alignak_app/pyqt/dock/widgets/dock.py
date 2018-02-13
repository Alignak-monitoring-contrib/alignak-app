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
    Dock manage creation of Alignak-app Dock
"""

from PyQt5.Qt import QWidget, QGridLayout, QLabel, Qt, QTimer

from alignak_app.core.backend.data_manager import data_manager
from alignak_app.core.models.item import get_host_msg_and_event_type
from alignak_app.core.utils.config import settings

from alignak_app.pyqt.common.frames import get_frame_separator
from alignak_app.pyqt.dock.widgets.status import StatusQWidget
from alignak_app.pyqt.dock.widgets.buttons import ButtonsQWidget
from alignak_app.pyqt.dock.widgets.events import get_events_widget
from alignak_app.pyqt.dock.widgets.livestate import LivestateQWidget
from alignak_app.pyqt.dock.widgets.spy import SpyQWidget


class DockQWidget(QWidget):
    """
        Class who create QWidgets for dock
    """

    def __init__(self, parent=None):
        super(DockQWidget, self).__init__(parent)
        # Fields
        self.status_widget = StatusQWidget()
        self.buttons_widget = ButtonsQWidget()
        self.livestate_widget = LivestateQWidget()
        self.spy_widget = SpyQWidget()
        self.spy_timer = QTimer()
        self.spied_hosts = []

    def initialize(self):
        """
        Initialize dock QWidget

        """

        layout = QGridLayout()
        self.setLayout(layout)

        spy_interval = int(settings.get_config('Alignak-app', 'spy_interval')) * 1000
        self.spy_timer.setInterval(spy_interval)
        self.spy_timer.start()
        self.spy_timer.timeout.connect(self.send_spy_events)

        # Add Alignak status
        status = QLabel(_('Alignak'))
        status.setObjectName('title')
        layout.addWidget(status)
        layout.setAlignment(status, Qt.AlignCenter)
        layout.addWidget(get_frame_separator())
        self.status_widget.initialize()
        layout.addWidget(self.status_widget)

        self.buttons_widget.initialize()
        layout.addWidget(self.buttons_widget)

        # Livestate
        livestate = QLabel(_('Livestate'))
        livestate.setObjectName('title')
        layout.addWidget(livestate)
        layout.setAlignment(livestate, Qt.AlignCenter)
        layout.addWidget(get_frame_separator())
        self.livestate_widget.initialize()
        layout.addWidget(self.livestate_widget)

        # Last Events
        last_event_label = QLabel(_('Last Events'))
        last_event_label.setObjectName('title')
        layout.addWidget(last_event_label)
        layout.setAlignment(last_event_label, Qt.AlignCenter)
        layout.addWidget(get_frame_separator())
        layout.addWidget(get_events_widget())

        # Spieds hosts
        spy_title = QLabel(_('Spied Hosts'))
        spy_title.setObjectName('title')
        layout.addWidget(spy_title)
        layout.setAlignment(spy_title, Qt.AlignCenter)
        layout.addWidget(get_frame_separator())
        self.spy_widget.initialize()
        layout.addWidget(self.spy_widget)

        self.spy_widget.spy_list_widget.item_dropped.connect(get_events_widget().remove_event)

    def send_spy_events(self):
        """
        Send event for one host spied

        """

        if not self.spied_hosts:
            # Reversed the list to have the host first spied on
            self.spied_hosts = list(reversed(self.spy_widget.spy_list_widget.spied_hosts))

        if self.spied_hosts:
            host_id = self.spied_hosts.pop()
            host_and_services = data_manager.get_host_with_services(host_id)

            msg_and_event_type = get_host_msg_and_event_type(host_and_services)

            get_events_widget().add_event(
                'TODO',
                msg_and_event_type['message'],
                timer=False,
                spied_on=True,
                host=host_and_services['host'].item_id
            )
