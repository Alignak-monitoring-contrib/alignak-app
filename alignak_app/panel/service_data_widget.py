#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2017:
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

from logging import getLogger

from alignak_app.core.utils import get_image_path, get_css
from alignak_app.core.utils import get_time_diff_since_last_timestamp
from alignak_app.core.data_manager import data_manager
from alignak_app.models.item_model import get_icon_item, get_real_host_state_icon
from alignak_app.panel.actions import AckQDialog, DownQDialog, QDialog
from alignak_app.dock.events_widget import events_widget

from PyQt5.Qt import QLabel, QWidget, QIcon, Qt  # pylint: disable=no-name-in-module
from PyQt5.Qt import QPixmap, QVBoxLayout, QGridLayout  # pylint: disable=no-name-in-module
from PyQt5.Qt import QTreeWidget, QTreeWidgetItem  # pylint: disable=no-name-in-module

logger = getLogger(__name__)


class ServiceDataQWidget(QWidget):
    """
        TODO
    """

    def __init__(self, parent=None):
        super(ServiceDataQWidget, self).__init__(parent)
        self.setStyleSheet(get_css())
        # Fields
        self.labels = {
            'name': QLabel()
        }

    def initialize(self):
        """
        TODO
        :return:
        """

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(self.labels['name'])

    def update_widget(self, name):
        """
        TODO
        :return:
        """

        self.labels['name'].setText('Service name: %s' % name)
