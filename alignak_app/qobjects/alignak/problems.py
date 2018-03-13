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
    Problems manage creation of QWidgets to display problems found in Alignak backend:
"""

from logging import getLogger

from PyQt5.Qt import QWidget, QIcon, QVBoxLayout, QPushButton, Qt, QLabel, QHBoxLayout, QLineEdit
from PyQt5.Qt import QStandardItemModel, QSortFilterProxyModel

from alignak_app.backend.datamanager import data_manager
from alignak_app.utils.config import settings

from alignak_app.qobjects.common.actions import ActionsQWidget
from alignak_app.qobjects.alignak.problems_table import ProblemsQTableView

logger = getLogger(__name__)


class ProblemsQWidget(QWidget):
    """
        Class who create Problems QWidget
    """

    def __init__(self, parent=None):
        super(ProblemsQWidget, self).__init__(parent)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        # Fields
        self.problem_table = ProblemsQTableView()
        self.problems_title = QLabel()
        self.problems_model = QStandardItemModel()
        self.actions_widget = ActionsQWidget()
        self.host_btn = QPushButton()
        self.spy_btn = QPushButton()
        self.spy_widget = None
        self.line_search = QLineEdit()

    def initialize(self, spy_widget):
        """
        Initialize QWidget and set SpyQWidget

        :param spy_widget: instance of SpyQWidget to manage spy events
        :type spy_widget: alignak_app.qobjects.events.spy.SpyQWidget
        """

        problem_layout = QVBoxLayout()
        self.setLayout(problem_layout)

        self.spy_widget = spy_widget

        problem_layout.addWidget(self.get_problems_widget_title())

        problem_layout.addWidget(self.get_search_widget())

        # self.problem_table.initialize()
        problem_layout.addWidget(self.problem_table)

        self.update_problems_data()

    def update_action_buttons(self):
        """
        Update status of action buttons and set current item for ActionsQWidget

        """

        # Get QStandardItem
        standard_item = self.problems_model.item(
            self.problem_table.selectionModel().currentIndex().row(),
            self.problem_table.selectionModel().currentIndex().column()
        )

        if standard_item:
            item = standard_item.item

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
            self.host_btn.setEnabled(True)

    def get_search_widget(self):
        """
        Create and return the search QWidget

        :return: search QWidget
        :rtype: QWidget
        """

        widget = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(0)
        widget.setLayout(layout)

        # Search label
        search_lbl = QLabel(_('Search Problems'))
        search_lbl.setObjectName('bordertitle')
        search_lbl.setFixedHeight(25)
        search_lbl.setToolTip(_('Search Problems'))
        layout.addWidget(search_lbl)

        # QLineEdit
        self.line_search.setFixedHeight(search_lbl.height())
        layout.addWidget(self.line_search)

        return widget

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

        layout_title.addWidget(self.get_btn_widget())

        self.actions_widget.initialize(None)
        self.actions_widget.acknowledge_btn.setEnabled(False)
        self.actions_widget.downtime_btn.setEnabled(False)
        layout_title.addWidget(self.actions_widget)

        refresh_btn = QPushButton(_('Refresh'))
        refresh_btn.setObjectName('ok')
        refresh_btn.setFixedSize(120, 30)
        refresh_btn.clicked.connect(self.update_problems_data)
        layout_title.addWidget(refresh_btn)

        return widget_title

    def get_btn_widget(self):
        """
        Return QWidget with spy and host synthesis QPushButtons

        :return: widget with spy and host button
        :rtype: QWidget
        """

        widget_btn = QWidget()
        layout_btn = QHBoxLayout()
        widget_btn.setLayout(layout_btn)

        self.host_btn.setIcon(QIcon(settings.get_image('host')))
        self.host_btn.setFixedSize(80, 20)
        self.host_btn.setEnabled(False)
        self.host_btn.setToolTip(_('See current item in synthesis view'))
        layout_btn.addWidget(self.host_btn)

        self.spy_btn.setIcon(QIcon(settings.get_image('spy')))
        self.spy_btn.setFixedSize(80, 20)
        self.spy_btn.setEnabled(False)
        self.spy_btn.setToolTip(_('Spy current host'))
        self.spy_btn.clicked.connect(self.add_spied_host)

        layout_btn.addWidget(self.spy_btn)

        layout_btn.setAlignment(Qt.AlignCenter)

        return widget_btn

    def add_spied_host(self):
        """
        Add a host to spied hosts

        """

        # Get QStandardItem
        standard_item = self.problems_model.item(
            self.problem_table.selectionModel().currentIndex().row(),
            self.problem_table.selectionModel().currentIndex().column()
        )

        if standard_item:
            item = standard_item.item
            if 'service' in item.item_type:
                item_id = item.data['host']
            else:
                item_id = item.item_id

            self.spy_widget.spy_list_widget.add_spy_host(item_id)
            self.spy_widget.update_parent_spytab()

        self.update_action_buttons()

    def update_problems_data(self):
        """
        Update data of Problems QTableWidget and problems title

        """

        problems_data = data_manager.get_problems()

        if self.parent():
            self.parent().parent().setTabText(
                1, _("Problems (%d)") % len(problems_data['problems'])
            )

        self.problems_title.setText(
            _('There are %d problems to manage (hosts: %d, services: %d)') % (
                len(problems_data['problems']),
                problems_data['hosts_nb'],
                problems_data['services_nb']
            )
        )
        self.problems_model.setRowCount(len(problems_data['problems']))
        self.problems_model.setColumnCount(len(self.problem_table.headers_list))
        self.problems_model.setSortRole(1)

        for row, item in enumerate(problems_data['problems']):
            self.problems_model.setItem(row, 0, self.problem_table.get_tableitem(item))
            self.problems_model.setItem(row, 1, self.problem_table.get_output_tableitem(item))

        proxy_filter = QSortFilterProxyModel()
        proxy_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        proxy_filter.setSourceModel(self.problems_model)
        self.line_search.textChanged.connect(proxy_filter.setFilterRegExp)

        self.problem_table.initialize(proxy_filter)
        self.problems_model.setHorizontalHeaderLabels(self.problem_table.headers_list)
        self.problem_table.selectionModel().selectionChanged.connect(self.update_action_buttons)
