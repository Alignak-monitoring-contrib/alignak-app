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
    Synthesis
    +++++++++
    Synthesis manage creation of QWidget for Host Synthesis view
"""

from logging import getLogger

from PyQt5.Qt import QPushButton, QCompleter, QLineEdit, QIcon, QHBoxLayout, QLabel
from PyQt5.Qt import QStringListModel, Qt, QVBoxLayout, QWidget

from alignak_app.backend.datamanager import data_manager
from alignak_app.utils.config import settings

from alignak_app.qobjects.host.host import HostQWidget
from alignak_app.qobjects.service.services import ServicesQWidget

logger = getLogger(__name__)


class SynthesisQWidget(QWidget):
    """
        Class who manage Synthesis view with Host and Services QWidgets
    """

    def __init__(self, parent=None):
        super(SynthesisQWidget, self).__init__(parent)
        # Fields
        self.host_widget = HostQWidget()
        self.services_widget = ServicesQWidget()
        self.line_search = QLineEdit()
        self.completer = QCompleter()
        self.hint_widget = QWidget()

    def initialize_synthesis(self):
        """
        Initialize Synthesis QWidget

        """

        synthesis_layout = QVBoxLayout()
        self.setLayout(synthesis_layout)

        # Search widget
        search_widget = self.get_search_widget()
        synthesis_layout.addWidget(search_widget)

        # Host widget
        self.host_widget.initialize()
        synthesis_layout.addWidget(self.host_widget)

        # Hint Widget
        hint_text = _(
            '<h4>Dahsboard</h4>'
            '<ul><li>At the top of App, '
            'you have a dashboard that summarizes the number of items per state.</li></ul>'
            '<h4>Tabs</h4>'
            '<ul><li><h4>Host Synthesis</h4></li>'
            'Tap in the search bar to view a host and its services.'
            '<li><h4>Problems</h4></li>'
            'The "Problems" tab will show you all problems detected in your backend.'
            '<li><h4>Spy Hosts</h4></li>'
            'A "Spy Host" will keep you regularly informed of his condition. '
            'You will also see problems detected for this host, in the "Spy Hosts" panel.</ul>'
            '<h4>Alignak</h4>'
            '<ul><li>You can see your backend status and daemons if available, '
            'as well as your profile.</li></ul>'
            '<h4>Livestate</h4>'
            '<ul><li>In the livestate, you can see global state of your monitored items.</li></ul>'
            '<h4>Events</h4>'
            '<ul><li>Events will show you informative messages your actions inside App.</li></ul>'
        )
        hint_layout = QVBoxLayout(self.hint_widget)
        hint_label = QLabel(hint_text)
        hint_label.setObjectName('subtitle')
        hint_layout.addWidget(hint_label)
        synthesis_layout.addWidget(self.hint_widget)

        # Services widget
        self.services_widget.initialize()
        synthesis_layout.addWidget(self.services_widget)

        # Align all widgets to Top
        synthesis_layout.setAlignment(Qt.AlignTop)

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
        layout.addWidget(self.line_search)
        self.create_line_search([])

        return widget

    def create_line_search(self, hostnames_list):
        """
        Add all hosts to QLineEdit and set QCompleter

        :param hostnames_list: list of host names
        :type hostnames_list: list
        """

        # Get QStringListModel
        model = self.completer.model()
        if not model:
            model = QStringListModel()

        model.setStringList(hostnames_list)

        # Configure QCompleter from model
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setModel(model)
        self.completer.popup().setObjectName('popup')

        # Add completer to QLineEdit
        self.line_search.setCompleter(self.completer)
        self.line_search.setPlaceholderText(_('Type a host name to display its data'))
        self.line_search.setToolTip(_('Type a host name to display its data'))

    def update_synthesis(self, host, services, not_spied):
        """
        Update Synthesis QWidget with given host and services

        :param host: host item
        :type host: alignak_app.items.host.Host
        :param services: list of services attached to host
        :type services: list
        :param not_spied: define if host is spied or not
        :type not_spied: bool
        """

        self.host_widget.spy_btn.setEnabled(not_spied)

        if host:
            logger.info('Display %s in synthesis view', host.name)
            # Update Qwidgets
            self.host_widget.update_host(host)
            self.services_widget.update_widget(host, services)
            self.hint_widget.hide()
            self.host_widget.show()
            self.services_widget.show()

            # If the service element does not have the same ID as the host, reset to None
            if self.services_widget.service_data_widget.service_item:
                if self.services_widget.service_data_widget.service_item.data['host'] != \
                        self.services_widget.host.item_id:
                    self.services_widget.service_data_widget.service_item = None

        else:
            self.host_widget.hide()
            self.services_widget.hide()
            self.hint_widget.show()
