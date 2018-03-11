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

from PyQt5.Qt import QWidget, QIcon, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, Qt
from PyQt5.Qt import QAbstractItemView, QPixmap, QLabel, QHBoxLayout

from alignak_app.backend.datamanager import data_manager
from alignak_app.utils.config import settings
from alignak_app.items.item import get_icon_name_from_state

from alignak_app.qobjects.common.actions import ActionsQWidget

logger = getLogger(__name__)


class ProblemsQWidget(QWidget):
    """
        Class who create Problems QWidget
    """

    def __init__(self, parent=None):
        super(ProblemsQWidget, self).__init__(parent)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        # Fields
        self.problem_table = QTableWidget()
        self.headers_list = [
            _('Item Type'), '', _('Host'), _('Service'), _('State'), _('Actions'), _('Output')
        ]
        self.problems_title = QLabel()
        self.layout = QVBoxLayout()
        self.spy_widget = None

    def initialize(self, spy_listwidget):
        """
        Initialize QWidget

        :param spy_listwidget: instance of SpyQListWidget to add spy events
        :type spy_listwidget: alignak_app.qobjects.events.spy.SpyQWidget
        """

        self.setLayout(self.layout)
        self.spy_widget = spy_listwidget

        self.layout.addWidget(self.get_problems_widget_title())

        self.problem_table.setObjectName('problems')
        self.problem_table.verticalHeader().hide()
        self.problem_table.verticalHeader().setDefaultSectionSize(40)
        self.problem_table.setColumnCount(len(self.headers_list))
        self.problem_table.setColumnWidth(1, 32)
        self.problem_table.setColumnWidth(2, 150)
        self.problem_table.setColumnWidth(3, 150)
        self.problem_table.setColumnWidth(4, 150)
        self.problem_table.setColumnWidth(5, 180)
        self.problem_table.setColumnWidth(6, 600)
        self.problem_table.setSortingEnabled(True)
        self.problem_table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.problem_table.setHorizontalHeaderLabels(self.headers_list)
        self.problem_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.problem_table.horizontalHeader().setStretchLastSection(True)
        self.problem_table.horizontalHeader().setMinimumHeight(30)
        self.problem_table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.problem_table)

        self.update_problems_data()

    def get_problems_widget_title(self):
        """
        Return QWidget title with number of problems and refresh QPushButton

        :return: QWidget with number of problems
        :rtype: QWidget
        """

        widget_title = QWidget()
        layout_title = QHBoxLayout()
        widget_title.setLayout(layout_title)

        self.problems_title.setObjectName('itemtitle')
        layout_title.addWidget(self.problems_title)

        refresh_btn = QPushButton(_('Refresh'))
        refresh_btn.setObjectName('ok')
        refresh_btn.setFixedSize(120, 30)
        refresh_btn.clicked.connect(self.update_problems_data)
        layout_title.addWidget(refresh_btn)

        return widget_title

    @staticmethod
    def get_icon_widget(item):
        """
        Return QWidget with corresponding icon to item state

        :param item: host or service item
        :type item: alignak_app.items.item.Item
        :return: QWidget with corresponding icon
        :rtype: QWidget
        """

        widget_icon = QWidget()
        layout_icon = QVBoxLayout()
        widget_icon.setLayout(layout_icon)

        icon_label = QLabel()
        icon = QPixmap(settings.get_image(
            get_icon_name_from_state(item.item_type, item.data['ls_state'])
        ))
        icon_label.setPixmap(icon)
        icon_label.setFixedSize(18, 18)
        icon_label.setScaledContents(True)

        layout_icon.addWidget(icon_label)
        layout_icon.setAlignment(icon_label, Qt.AlignCenter)

        return widget_icon

    def get_btn_widget(self, item):
        """
        Return QWidget with spy QPushButton

        :param item: host or service item
        :type item: alignak_app.items.item.Item
        :return: widget with spy button
        :rtype: QWidget
        """

        widget_btn = QWidget()
        layout_btn = QVBoxLayout()
        widget_btn.setLayout(layout_btn)

        spy_btn = QPushButton()
        spy_btn.setIcon(QIcon(settings.get_image('spy')))
        spy_btn.setObjectName('ok')
        spy_btn.setFixedSize(20, 20)
        item_id = item.data['host'] if item.item_type == 'service' else item.item_id
        spy_btn.clicked.connect(
            lambda: self.add_spied_host(item_id)
        )

        layout_btn.addWidget(spy_btn)
        layout_btn.setAlignment(spy_btn, Qt.AlignCenter)

        return widget_btn

    @staticmethod
    def get_tableitem(text):
        """
        Return centered QTableWidgetItem

        :param text: text to display in table item
        :type text: str
        :return: table item with text
        :rtype: QTableWidgetItem
        """

        tableitem = QTableWidgetItem(text)
        tableitem.setTextAlignment(Qt.AlignCenter)

        return tableitem

    @staticmethod
    def get_host_tableitem(item):
        """
        Return host QTableWidgetItem

        :param item: host or service item
        :type item: alignak_app.items.host.Host | alignak_app.items.service.Service
        :return: the table item with item name
        :rtype: QTableWidgetItem
        """

        if 'host' in item.data:
            hostname = data_manager.get_item('host', '_id', item.data['host']).get_display_name()
            host_tableitem = QTableWidgetItem(hostname)
        else:
            host_tableitem = QTableWidgetItem(item.get_display_name())

        host_tableitem.setTextAlignment(Qt.AlignCenter)

        return host_tableitem

    @staticmethod
    def get_service_tableitem(item):
        """
        Return service QTableWidgetItem

        :param item: host or service item
        :type item: alignak_app.items.host.Host | alignak_app.items.service.Service
        :return: the table item with item name
        :rtype: QTableWidgetItem
        """

        if 'host' in item.data:
            service_tableitem = QTableWidgetItem(item.get_display_name())
        else:
            service_tableitem = QTableWidgetItem('')

        service_tableitem.setTextAlignment(Qt.AlignCenter)

        return service_tableitem

    @staticmethod
    def get_action_widget(item):
        """
        Return Actions QWidget

        :param item: host or service item
        :type item: alignak_app.items.item.Item
        :return: actions QWidget
        :rtype: ActionsQWidget
        """

        actions_widget = ActionsQWidget()
        actions_widget.initialize(item)

        return actions_widget

    def add_spied_host(self, item_id):
        """
        Add a host to spied hosts

        :param item_id: id of host to spy
        :type item_id: str
        """

        self.spy_widget.spy_list_widget.add_spy_host(item_id)
        self.spy_widget.update_parent_spytab()

    def update_problems_data(self):
        """
        Update data of QTableWidget and problems title

        """

        problems_data = data_manager.get_problems()

        self.problems_title.setText(
            _('There are %d problems to manage (hosts: %d, services: %d)') % (
                len(problems_data['problems']),
                problems_data['hosts_nb'],
                problems_data['services_nb']
            )
        )
        self.problem_table.setRowCount(len(problems_data['problems']))

        row = 0
        for item in problems_data['problems']:
            self.problem_table.setCellWidget(row, 0, self.get_icon_widget(item))
            self.problem_table.setCellWidget(row, 1, self.get_btn_widget(item))
            self.problem_table.setItem(row, 2, self.get_host_tableitem(item))
            self.problem_table.setItem(row, 3, self.get_service_tableitem(item))
            self.problem_table.setItem(row, 4, self.get_tableitem(item.data['ls_state']))
            self.problem_table.setCellWidget(row, 5, self.get_action_widget(item))
            self.problem_table.setItem(row, 6, self.get_tableitem(item.data['ls_output']))
            row += 1
