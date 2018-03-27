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

from PyQt5.Qt import QPushButton, QCompleter, QLineEdit, QIcon, QHBoxLayout, QLabel
from PyQt5.Qt import QStringListModel, Qt, QVBoxLayout, QWidget, QTabWidget

from alignak_app.backend.datamanager import data_manager
from alignak_app.backend.backend import app_backend
from alignak_app.utils.config import settings

from alignak_app.qobjects.events.item import EventItem
from alignak_app.qobjects.events.spy import SpyQWidget
from alignak_app.qobjects.alignak.dashboard import DashboardQWidget
from alignak_app.qobjects.host.host import HostQWidget
from alignak_app.qobjects.alignak.problems import ProblemsQWidget
from alignak_app.qobjects.service.services import ServicesQWidget

logger = getLogger(__name__)


class PanelQWidget(QWidget):
    """
        Class who manage Panel with Host and Services QWidgets
    """

    spy_icons = {
        True: 'spy',
        False: 'spy_ok',
    }

    def __init__(self, parent=None):
        super(PanelQWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        # Fields
        self.tab_widget = QTabWidget()
        self.layout = QVBoxLayout()
        self.line_search = QLineEdit()
        self.completer = QCompleter()
        self.hostnames_list = []
        self.dashboard_widget = DashboardQWidget()
        self.host_widget = HostQWidget()
        self.synthesis_widget = QWidget()
        self.services_widget = ServicesQWidget()
        self.problems_widget = ProblemsQWidget()
        self.spy_text = {True: _("Spy Host"), False: _("Host spied!")}
        self.spy_widget = SpyQWidget()
        self.spy_button = QPushButton(self.spy_text[True])
        self.spied_hosts = []

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

        # Synthesis
        self.init_synthesis_widget()
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
        self.tab_widget.insertTab(tab_order.index('s'), self.spy_widget, _('Spied Hosts'))
        self.tab_widget.setTabToolTip(
            self.tab_widget.indexOf(self.spy_widget), 'See the hosts spied by Alignak-app'
        )

        # Hide widget for first display
        self.host_widget.hide()
        self.services_widget.hide()

    def init_synthesis_widget(self):
        """
        Initialize Synthesis QWidget

        """

        synthesis_layout = QVBoxLayout()
        self.synthesis_widget.setLayout(synthesis_layout)

        # Search widget
        search_widget = self.get_search_widget()
        synthesis_layout.addWidget(search_widget)

        # Host widget
        self.host_widget.initialize()
        synthesis_layout.addWidget(self.host_widget)

        # Services widget
        self.services_widget.initialize()
        synthesis_layout.addWidget(self.services_widget)

        # Align all widgets to Top
        synthesis_layout.setAlignment(Qt.AlignTop)

    @staticmethod
    def get_tab_order():
        """
        Return tab order defined by user, else default order

        :return: tab order of App
        :rtype: list
        """

        default_order = ['h', 'p', 's']
        tab_order = settings.get_config('Alignak-app', 'tab_order').split(',')

        try:
            assert len(tab_order) == len(default_order)
            for nb in default_order:
                assert nb in tab_order
        except AssertionError:
            logger.error('Wrong "tab_order" value in config file %s', tab_order)
            tab_order = ['h', 'p', 's']

        return tab_order

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
        search_lbl = QLabel(_('Search Host'))
        search_lbl.setObjectName('bordertitle')
        search_lbl.setFixedHeight(25)
        search_lbl.setToolTip(_('Search Host'))
        layout.addWidget(search_lbl)

        # QLineEdit
        self.line_search.setFixedHeight(search_lbl.height())
        self.line_search.returnPressed.connect(self.display_host)
        self.line_search.cursorPositionChanged.connect(self.display_host)
        layout.addWidget(self.line_search)

        self.spy_button.setIcon(QIcon(settings.get_image('spy')))
        self.spy_button.setObjectName('valid')
        self.spy_button.setFixedSize(110, 25)
        self.spy_button.clicked.connect(self.spy_host)
        layout.addWidget(self.spy_button)

        self.create_line_search()

        return widget

    def spy_host(self):
        """
        Spy host who is available in line_search QLineEdit

        """

        if self.line_search.text() in self.hostnames_list:
            host = data_manager.get_item('host', 'name', self.line_search.text())
            self.spy_widget.spy_list_widget.add_spy_host(host.item_id)
            self.spy_button.setEnabled(False)

            self.spy_button.setIcon(
                QIcon(settings.get_image(self.spy_icons[False]))
            )
            self.spy_button.setText(self.spy_text[False])
            self.update_panel_spytab()
        else:
            self.spy_button.setEnabled(True)
            self.spy_button.setIcon(
                QIcon(settings.get_image(self.spy_icons[True]))
            )
            self.spy_button.setText(self.spy_text[True])

    def update_panel_spytab(self):
        """
        Update text of the psy panel tab

        """

        self.tab_widget.setTabText(
            self.tab_widget.indexOf(self.spy_widget),
            "Spied Hosts (%d)" % self.spy_widget.spy_list_widget.count()
        )

    def create_line_search(self, hostnames_list=None):
        """
        Add all hosts to QLineEdit and set QCompleter

        :param hostnames_list: list of host names
        :type hostnames_list: list
        """

        # Get QStringListModel
        model = self.completer.model()
        if not model:
            model = QStringListModel()

        if not hostnames_list:
            self.hostnames_list = data_manager.get_all_hostnames()
        else:
            self.hostnames_list = hostnames_list

        model.setStringList(self.hostnames_list)

        # Configure QCompleter from model
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setModel(model)
        self.completer.popup().setObjectName('popup')

        # Add completer to QLineEdit
        self.line_search.setCompleter(self.completer)
        self.line_search.setPlaceholderText(_('Type a host name to display its data'))
        self.line_search.setToolTip(_('Type a host name to display its data'))

    def display_host(self):
        """
        Display and update HostQWidget

        """

        # Update and set "line_search" in case hosts have been added or deleted
        hostnames_list = data_manager.get_all_hostnames()
        if hostnames_list != self.hostnames_list:
            self.create_line_search(hostnames_list)

        # If sender is QPushButton from problems, set "line_search" text
        if isinstance(self.sender(), QPushButton):
            self.set_line_search()

        # Display host if exists
        if self.line_search.text().rstrip() in self.hostnames_list:
            # Get Host Item and its services
            host_item = data_manager.get_item('host', self.line_search.text().rstrip())
            services = data_manager.get_host_services(host_item.item_id)
            if not services:
                app_backend.query_services(host_item.item_id)
                services = data_manager.get_host_services(host_item.item_id)

            # Set spy button enable or not
            not_spied = bool(
                host_item.item_id not in self.spy_widget.spy_list_widget.spied_hosts
            )
            self.spy_button.setEnabled(not_spied)
            self.spy_button.setIcon(
                QIcon(settings.get_image(self.spy_icons[not_spied]))
            )
            self.spy_button.setText(self.spy_text[not_spied])

            # Update Qwidgets
            self.host_widget.update_host(host_item)
            self.host_widget.show()
            self.services_widget.update_widget(host_item, services)
            self.services_widget.show()
            self.dashboard_widget.update_dashboard()
            self.dashboard_widget.show()

            # If the service element does not have the same ID as the host, reset to None
            if self.services_widget.service_data_widget.service_item:
                if self.services_widget.service_data_widget.service_item.data['host'] != \
                        self.services_widget.host.item_id:
                    self.services_widget.service_data_widget.service_item = None
        else:
            self.host_widget.hide()
            self.services_widget.hide()

            self.spy_button.setEnabled(True)
            self.spy_button.setIcon(
                QIcon(settings.get_image(self.spy_icons[True]))
            )
            self.spy_button.setText(self.spy_text[True])

        self.spy_button.style().unpolish(self.spy_button)
        self.spy_button.style().polish(self.spy_button)

    def set_line_search(self):
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
                self.line_search.setText(hostname)
                self.tab_widget.setCurrentIndex(self.tab_widget.indexOf(self.synthesis_widget))

    def dragMoveEvent(self, event):  # pragma: no cover
        """
        Override dragMoveEvent.
         Only accept EventItem() objects who have ``Qt.UserRole``

        :param event: event triggered when something move
        """

        if isinstance(event.source().currentItem(), EventItem):
            if event.source().currentItem().data(Qt.UserRole):
                event.accept()
            else:
                event.ignore()
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

        self.line_search.setText(host.name)
        self.tab_widget.setCurrentIndex(self.tab_widget.indexOf(self.synthesis_widget))
        self.display_host()

    def dragEnterEvent(self, event):
        """
        Override dragEnterEvent.

        :param event: event triggered when something enter
        """

        event.accept()
        event.acceptProposedAction()
