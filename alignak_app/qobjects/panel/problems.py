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
        self.problem_widget = QTableWidget()
        self.headers_list = [
            _('Item Type'), _('Host'), _('Service'), _('State'), _('Actions'), _('Output')
        ]
        self.problems_title = QLabel()
        self.layout = QVBoxLayout()

    def initialize(self):
        """
        Initialize QWidget

        """

        self.setLayout(self.layout)

        self.layout.addWidget(self.get_problems_widget_title())

        self.problem_widget.verticalHeader().hide()
        self.problem_widget.verticalHeader().setDefaultSectionSize(40)
        self.problem_widget.setColumnCount(len(self.headers_list))
        self.problem_widget.setColumnWidth(1, 150)
        self.problem_widget.setColumnWidth(2, 150)
        self.problem_widget.setColumnWidth(3, 150)
        self.problem_widget.setColumnWidth(4, 180)
        self.problem_widget.setColumnWidth(5, 600)
        self.problem_widget.setSortingEnabled(True)
        self.problem_widget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.problem_widget.setHorizontalHeaderLabels(self.headers_list)
        self.problem_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.problem_widget.horizontalHeader().setStretchLastSection(True)
        self.problem_widget.horizontalHeader().setHighlightSections(False)
        self.layout.addWidget(self.problem_widget)

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

    # noinspection PyListCreation
    def get_table_items_problem(self, item):
        """
        Return list of QWidgets and QTableWidgetItem

        :param item: ItemModel instance with its data
        :type item: alignak_app.core.models.host.Host | alignak_app.core.models.service.Service
        :return: list of QWidgets and QTableWidgetItem
        :rtype: list
        """

        table_items = []

        # Icon
        table_items.append(self.get_icon_widget(item.item_type, item.data['ls_state']))

        # Host and Service
        if 'host' in item.data:
            hostname = data_manager.get_item('host', '_id', item.data['host']).get_display_name()
            item_table_host = QTableWidgetItem(hostname)
            item_table_service = QTableWidgetItem(item.get_display_name())
        else:
            item_table_host = QTableWidgetItem(item.get_display_name())
            item_table_service = QTableWidgetItem('')
        item_table_host.setTextAlignment(Qt.AlignCenter)
        item_table_service.setTextAlignment(Qt.AlignCenter)
        table_items.append(item_table_host)
        table_items.append(item_table_service)

        # State
        item_table_state = QTableWidgetItem(item.data['ls_state'])
        item_table_state.setTextAlignment(Qt.AlignCenter)
        table_items.append(item_table_state)

        # Actions
        actions_widget = ActionsQWidget()
        actions_widget.initialize(item)
        table_items.append(actions_widget)

        # Output
        item_table_output = QTableWidgetItem(item.data['ls_output'])
        item_table_output.setTextAlignment(Qt.AlignCenter)
        table_items.append(item_table_output)

        return table_items

    @staticmethod
    def get_icon_widget(item_type, state):
        """
        Return QWidget with corresponding icon to item state

        :param item_type: type of item: host | service
        :type item_type: str
        :param state: state of item
        :type state: str
        :return: QWidget with corresponding icon
        :rtype: QWidget
        """

        widget_icon = QWidget()
        layout_icon = QVBoxLayout()
        widget_icon.setLayout(layout_icon)

        icon_label = QLabel()
        icon = QPixmap(settings.get_image(get_icon_name_from_state(item_type, state)))
        icon_label.setPixmap(icon)
        icon_label.setFixedSize(18, 18)
        icon_label.setScaledContents(True)

        layout_icon.addWidget(icon_label)
        layout_icon.setAlignment(icon_label, Qt.AlignCenter)

        return widget_icon

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
        self.problem_widget.setRowCount(len(problems_data['problems']))

        row = 0
        for item in problems_data['problems']:
            table_items = self.get_table_items_problem(item)
            self.problem_widget.setCellWidget(row, 0, table_items[0])
            self.problem_widget.setItem(row, 1, table_items[1])
            self.problem_widget.setItem(row, 2, table_items[2])
            self.problem_widget.setItem(row, 3, table_items[3])
            self.problem_widget.setCellWidget(row, 4, table_items[4])
            self.problem_widget.setItem(row, 5, table_items[5])
            row += 1
