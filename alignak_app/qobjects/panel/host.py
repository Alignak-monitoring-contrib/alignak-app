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
    Host
    ++++
    Host manage creation of QWidget to display host data
"""

from logging import getLogger

from PyQt5.Qt import QLabel, QWidget, QGridLayout, Qt, QPixmap, QVBoxLayout, QHBoxLayout
from PyQt5.Qt import QPushButton, QIcon, QTimer, QScrollArea

from alignak_app.backend.backend import app_backend
from alignak_app.backend.datamanager import data_manager
from alignak_app.items.item import get_host_msg_and_event_type
from alignak_app.items.item import get_icon_name, get_real_host_state_icon
from alignak_app.utils.config import settings
from alignak_app.utils.time import get_time_diff_since_last_timestamp

from alignak_app.qobjects.common.actions import ActionsQWidget
from alignak_app.qobjects.common.buttons import ToggleQWidgetButton
from alignak_app.qobjects.dock.events import send_event
from alignak_app.qobjects.panel.history import HistoryQWidget

from alignak_app.qthreads.threadmanager import thread_manager

logger = getLogger(__name__)


class HostQWidget(QWidget):
    """
        Class who create QWidget to display host data
    """

    def __init__(self, parent=None):
        super(HostQWidget, self).__init__(parent)
        # Fields
        self.actions_widget = ActionsQWidget()
        self.host_item = None
        self.service_items = None
        self.labels = {
            'host_icon': QLabel(),
            'host_name': QLabel(),
            'state_icon': QLabel(),
            'ls_last_check': QLabel(),
            'ls_output': QLabel(),
            'realm': QLabel(),
            'address': QLabel(),
            'business_impact': QLabel(),
            'notes': QLabel()
        }
        self.activecheck_btn = ToggleQWidgetButton()
        self.passivecheck_btn = ToggleQWidgetButton()
        self.history_btn = QPushButton()
        self.history_widget = None
        self.host_history = None
        self.refresh_timer = QTimer()

    def initialize(self):
        """
        Initialize QWidget

        """

        layout = QGridLayout()
        self.setLayout(layout)

        # Add Qwidgets
        layout.addWidget(self.get_host_icon_widget(), 0, 0, 2, 1)

        layout.addWidget(self.get_last_check_widget(), 0, 1, 1, 1)

        layout.addWidget(self.get_variables_widget(), 0, 2, 1, 1)

        layout.addWidget(self.get_notes_output_widget(), 1, 1, 1, 2)

        layout.addWidget(self.get_actions_widget(), 0, 3, 2, 1)

        update_host = int(settings.get_config('Alignak-app', 'update_host')) * 1000
        self.refresh_timer.setInterval(update_host)
        self.refresh_timer.start()
        self.refresh_timer.timeout.connect(self.update_host)

    def set_data(self, hostname):
        """
        Set data of host and service

        :param hostname: name of host to display
        :type hostname: str
        """

        host_and_services = data_manager.get_host_with_services(hostname)

        self.host_item = host_and_services['host']
        self.service_items = host_and_services['services']

    def get_host_icon_widget(self):
        """
        Return QWidget with overall icon state and host name

        :return: widget with host name and icon
        :rtype: QWidget
        """

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Host Icon
        layout.addWidget(self.labels['host_icon'])
        layout.setAlignment(self.labels['host_icon'], Qt.AlignCenter)

        # Host Name
        self.labels['host_name'].setObjectName('itemname')
        layout.addWidget(self.labels['host_name'])
        layout.setAlignment(self.labels['host_name'], Qt.AlignCenter)

        return widget

    def get_actions_widget(self):
        """
        Return QWidget with actions buttons

        :return: widget with buttons
        :rtype: QWidget
        """

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        action_title = QLabel(_('Host actions'))
        action_title.setObjectName('itemtitle')
        action_title.setFixedHeight(25)
        layout.addWidget(action_title)

        ack_down_lbl = QLabel(_('Acknowledge / Downtime:'))
        ack_down_lbl.setObjectName('subtitle')
        layout.addWidget(ack_down_lbl)

        self.actions_widget.initialize(self.host_item)
        layout.addWidget(self.actions_widget)

        activecheck_lbl = QLabel(_('Active checks:'))
        activecheck_lbl.setObjectName('subtitle')
        layout.addWidget(activecheck_lbl)
        self.activecheck_btn.initialize()
        self.activecheck_btn.toggle_btn.clicked.connect(lambda: self.patch_host_checks(
            'active_checks_enabled', self.activecheck_btn.get_btn_state()
        ))
        layout.addWidget(self.activecheck_btn)

        passivecheck_lbl = QLabel(_('Passive checks:'))
        passivecheck_lbl.setObjectName('subtitle')
        layout.addWidget(passivecheck_lbl)
        self.passivecheck_btn.initialize()
        self.passivecheck_btn.toggle_btn.clicked.connect(lambda: self.patch_host_checks(
            'passive_checks_enabled', self.passivecheck_btn.get_btn_state()
        ))
        layout.addWidget(self.passivecheck_btn)

        hist_lbl = QLabel(_('Timeline:'))
        hist_lbl.setObjectName('subtitle')
        layout.addWidget(hist_lbl)
        self.history_btn.setIcon(QIcon(settings.get_image('time')))
        self.history_btn.setFixedSize(80, 20)
        self.history_btn.clicked.connect(self.show_history)
        layout.addWidget(self.history_btn)
        layout.setAlignment(self.history_btn, Qt.AlignCenter)

        layout.setAlignment(Qt.AlignCenter)

        return widget

    def show_history(self):
        """
        Create and show HistoryQWidget

        """

        self.history_widget = HistoryQWidget(self)
        self.history_widget.initialize(self.host_item.name, self.host_history)
        self.history_widget.app_widget.show()

    def patch_host_checks(self, check_type, state):  # pragma: no cover
        """
        Patch the host check: 'active_checks_enabled' | 'passive_checks_enabled'

        :param check_type: type of check: 'active_checks_enabled' | 'passive_checks_enabled'
        :type check_type: str
        :param state: state of Toggle button
        :type state: bool
        """

        data = {check_type: state}
        headers = {'If-Match': self.host_item.data['_etag']}
        endpoint = '/'.join([self.host_item.item_type, self.host_item.item_id])

        patched = app_backend.patch(endpoint, data, headers)

        if patched:
            self.host_item.data[check_type] = state
            data_manager.update_item_data(
                self.host_item.item_type, self.host_item.item_id, self.host_item.data
            )
            enabled = _('enabled') if state else _('disabled')
            message = _(
                _("[%s] %s for %s" % (check_type, enabled, self.host_item.get_display_name()))
            )
            send_event('INFO', message, timer=True)
        else:
            send_event(
                'ERROR',
                _("Backend PATCH failed, please check your logs !")
            )

    def get_last_check_widget(self):
        """
        Return QWidget with last check data

        :return: widget with last check data
        :rtype: QWidget
        """

        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        # Title
        check_title = QLabel(_('My last check'))
        check_title.setObjectName('itemtitle')
        check_title.setFixedHeight(25)
        layout.addWidget(check_title, 0, 0, 1, 2)

        # State
        state_title = QLabel(_("State:"))
        state_title.setObjectName('subtitle')
        layout.addWidget(state_title, 1, 0, 1, 1)

        layout.addWidget(self.labels['state_icon'], 1, 1, 1, 1)

        # When last check
        when_title = QLabel(_("When:"))
        when_title.setObjectName('subtitle')
        layout.addWidget(when_title, 2, 0, 1, 1)

        layout.addWidget(self.labels['ls_last_check'], 2, 1, 1, 1)

        return widget

    def get_variables_widget(self):
        """
        Return QWidget with host variables

        :return: widget with host variables
        :rtype: QWidget
        """

        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        # Title
        check_title = QLabel(_('My variables'))
        check_title.setObjectName('itemtitle')
        check_title.setFixedHeight(25)
        layout.addWidget(check_title, 0, 0, 1, 2)

        # Realm
        realm_title = QLabel(_("Realm:"))
        realm_title.setObjectName('subtitle')
        layout.addWidget(realm_title, 1, 0, 1, 1)

        layout.addWidget(self.labels['realm'], 1, 1, 1, 1)

        # Address
        address_title = QLabel(_("Host address:"))
        address_title.setObjectName('subtitle')
        layout.addWidget(address_title, 2, 0, 1, 1)

        layout.addWidget(self.labels['address'], 2, 1, 1, 1)

        # Business impact
        business_title = QLabel(_("Business impact:"))
        business_title.setObjectName('subtitle')
        layout.addWidget(business_title, 3, 0, 1, 1)

        layout.addWidget(self.labels['business_impact'], 3, 1, 1, 1)

        return widget

    def get_notes_output_widget(self):
        """
        Return QWidget with output and notes data

        :return: widget with host output and notes
        :rtype: QWidget
        """

        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        # Output
        output_title = QLabel(_("Output"))
        output_title.setObjectName('title')
        layout.addWidget(output_title, 0, 0, 1, 1)

        self.labels['ls_output'].setWordWrap(True)
        self.labels['ls_output'].setTextInteractionFlags(Qt.TextSelectableByMouse)
        output_scrollarea = QScrollArea()
        output_scrollarea.setWidget(self.labels['ls_output'])
        output_scrollarea.setWidgetResizable(True)
        output_scrollarea.setObjectName('output')
        layout.addWidget(output_scrollarea, 1, 0, 1, 1)

        # Notes
        notes_title = QLabel(_("Notes:"))
        notes_title.setObjectName('title')
        layout.addWidget(notes_title, 0, 1, 1, 1)

        self.labels['notes'].setWordWrap(True)
        self.labels['notes'].setTextInteractionFlags(Qt.TextSelectableByMouse)
        notes_scrollarea = QScrollArea()
        notes_scrollarea.setWidget(self.labels['notes'])
        notes_scrollarea.setWidgetResizable(True)
        notes_scrollarea.setObjectName('notes')
        layout.addWidget(notes_scrollarea, 1, 1, 1, 1)

        return widget

    def update_host(self, hostname=None):
        """
        Update HostQWidget data and QLabels

        :param hostname: name of host who is display
        :type hostname: str
        """

        if self.host_item and not hostname:
            self.set_data(self.host_item.name)
        if hostname:
            self.set_data(hostname)

        if self.host_item or hostname:
            icon_name = get_real_host_state_icon(self.service_items)
            icon_pixmap = QPixmap(settings.get_image(icon_name))

            self.labels['host_icon'].setPixmap(QPixmap(icon_pixmap))
            self.labels['host_icon'].setToolTip(
                get_host_msg_and_event_type(
                    {'host': self.host_item, 'services': self.service_items}
                )['message']
            )
            self.labels['host_name'].setText('%s' % self.host_item.get_display_name())

            icon_name = get_icon_name(
                'host',
                self.host_item.data['ls_state'],
                self.host_item.data['ls_acknowledged'],
                self.host_item.data['ls_downtimed'],
                self.host_item.data['passive_checks_enabled'] +
                self.host_item.data['active_checks_enabled']
            )
            pixmap_icon = QPixmap(settings.get_image(icon_name))
            final_icon = pixmap_icon.scaled(32, 32, Qt.KeepAspectRatio)
            self.labels['state_icon'].setPixmap(final_icon)
            self.labels['state_icon'].setToolTip(self.host_item.get_tooltip())

            since_last_check = get_time_diff_since_last_timestamp(
                self.host_item.data['ls_last_check']
            )
            self.labels['ls_last_check'].setText(since_last_check)
            self.labels['ls_output'].setText(self.host_item.data['ls_output'])

            self.labels['realm'].setText(
                data_manager.get_realm_name(self.host_item.data['_realm'])
            )
            self.labels['address'].setText(self.host_item.data['address'])
            self.labels['business_impact'].setText(str(self.host_item.data['business_impact']))
            self.labels['notes'].setText(self.host_item.data['notes'])

            self.actions_widget.item = self.host_item
            self.actions_widget.update_widget()

            self.activecheck_btn.update_btn_state(self.host_item.data['active_checks_enabled'])
            self.passivecheck_btn.update_btn_state(self.host_item.data['passive_checks_enabled'])

            self.host_history = data_manager.get_item('history', self.host_item.item_id)
            if self.host_history:
                self.history_btn.setEnabled(True)
                self.history_btn.setToolTip(_('History is available'))
            else:
                self.history_btn.setToolTip(_('History is not available, please wait...'))
                self.history_btn.setEnabled(False)

                if app_backend.connected:
                    thread_manager.add_priority_thread(
                        'history',
                        {'hostname': self.host_item.name, 'host_id': self.host_item.item_id}
                    )
                else:
                    thread_manager.stop_threads()
