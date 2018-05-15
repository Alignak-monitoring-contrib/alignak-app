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

from PyQt5.Qt import QLabel, QWidget, QGridLayout, Qt, QPixmap, QVBoxLayout
from PyQt5.Qt import QPushButton, QIcon, QTimer, QScrollArea

from alignak_app.backend.backend import app_backend
from alignak_app.backend.datamanager import data_manager
from alignak_app.items.item import Item, get_icon_name, get_overall_state_icon
from alignak_app.utils.config import settings
from alignak_app.utils.time import get_diff_since_last_timestamp, get_date_fromtimestamp

from alignak_app.qobjects.common.actions import ActionsQWidget
from alignak_app.qobjects.common.buttons import ToggleQWidgetButton
from alignak_app.qobjects.common.dialogs import EditQDialog
from alignak_app.qobjects.events.events import send_event
from alignak_app.qobjects.host.history import HistoryQWidget
from alignak_app.qobjects.host.customs import CustomsQWidget

from alignak_app.qobjects.threads.threadmanager import thread_manager

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
        self.history_widget = HistoryQWidget()
        self.host_history = None
        self.customs_widget = CustomsQWidget()
        self.customs_btn = QPushButton()
        self.spy_btn = QPushButton()
        self.refresh_timer = QTimer()
        self.refresh_counter = 0

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

    def set_data(self, host_item):
        """
        Set data of host and service

        :param host_item: the Host item
        :type host_item: alignak_app.items.host.Host
        """

        # Query services of host
        self.host_item = host_item

        # Get problems
        host_and_services = data_manager.get_host_with_services(host_item.item_id)
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
        self.labels['host_name'].setWordWrap(True)
        layout.addWidget(self.labels['host_name'])
        layout.setAlignment(self.labels['host_name'], Qt.AlignCenter)

        # Customs button
        customs_lbl = QLabel(_('Configuration:'))
        customs_lbl.setObjectName('subtitle')
        layout.addWidget(customs_lbl)
        layout.setAlignment(customs_lbl, Qt.AlignBottom)
        self.customs_btn.setIcon(QIcon(settings.get_image('settings')))
        self.customs_btn.setFixedSize(80, 20)
        self.customs_btn.clicked.connect(self.show_customs)
        layout.addWidget(self.customs_btn)
        layout.setAlignment(self.customs_btn, Qt.AlignCenter)

        # Initialize Customs QWidget
        self.customs_widget.initialize()

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

        # Actions
        action_title = QLabel(_('Host actions'))
        action_title.setObjectName('itemtitle')
        action_title.setFixedHeight(25)
        layout.addWidget(action_title)

        ack_down_lbl = QLabel(_('Acknowledge / Downtime:'))
        ack_down_lbl.setObjectName('subtitle')
        layout.addWidget(ack_down_lbl)

        self.actions_widget.initialize(self.host_item)
        layout.addWidget(self.actions_widget)

        # Active Checks
        activecheck_lbl = QLabel(_('Active checks:'))
        activecheck_lbl.setObjectName('subtitle')
        layout.addWidget(activecheck_lbl)
        self.activecheck_btn.initialize()
        self.activecheck_btn.toggle_btn.clicked.connect(lambda: self.patch_host_checks(
            'active_checks_enabled', self.activecheck_btn.is_checked()
        ))
        layout.addWidget(self.activecheck_btn)

        # Passive Checks
        passivecheck_lbl = QLabel(_('Passive checks:'))
        passivecheck_lbl.setObjectName('subtitle')
        layout.addWidget(passivecheck_lbl)
        self.passivecheck_btn.initialize()
        self.passivecheck_btn.toggle_btn.clicked.connect(lambda: self.patch_host_checks(
            'passive_checks_enabled', self.passivecheck_btn.is_checked()
        ))
        layout.addWidget(self.passivecheck_btn)

        # History
        hist_lbl = QLabel(_('Timeline:'))
        hist_lbl.setObjectName('subtitle')
        layout.addWidget(hist_lbl)
        self.history_btn.setIcon(QIcon(settings.get_image('time')))
        self.history_btn.setFixedSize(80, 20)
        self.history_btn.clicked.connect(self.show_history)
        self.history_btn.setToolTip(_('See history of host'))
        layout.addWidget(self.history_btn)
        layout.setAlignment(self.history_btn, Qt.AlignCenter)

        self.history_widget.initialize()

        # Spy Button
        spy_lbl = QLabel(_('Spy Host:'))
        spy_lbl.setObjectName('subtitle')
        layout.addWidget(spy_lbl)
        self.spy_btn.setIcon(QIcon(settings.get_image('spy')))
        self.spy_btn.setFixedSize(80, 20)
        self.spy_btn.setToolTip(_('Spy current host'))
        layout.addWidget(self.spy_btn)
        layout.setAlignment(self.spy_btn, Qt.AlignCenter)

        layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        return widget

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
        layout.addWidget(output_scrollarea, 1, 0, 1, 2)

        # Notes
        notes_title = QLabel(_("Notes:"))
        notes_title.setObjectName('title')
        layout.addWidget(notes_title, 0, 2, 1, 1)

        notes_btn = QPushButton()
        notes_btn.setIcon(QIcon(settings.get_image('edit')))
        notes_btn.setToolTip(_("Edit host notes."))
        notes_btn.setFixedSize(32, 32)
        notes_btn.clicked.connect(self.patch_data)
        layout.addWidget(notes_btn, 0, 3, 1, 1)

        self.labels['notes'].setWordWrap(True)
        self.labels['notes'].setTextInteractionFlags(Qt.TextSelectableByMouse)
        notes_scrollarea = QScrollArea()
        notes_scrollarea.setWidget(self.labels['notes'])
        notes_scrollarea.setWidgetResizable(True)
        notes_scrollarea.setObjectName('notes')
        layout.addWidget(notes_scrollarea, 1, 2, 1, 2)

        return widget

    def show_history(self):
        """
        Update and show HistoryQWidget

        """

        self.history_widget.update_history_data(self.host_item.name, self.host_history)
        self.history_widget.show()

    def show_customs(self):
        """
        Update and show CustomsQWidget

        """

        self.customs_widget.update_customs(self.host_item)
        self.customs_widget.show()

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
            event_type = 'OK' if state else 'WARN'
            message = _(
                _('%s %s for %s' %
                  (Item.get_check_text(check_type), enabled, self.host_item.get_display_name()))
            )
            send_event(event_type, message, timer=True)
        else:
            send_event(
                'ERROR',
                _("Backend PATCH failed, please check your logs !")
            )

    def patch_data(self):  # pragma: no cover
        """
        Display QDialog for patch

        """

        notes_dialog = EditQDialog()
        notes_dialog.initialize(
            _('Edit Host Notes'),
            self.host_item.data['notes']
        )

        if notes_dialog.exec_() == EditQDialog.Accepted:
            data = {'notes': str(notes_dialog.text_edit.toPlainText())}
            headers = {'If-Match': self.host_item.data['_etag']}
            endpoint = '/'.join(['host', self.host_item.item_id])

            patched = app_backend.patch(endpoint, data, headers)

            if patched:
                data_manager.update_item_data(
                    self.host_item.item_type,
                    self.host_item.item_id,
                    {'notes': notes_dialog.text_edit.toPlainText()}
                )
                self.labels['notes'].setText(notes_dialog.text_edit.toPlainText())
                message = _(
                    _("Host notes have been edited.")
                )
                send_event('INFO', message)
            else:
                send_event(
                    'ERROR',
                    _("Backend PATCH failed, please check your logs !")
                )

    def update_host(self, host_item=None):
        """
        Update HostQWidget data and QLabels

        :param host_item: the Host item
        :type host_item: alignak_app.items.host.Host
        """

        if self.host_item and not host_item:
            self.set_data(self.host_item)
        if host_item:
            self.set_data(host_item)

        if self.host_item or host_item:
            # Update host services
            self.refresh_counter += 1
            if self.refresh_counter > 10:
                thread_manager.add_high_priority_thread('service', self.host_item.item_id)
                self.refresh_counter = 0

            # Update host
            icon_name = get_overall_state_icon(
                self.service_items,
                self.host_item.data['_overall_state_id']
            )
            icon_pixmap = QPixmap(settings.get_image(icon_name))

            self.labels['host_icon'].setPixmap(QPixmap(icon_pixmap))
            self.labels['host_icon'].setToolTip(
                self.host_item.get_overall_tooltip(self.service_items)
            )
            self.labels['host_name'].setText('%s' % self.host_item.get_display_name())

            monitored = self.host_item.data[
                'passive_checks_enabled'] + self.host_item.data['active_checks_enabled']
            icon_name = get_icon_name(
                'host',
                self.host_item.data['ls_state'],
                self.host_item.data['ls_acknowledged'],
                self.host_item.data['ls_downtimed'],
                monitored
            )
            pixmap_icon = QPixmap(settings.get_image(icon_name))
            final_icon = pixmap_icon.scaled(32, 32, Qt.KeepAspectRatio)
            self.labels['state_icon'].setPixmap(final_icon)
            self.labels['state_icon'].setToolTip(self.host_item.get_tooltip())

            since_last_check = get_diff_since_last_timestamp(
                self.host_item.data['ls_last_check']
            )
            last_check_tooltip = get_date_fromtimestamp(self.host_item.data['ls_last_check'])

            self.labels['ls_last_check'].setText(since_last_check)
            self.labels['ls_last_check'].setToolTip(last_check_tooltip)
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
            self.customs_btn.setEnabled(bool(self.host_item.data['customs']))

            # Update host history
            self.host_history = data_manager.get_item('history', self.host_item.item_id)
            if self.host_history:
                self.history_btn.setEnabled(True)
                self.history_btn.setToolTip(_('History is available'))
            else:
                self.history_btn.setToolTip(_('History is not available, please wait...'))
                self.history_btn.setEnabled(False)

                if app_backend.connected:
                    thread_manager.add_high_priority_thread(
                        'history',
                        {'hostname': self.host_item.name, 'host_id': self.host_item.item_id}
                    )
                else:
                    thread_manager.stop_threads()
