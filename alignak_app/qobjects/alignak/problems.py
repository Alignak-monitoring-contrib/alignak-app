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

    * **Hosts**: ``DOWN``, ``UNREACHABLE``
    * **Services**: ``WARNING``, ``CRITICAL``, ``UNKNOWN``

"""

from logging import getLogger

from PyQt5.Qt import QWidget, QIcon, QVBoxLayout, QPushButton, Qt, QLabel, QHBoxLayout

from alignak_app.backend.datamanager import data_manager
from alignak_app.utils.config import settings

from alignak_app.qobjects.common.actions import ActionsQWidget
from alignak_app.qobjects.alignak.problems_table import ProblemsQTableWidget

logger = getLogger(__name__)


class ProblemsQWidget(QWidget):
    """
        Class who create Problems QWidget
    """

    def __init__(self, parent=None):
        super(ProblemsQWidget, self).__init__(parent)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        # Fields
        self.problem_table = ProblemsQTableWidget()
        self.problems_title = QLabel()
        self.actions_widget = ActionsQWidget()
        self.host_btn = QPushButton()
        self.spy_btn = QPushButton()
        self.spy_widget = None

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

        self.problem_table.initialize()
        self.problem_table.currentItemChanged.connect(self.update_action_buttons)
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
            self.host_btn.setEnabled(True)

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
        self.problem_table.setRowCount(len(problems_data['problems']))

        row = 0
        for item in problems_data['problems']:
            self.problem_table.setItem(row, 0, self.problem_table.get_tableitem(item))
            self.problem_table.setItem(row, 1, self.problem_table.get_output_tableitem(item))
            row += 1
