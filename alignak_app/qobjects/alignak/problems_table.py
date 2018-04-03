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
    Problems Table
    ++++++++++++++
    Problems Table manage creation of QTableView to display problems found in Alignak backend:

    * **Hosts**: ``DOWN``, ``UNREACHABLE``
    * **Services**: ``WARNING``, ``CRITICAL``, ``UNKNOWN``

"""

from logging import getLogger

from PyQt5.Qt import QIcon, QStandardItem, Qt, QAbstractItemView, QSize, QTableView
from PyQt5.Qt import QSortFilterProxyModel, QStandardItemModel

from alignak_app.backend.datamanager import data_manager
from alignak_app.utils.config import settings
from alignak_app.items.item import get_icon_name_from_state

logger = getLogger(__name__)


class ProblemsQTableView(QTableView):
    """
        Class who create Problems QTableView to display each problem
    """

    def __init__(self, parent=None):
        super(ProblemsQTableView, self).__init__(parent)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        self.setObjectName('problems')
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(40)
        self.setIconSize(QSize(24, 24))
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setMinimumHeight(40)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        # Fields
        self.headers_list = [
            _('Items in problem'), _('Output')
        ]

    def get_tableitem(self, item):
        """
        Return centered QTableWidgetItem with problem

        :param item: host or service item
        :type item: alignak_app.items.host.Host | alignak_app.items.service.Service
        :return: table item with text
        :rtype: QStandardItem
        """

        tableitem = QStandardItem(self.get_item_text(item))
        tableitem.setData(item, Qt.UserRole)

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
        :rtype: QStandardItem
        """

        if not item.data['ls_output']:
            item.data['ls_output'] = 'n\\a'
        tableitem = QStandardItem(item.data['ls_output'])
        tableitem.setData(item, Qt.UserRole)

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

        hostname = ''
        if 'host' in item.data:
            host = data_manager.get_item('host', '_id', item.data['host'])
            if host:
                hostname = host.get_display_name()
            service_name = item.get_display_name()
        else:
            hostname = item.get_display_name()
            service_name = ''

        if service_name:
            text = _('%s is %s (Attached to %s)') % (service_name, item.data['ls_state'], hostname)
        else:
            text = _('%s is %s') % (hostname, item.data['ls_state'])

        return text

    def update_view(self, problems_data):
        """
        Update QTableView model and proxy filter

        :param problems_data: problems found in database
        :type problems_data: dict
        :return: proxy filter to connect with line edit
        :rtype: QSortFilterProxyModel
        """

        problems_model = QStandardItemModel()
        problems_model.setRowCount(len(problems_data['problems']))
        problems_model.setColumnCount(len(self.headers_list))

        if problems_data['problems']:
            for row, item in enumerate(problems_data['problems']):
                problems_model.setItem(row, 0, self.get_tableitem(item))
                problems_model.setItem(row, 1, self.get_output_tableitem(item))

        else:
            tableitem = QStandardItem('No problem to report.')

            icon = QIcon(settings.get_image('checked'))
            tableitem.setIcon(icon)
            tableitem.setTextAlignment(Qt.AlignCenter)
            problems_model.setItem(0, 0, tableitem)

        proxy_filter = QSortFilterProxyModel()
        proxy_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        proxy_filter.setSourceModel(problems_model)

        problems_model.setHorizontalHeaderLabels(self.headers_list)

        self.setModel(proxy_filter)

        self.setColumnWidth(0, 500)
        self.setColumnWidth(1, 300)

        return proxy_filter
