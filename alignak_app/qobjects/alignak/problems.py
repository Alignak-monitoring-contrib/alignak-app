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

from PyQt5.Qt import QWidget, QIcon, QVBoxLayout, QPushButton, Qt, QLabel, QLineEdit, QHBoxLayout

from alignak_app.backend.datamanager import data_manager
from alignak_app.backend.backend import app_backend
from alignak_app.utils.config import settings

from alignak_app.qobjects.common.actions import ActionsQWidget
from alignak_app.qobjects.common.buttons import ToggleQWidgetButton
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
        self.line_search = QLineEdit()
        self.problems_table = ProblemsQTableView()
        self.problems_title = QLabel()
        self.actions_widget = ActionsQWidget()
        self.spy_widget = None
        self.filter_hosts_btn = ToggleQWidgetButton()
        self.filter_services_btn = ToggleQWidgetButton()
        self.spy_btn = QPushButton()
        self.host_btn = QPushButton()

    def initialize(self, spy_widget):
        """
        Initialize QWidget and set SpyQWidget

        :param spy_widget: instance of SpyQWidget to manage spy events
        :type spy_widget: alignak_app.qobjects.events.spy.SpyQWidget
        """

        problem_layout = QVBoxLayout()
        problem_layout.setContentsMargins(5, 20, 5, 5)
        self.setLayout(problem_layout)

        self.spy_widget = spy_widget

        self.problems_title.setObjectName('title')
        problem_layout.addWidget(self.problems_title)

        problem_layout.addWidget(self.get_search_widget())

        problem_layout.addWidget(self.get_btn_widget())

        problem_layout.addWidget(self.problems_table)

        self.update_problems_data()

    def get_curent_user_role_item(self):
        """
        Return current selected item by ``Qt.UserRole``

        :return: current selected item or None
        :rtype: alignak_app.items.item.Item
        """

        item = self.problems_table.model().data(
            self.problems_table.selectionModel().currentIndex(),
            Qt.UserRole
        )

        return item

    def update_action_buttons(self):
        """
        Update status of action buttons and set current item for ActionsQWidget

        """

        # Get item by UserRole
        item = self.get_curent_user_role_item()

        if item:
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
        else:
            self.actions_widget.acknowledge_btn.setEnabled(False)
            self.actions_widget.downtime_btn.setEnabled(False)
            self.host_btn.setEnabled(False)
            self.spy_btn.setEnabled(False)

    def get_search_widget(self):
        """
        Create and return the search QWidget

        :return: search QWidget
        :rtype: QWidget
        """

        widget = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(5, 20, 5, 10)
        widget.setLayout(layout)

        # Search label
        search_lbl = QLabel(_('Search Problems'))
        search_lbl.setObjectName('bordertitle')
        search_lbl.setFixedHeight(25)
        search_lbl.setToolTip(_('Search Problems'))
        layout.addWidget(search_lbl)

        # QLineEdit
        self.line_search.setFixedHeight(search_lbl.height())
        self.line_search.setPlaceholderText(_('Type text to filter problems...'))
        layout.addWidget(self.line_search)

        # Refresh button
        refresh_btn = QPushButton(_('Refresh'))
        refresh_btn.setObjectName('ok')
        refresh_btn.setFixedSize(120, search_lbl.height())
        refresh_btn.setToolTip(_('Refresh problems'))
        refresh_btn.clicked.connect(self.update_problems_data)
        layout.addWidget(refresh_btn)

        return widget

    def get_btn_widget(self):
        """
        Return QWidget with spy and host synthesis QPushButtons

        :return: widget with spy and host button
        :rtype: QWidget
        """

        widget_btn = QWidget()
        layout_btn = QHBoxLayout()
        layout_btn.setContentsMargins(0, 0, 0, 5)
        widget_btn.setLayout(layout_btn)

        host_filter = QLabel(_('Filter hosts'))
        host_filter.setObjectName('subtitle')
        layout_btn.addWidget(host_filter)
        self.filter_hosts_btn.initialize()
        self.filter_hosts_btn.update_btn_state(False)
        self.filter_hosts_btn.toggle_btn.clicked.connect(lambda: self.update_problems_data('host'))
        layout_btn.addWidget(self.filter_hosts_btn)

        service_filter = QLabel(_('Filter services'))
        service_filter.setObjectName('subtitle')
        layout_btn.addWidget(service_filter)
        self.filter_services_btn.initialize()
        self.filter_services_btn.update_btn_state(False)
        self.filter_services_btn.toggle_btn.clicked.connect(
            lambda: self.update_problems_data('service')
        )
        layout_btn.addWidget(self.filter_services_btn)

        layout_btn.addStretch()

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

        self.actions_widget.initialize(None)
        self.actions_widget.acknowledge_btn.setEnabled(False)
        self.actions_widget.downtime_btn.setEnabled(False)
        layout_btn.addWidget(self.actions_widget)

        layout_btn.setAlignment(Qt.AlignCenter)

        return widget_btn

    def add_spied_host(self):
        """
        Add a host to spied hosts

        """

        # Get item by UserRole
        item = self.get_curent_user_role_item()

        if item:
            if 'service' in item.item_type:
                item_id = item.data['host']
            else:
                item_id = item.item_id

            app_backend.query_services(item_id)
            self.spy_widget.spy_list_widget.add_spy_host(item_id)
            self.spy_widget.update_parent_spytab()

        self.update_action_buttons()

    def update_problems_data(self, item_type=''):
        """
        Update data of Problems QTableWidget and problems title

        :param item_type: type of item to filter
        :type item_type: str
        """

        problems_data = data_manager.get_problems()
        old_research = self.line_search.text()

        if self.parent():
            self.parent().parent().setTabText(
                self.parent().parent().indexOf(self),
                _("Problems (%d)") % len(problems_data['problems'])
            )

        if self.filter_hosts_btn.is_checked() and not self.filter_services_btn.is_checked():
            item_type = 'host'
        if self.filter_services_btn.is_checked() and not self.filter_hosts_btn.is_checked():
            item_type = 'service'
        if not self.filter_services_btn.is_checked() and not self.filter_hosts_btn.is_checked():
            item_type = ''

        if isinstance(item_type, str):
            if 'host' in item_type and self.filter_hosts_btn.is_checked():
                if self.filter_services_btn.is_checked():
                    self.filter_services_btn.update_btn_state(False)
            if 'service' in item_type and self.filter_services_btn.is_checked():
                if self.filter_hosts_btn.is_checked():
                    self.filter_hosts_btn.update_btn_state(False)
            problems_data['problems'] = [
                item for item in problems_data['problems'] if item_type in item.item_type
            ]

        proxy_filter = self.problems_table.update_view(problems_data)
        if problems_data['problems']:
            self.problems_title.setText(
                _('There are %d problems to manage (hosts: %d, services: %d)') % (
                    len(problems_data['problems']),
                    problems_data['hosts_nb'],
                    problems_data['services_nb']
                )
            )
            self.line_search.textChanged.connect(proxy_filter.setFilterRegExp)
        else:
            self.problems_title.setText(_('If problems are found, they will be displayed here.'))

        self.problems_table.selectionModel().selectionChanged.connect(self.update_action_buttons)
        self.update_action_buttons()

        if old_research:
            self.line_search.setText(old_research)
            self.line_search.textChanged.emit(old_research)
