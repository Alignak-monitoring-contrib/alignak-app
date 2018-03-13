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
    Problems
    ++++++++
    Problems manage creation of QWidget to display problems found in Alignak backend:

    * **Hosts**: ``DOWN``
    * **Services**: ``WARNING``, ``CRITICAL``, ``UNKNOWN``

"""

from logging import getLogger

from PyQt5.Qt import QIcon, QTableWidget, QTableWidgetItem, Qt, QAbstractItemView, QSize

from alignak_app.backend.datamanager import data_manager
from alignak_app.utils.config import settings
from alignak_app.items.item import get_icon_name_from_state

logger = getLogger(__name__)


class ProblemsQTableWidget(QTableWidget):
    """
        Class who create Problems QTableWidget to display each problem
    """

    def __init__(self, parent=None):
        super(ProblemsQTableWidget, self).__init__(parent)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        # Fields
        self.headers_list = [
            _('Items in problem'), _('Output')
        ]

    def initialize(self):
        """
        Initialize Problems QTableWidget cells, rows

        """

        self.setObjectName('problems')
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(40)
        self.setColumnCount(len(self.headers_list))
        self.setColumnWidth(0, 500)
        self.setColumnWidth(1, 300)
        self.setSortingEnabled(True)
        self.setIconSize(QSize(24, 24))
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalHeaderLabels(self.headers_list)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setMinimumHeight(40)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.setDragEnabled(True)

    def get_tableitem(self, item):
        """
        Return centered QTableWidgetItem with problem

        :param item: host or service item
        :type item: alignak_app.items.host.Host | alignak_app.items.service.Service
        :return: table item with text
        :rtype: QTableWidgetItem
        """

        tableitem = AppQTableWidgetItem(self.get_item_text(item))
        tableitem.add_backend_item(item)

        icon = QIcon(settings.get_image(
            get_icon_name_from_state(item.item_type, item.data['ls_state'])
        ))
        tableitem.setIcon(icon)
        tableitem.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        return tableitem

    @staticmethod
    def get_output_tableitem(item):
        """
        Return centered QTableWidgetItem with output

        :param item: host or service item
        :type item: alignak_app.items.host.Host | alignak_app.items.service.Service
        :return: table item with text
        :rtype: QTableWidgetItem
        """

        if not item.data['ls_output']:
            item.data['ls_output'] = 'n\\a'
        tableitem = AppQTableWidgetItem(item.data['ls_output'])
        tableitem.add_backend_item(item)

        tableitem.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        return tableitem

    @staticmethod
    def get_item_text(item):
        """
        Return item text depends if it's a host or service

        :param item: host or service item
        :type item: alignak_app.items.host.Host | alignak_app.items.service.Service
        :return: text of item
        :rtype: str
        """

        if 'host' in item.data:
            hostname = data_manager.get_item('host', '_id', item.data['host']).get_display_name()
            service_name = item.get_display_name()
        else:
            hostname = item.get_display_name()
            service_name = ''

        if service_name:
            text = _('%s is %s (Attached to %s)') % (service_name, item.data['ls_state'], hostname)
        else:
            text = _('%s is %s') % (hostname, item.data['ls_state'])

        return text


class AppQTableWidgetItem(QTableWidgetItem):  # pylint: disable=too-few-public-methods
    """
        Class who create QTableWidgetItem for App, with an item field
    """

    def __init__(self, parent=None):
        super(AppQTableWidgetItem, self).__init__(parent)
        self.item = None

    def add_backend_item(self, item):
        """
        Add backend item

        :param item: host or service item
        :type item: alignak_app.items.host.Host | alignak_app.items.service.Service
        """

        self.item = item
