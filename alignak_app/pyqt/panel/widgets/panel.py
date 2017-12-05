#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2017:
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
    Panel QWidget manage the creation of Hosts and Services QWidgets
"""

from logging import getLogger

from PyQt5.Qt import QApplication, QPushButton, QCompleter, QLineEdit, QIcon, QHBoxLayout
from PyQt5.Qt import QStringListModel, Qt, QVBoxLayout, QWidget, QTabWidget

from alignak_app.core.backend.data_manager import data_manager
from alignak_app.core.utils.config import app_css, get_image
from alignak_app.pyqt.common.frames import AppQFrame, get_frame_separator
from alignak_app.pyqt.dock.widgets.events import EventItem
from alignak_app.pyqt.panel.widgets.dashboard import DashboardQWidget
from alignak_app.pyqt.panel.widgets.host import HostQWidget
from alignak_app.pyqt.panel.widgets.problems import ProblemsQWidget
from alignak_app.pyqt.panel.widgets.services import ServicesQWidget

logger = getLogger(__name__)


class PanelQWidget(QWidget):
    """
        Class who manage Panel with Host and Services QWidgets
    """

    def __init__(self, parent=None):
        super(PanelQWidget, self).__init__(parent)
        self.tab_widget = QTabWidget()
        self.setStyleSheet(app_css)
        self.setWindowIcon(QIcon(get_image('icon')))
        self.setAcceptDrops(True)
        # Fields
        self.layout = QVBoxLayout()
        self.line_search = QLineEdit()
        self.completer = QCompleter()
        self.app_widget = AppQFrame()
        self.hostnames_list = []
        self.dashboard_widget = DashboardQWidget()
        self.host_widget = HostQWidget()
        self.services_widget = ServicesQWidget()
        self.spy_button = QPushButton(_("Spy Host"))
        self.spy_widget = None

    def initialize(self, dock_width, spy_widget):
        """
        Create the QWidget with its items and layout.

        :param dock_width: width of dock, needed for PanelQWidget
        :type dock_width: int
        :param spy_widget: SpyQWidget to allow HostQWidget add spied host
        :type spy_widget: alignak_app.pyqt.dock.widgets.spy.SpyQWidget
        """

        logger.info('Create Panel View...')
        self.setLayout(self.layout)

        # Dashboard widget
        self.dashboard_widget.initialize()
        self.layout.addWidget(self.dashboard_widget)
        self.layout.addWidget(get_frame_separator())

        self.tab_widget.addTab(self.get_synthesis_widget(), _("Host Synthesis"))

        problems_widget = ProblemsQWidget()
        problems_widget.initialize()
        self.tab_widget.addTab(problems_widget, _("Problems"))

        self.layout.addWidget(self.tab_widget)

        # Apply size and position on AppQWidget
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        desktop = QApplication.desktop().availableGeometry(screen)

        self.app_widget.initialize(_('Hosts Synthesis View'))
        self.app_widget.add_widget(self)
        self.app_widget.resize(desktop.width() - dock_width, desktop.height())
        self.app_widget.move(0, 0)

        # Hide widgets for first start
        self.host_widget.hide()
        self.services_widget.hide()

        self.spy_widget = spy_widget

    def get_synthesis_widget(self):
        """
        Return synthesis QWidget()

        :return: synthesis QWidget()
        :rtype: QWidget
        """

        synthesis_widget = QWidget()
        synthesis_layout = QVBoxLayout()
        synthesis_widget.setLayout(synthesis_layout)

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

        return synthesis_widget

    def get_search_widget(self):
        """
        Create and return the search QWidget

        :return: search QWidget
        :rtype: QWidget
        """

        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)

        # Search button
        button = QPushButton(_('Search Host'), self)
        button.setObjectName('search')
        button.setFixedHeight(25)
        button.setToolTip(_('Search Host'))
        button.clicked.connect(self.display_host)
        layout.addWidget(button)

        self.line_search.setFixedHeight(button.height())
        self.line_search.returnPressed.connect(button.click)
        self.line_search.cursorPositionChanged.connect(button.click)
        layout.addWidget(self.line_search)

        self.spy_button.setIcon(QIcon(get_image('spy')))
        self.spy_button.setObjectName('search')
        self.spy_button.setFixedHeight(25)
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
            self.spy_widget.spy_list_widget.host_spied.emit(host.item_id)
            self.spy_button.setEnabled(False)

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

        # Add completer to QLineEdit
        self.line_search.setCompleter(self.completer)
        self.line_search.setPlaceholderText(_('Type a host name to display its data'))
        self.line_search.setToolTip(_('Type a host name to display its data'))

    def display_host(self):
        """
        Display and update HostQWidget

        """

        if self.line_search.text() in self.hostnames_list:
            # Update linesearch if needed
            hostnames_list = data_manager.get_all_hostnames()
            if hostnames_list != self.hostnames_list:
                self.create_line_search(hostnames_list)

            # Set spy button enable or not
            is_spied = bool(
                data_manager.get_item('host', 'name', self.line_search.text()).item_id not in
                self.spy_widget.spy_list_widget.spied_hosts
            )
            self.spy_button.setEnabled(is_spied)

            # Update QWidgets
            self.dashboard_widget.update_dashboard()
            self.dashboard_widget.show()
            self.host_widget.update_host(self.line_search.text())
            self.host_widget.show()
            self.services_widget.set_data(self.line_search.text())
            self.services_widget.update_widget()
            self.services_widget.show()
        else:
            self.host_widget.hide()
            self.services_widget.hide()

    def dragMoveEvent(self, event):
        """
        Override dragMoveEvent.
         Only accept EventItem() objects who are "spied_on" and not already spied

        :param event: event triggered when something move
        """

        if isinstance(event.source().currentItem(), EventItem):
            if event.source().currentItem().spied_on:
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        """
        Override dropEvent.
         Get dropped item data, create a new one, and delete the one who is in EventsQWidget

        :param event: event triggered when something is dropped
        """

        host = data_manager.get_item('host', '_id', event.source().currentItem().host)

        logger.debug('Drag and drop host in Panel: %s', host.name)
        logger.debug('... with current item: %s', event.source().currentItem())

        self.line_search.setText(host.name)
        self.display_host()

    def dragEnterEvent(self, event):
        """
        Override dragEnterEvent.

        :param event: event triggered when something enter
        """

        event.accept()
        event.acceptProposedAction()
