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
from PyQt5.Qt import QAbstractItemView, QLabel, QHBoxLayout, QSize

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
            _('Items in problem'), _('Output')
        ]
        self.problems_title = QLabel()
        self.actions_widget = ActionsQWidget()
        self.spy_btn = QPushButton()
        self.spy_widget = None

    def initialize(self, spy_listwidget):
        """
        Initialize QWidget

        :param spy_listwidget: instance of SpyQListWidget to add spy events
        :type spy_listwidget: alignak_app.qobjects.events.spy.SpyQWidget
        """

        problem_layout = QVBoxLayout()
        self.setLayout(problem_layout)

        self.spy_widget = spy_listwidget
        self.spy_btn.setEnabled(False)

        self.actions_widget.initialize(None)
        self.actions_widget.acknowledge_btn.setEnabled(False)
        self.actions_widget.downtime_btn.setEnabled(False)

        problem_layout.addWidget(self.get_problems_widget_title())

        self.problem_table.setObjectName('problems')
        self.problem_table.verticalHeader().hide()
        self.problem_table.verticalHeader().setDefaultSectionSize(40)
        self.problem_table.setColumnCount(len(self.headers_list))
        self.problem_table.setColumnWidth(0, 500)
        self.problem_table.setColumnWidth(1, 300)
        self.problem_table.setSortingEnabled(True)
        self.problem_table.setIconSize(QSize(24, 24))
        self.problem_table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.problem_table.setHorizontalHeaderLabels(self.headers_list)
        self.problem_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.problem_table.horizontalHeader().setStretchLastSection(True)
        self.problem_table.horizontalHeader().setMinimumHeight(40)
        self.problem_table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.problem_table.currentItemChanged.connect(self.update_action_buttons)
        self.problem_table.setDragEnabled(True)
        problem_layout.addWidget(self.problem_table)

        self.update_problems_data()

    def update_action_buttons(self):
        """
        Update status of action buttons and set current item for ActionsQWidget

        """

        if self.problem_table.currentItem():
            # Get item
            item = self.problem_table.currentItem().item

            # If the elements had been ack or downtimed, they would not be present
            self.actions_widget.acknowledge_btn.setEnabled(True)
            self.actions_widget.downtime_btn.setEnabled(True)
            self.actions_widget.item = item

            if 'service' in item.item_type:
                host_id = item.data['host']
            else:
                host_id = item.item_id
            self.spy_btn.setEnabled(
                bool(host_id not in self.spy_widget.spy_list_widget.spied_hosts)
            )

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

        layout_title.addWidget(self.get_spy_widget())
        layout_title.addWidget(self.actions_widget)

        refresh_btn = QPushButton(_('Refresh'))
        refresh_btn.setObjectName('ok')
        refresh_btn.setFixedSize(120, 30)
        refresh_btn.clicked.connect(self.update_problems_data)
        layout_title.addWidget(refresh_btn)

        return widget_title

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
            text = '%s is %s (Attached to %s)' % (service_name, item.data['ls_state'], hostname)
        else:
            text = '%s is %s' % (hostname, item.data['ls_state'])

        return text

    def get_spy_widget(self):
        """
        Return QWidget with spy QPushButton

        :return: widget with spy button
        :rtype: QWidget
        """

        widget_btn = QWidget()
        layout_btn = QVBoxLayout()
        widget_btn.setLayout(layout_btn)

        self.spy_btn.setIcon(QIcon(settings.get_image('spy')))
        self.spy_btn.setFixedSize(80, 20)
        self.spy_btn.clicked.connect(self.add_spied_host)

        layout_btn.addWidget(self.spy_btn)
        layout_btn.setAlignment(self.spy_btn, Qt.AlignCenter)

        return widget_btn

    def add_spied_host(self):
        """
        Add a host to spied hosts

        """

        if self.problem_table.currentItem():
            item = self.problem_table.currentItem().item
            if 'service' in item.item_type:
                item_id = self.problem_table.currentItem().item.data['host']
            else:
                item_id = self.problem_table.currentItem().item.item_id

            self.spy_widget.spy_list_widget.add_spy_host(item_id)
            self.spy_widget.update_parent_spytab()

        self.update_action_buttons()

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
            self.problem_table.setItem(row, 0, self.get_tableitem(item))
            self.problem_table.setItem(row, 1, self.get_output_tableitem(item))
            row += 1


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
