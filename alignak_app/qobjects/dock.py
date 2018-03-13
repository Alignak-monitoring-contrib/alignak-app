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
    Dock
    ++++
    Dock manage creation of QWidget for **Dock** (Right part)
"""

from PyQt5.Qt import QWidget, QGridLayout, QLabel, Qt

from alignak_app.qobjects.alignak.alignak import AlignakQWidget
from alignak_app.qobjects.events.events import get_events_widget
from alignak_app.qobjects.alignak.livestate import LivestateQWidget
from alignak_app.qobjects.events.spy import SpyQWidget


class DockQWidget(QWidget):
    """
        Class who create QWidgets for dock
    """

    def __init__(self, parent=None):
        super(DockQWidget, self).__init__(parent)
        # Fields
        self.status_widget = AlignakQWidget()
        self.livestate_widget = LivestateQWidget()
        self.spy_widget = SpyQWidget()

    def initialize(self):
        """
        Initialize dock QWidget

        """

        layout = QGridLayout()
        self.setLayout(layout)

        # Add Alignak status
        status = QLabel(_('Alignak'))
        status.setObjectName('itemtitle')
        layout.addWidget(status)
        layout.setAlignment(status, Qt.AlignCenter)
        self.status_widget.initialize()
        layout.addWidget(self.status_widget)

        # Livestate
        livestate = QLabel(_('Livestate'))
        livestate.setObjectName('itemtitle')
        layout.addWidget(livestate)
        layout.setAlignment(livestate, Qt.AlignCenter)
        self.livestate_widget.initialize()
        layout.addWidget(self.livestate_widget)

        # Last Events
        last_event_label = QLabel(_('Last Events'))
        last_event_label.setObjectName('itemtitle')
        layout.addWidget(last_event_label)
        layout.setAlignment(last_event_label, Qt.AlignCenter)
        layout.addWidget(get_events_widget())
