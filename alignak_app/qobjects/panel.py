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
    Panel
    +++++
    Panel manage creation of QWidget for Panel (Left part)
"""

from logging import getLogger

from PyQt5.Qt import QPushButton, QIcon, Qt, QVBoxLayout, QWidget, QTabWidget, QLabel

from alignak_app.backend.datamanager import data_manager
from alignak_app.backend.backend import app_backend
from alignak_app.utils.config import settings

from alignak_app.qobjects.events.item import EventItem
from alignak_app.qobjects.events.spy import SpyQWidget
from alignak_app.qobjects.alignak.dashboard import DashboardQWidget
from alignak_app.qobjects.alignak.problems import ProblemsQWidget
from alignak_app.qobjects.host.synthesis import SynthesisQWidget

logger = getLogger(__name__)


class PanelQWidget(QWidget):
    """
        Class who manage Panel with Host and Services QWidgets
    """

    def __init__(self, parent=None):
        super(PanelQWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        # Fields
        self.tab_widget = QTabWidget()
        self.layout = QVBoxLayout()
        self.dashboard_widget = DashboardQWidget()
        self.synthesis_widget = SynthesisQWidget()
        self.problems_widget = ProblemsQWidget()
        self.spy_widget = SpyQWidget()
        self.hostnames_list = []

    def initialize(self):
        """
        Create the QWidget with its items and layout.

        """

        logger.info('Create Panel View...')
        self.setLayout(self.layout)

        # Dashboard widget
        self.dashboard_widget.initialize()
        self.layout.addWidget(self.dashboard_widget)

        self.tab_widget.setMovable(True)
        self.layout.addWidget(self.tab_widget)
        tab_order = self.get_tab_order()

        # Set hostnames
        self.hostnames_list = data_manager.get_all_hostnames()

        # Synthesis
        self.synthesis_widget.initialize_synthesis()
        self.synthesis_widget.host_widget.spy_btn.clicked.connect(self.spy_host)
        self.synthesis_widget.line_search.returnPressed.connect(self.display_host)
        self.synthesis_widget.line_search.cursorPositionChanged.connect(self.display_host)
        self.synthesis_widget.create_line_search(self.hostnames_list)
        self.tab_widget.insertTab(tab_order.index('h'), self.synthesis_widget, _("Host Synthesis"))
        self.tab_widget.setTabToolTip(
            self.tab_widget.indexOf(self.synthesis_widget), _('See a synthesis view of a host')
        )

        # Problems
        self.problems_widget.initialize(self.spy_widget)
        self.problems_widget.host_btn.clicked.connect(self.display_host)
        self.tab_widget.insertTab(
            tab_order.index('p'),
            self.problems_widget,
            _('Problems (%d)') % len(data_manager.get_problems()['problems'])
        )
        self.tab_widget.setTabToolTip(
            self.tab_widget.indexOf(self.problems_widget), _('See the problems found in backend')
        )

        # Spied hosts
        self.spy_widget.initialize()
        self.tab_widget.insertTab(tab_order.index('s'), self.spy_widget, _('Spy Hosts'))
        self.tab_widget.setTabToolTip(
            self.tab_widget.indexOf(self.spy_widget), 'See spy hosts by Alignak-app'
        )

        # Hide widget for first display
        self.dashboard_widget.show()
        self.synthesis_widget.host_widget.hide()
        self.synthesis_widget.services_widget.hide()

    @staticmethod
    def get_tab_order():
        """
        Return tab order defined by user, else default order

        :return: tab order of App
        :rtype: list
        """

        default_order = ['p', 'h', 's']
        tab_order = settings.get_config('Alignak-app', 'tab_order').split(',')

        try:
            assert len(tab_order) == len(default_order)
            for nb in default_order:
                assert nb in tab_order
        except AssertionError:
            logger.error('Wrong "tab_order" value in config file %s', tab_order)
            tab_order = default_order

        return tab_order

    def spy_host(self):
        """
        Spy host who is available in line_search QLineEdit

        """

        if self.synthesis_widget.line_search.text() in self.hostnames_list:
            # Spy host
            self.spy_widget.spy_list_widget.add_spy_host(
                self.synthesis_widget.host_widget.host_item.item_id
            )

            # Update QWidgets
            self.synthesis_widget.host_widget.spy_btn.setEnabled(False)
            self.tab_widget.setTabText(
                self.tab_widget.indexOf(self.spy_widget),
                "Spied Hosts (%d)" % self.spy_widget.spy_list_widget.count()
            )

    def display_host(self):
        """
        Display and update HostQWidget

        """

        # Update and set "line_search" in case hosts have been added or deleted
        hostnames_list = data_manager.get_all_hostnames()
        if hostnames_list != self.hostnames_list:
            self.synthesis_widget.create_line_search(hostnames_list)

        # If sender is QPushButton from problems, set "line_search" text
        if isinstance(self.sender(), QPushButton):
            self.set_host_from_problems()

        # Display host if exists
        if self.synthesis_widget.line_search.text().rstrip() in self.hostnames_list:
            # Get Host Item and its services
            host = self.get_current_host()
            services = data_manager.get_host_services(host.item_id)

            if not services:
                app_backend.query_services(host.item_id)
                services = data_manager.get_host_services(host.item_id)

            # Update QWidgets
            not_spied = bool(
                host.item_id not in self.spy_widget.spy_list_widget.spied_hosts
            )
            self.synthesis_widget.update_synthesis(host, services, not_spied)
            self.dashboard_widget.update_dashboard()
        else:
            self.synthesis_widget.update_synthesis(None, None, True)

    def set_host_from_problems(self):
        """
        Set line search if ``sender()`` is instance of QPushButton from
        :class:`Problems <alignak_app.qobjects.alignak.problems.ProblemsQWidget>` QWidget

        """

        item = self.problems_widget.get_curent_user_role_item()
        if item:
            if 'service' in item.item_type:
                hostname = data_manager.get_item('host', item.data['host']).name
            else:
                hostname = item.name

            if hostname in self.hostnames_list:
                self.synthesis_widget.line_search.setText(hostname)
                self.tab_widget.setCurrentIndex(self.tab_widget.indexOf(self.synthesis_widget))

    def get_current_host(self):
        """
        Return current Host item with name in QLineEdit

        :return: current host
        :rtype: alignak_app.items.host.Host
        """

        current_host = data_manager.get_item(
            'host',
            self.synthesis_widget.line_search.text().rstrip()
        )

        return current_host

    def dragMoveEvent(self, event):  # pragma: no cover
        """
        Override dragMoveEvent.
         Only accept EventItem() objects who have ``Qt.UserRole``

        :param event: event triggered when something move
        """

        if event.source().currentItem().data(Qt.UserRole):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):  # pragma: no cover
        """
        Override dropEvent.
         Get dropped item data, create a new one, and delete the one who is in EventsQWidget

        :param event: event triggered when something is dropped
        """

        host = data_manager.get_item('host', '_id', event.source().currentItem().data(Qt.UserRole))

        logger.debug('Drag and drop host in Panel: %s', host.name)
        logger.debug('... with current item: %s', event.source().currentItem())

        self.synthesis_widget.line_search.setText(host.name)
        self.tab_widget.setCurrentIndex(self.tab_widget.indexOf(self.synthesis_widget))
        self.display_host()

    def dragEnterEvent(self, event):
        """
        Override dragEnterEvent.

        :param event: event triggered when something enter
        """

        event.accept()
        event.acceptProposedAction()
