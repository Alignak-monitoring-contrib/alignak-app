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
    Host QWidget manage display of host data
"""

from logging import getLogger

from PyQt5.Qt import QLabel, QWidget, QGridLayout, Qt, QPixmap, QVBoxLayout, QHBoxLayout
from PyQt5.Qt import QPushButton, QIcon

from alignak_app.core.backend import app_backend
from alignak_app.core.data_manager import data_manager
from alignak_app.core.items.model import get_icon_name, get_real_host_state_icon
from alignak_app.core.config import get_image, app_css
from alignak_app.core.app_time import get_time_diff_since_last_timestamp
from alignak_app.widgets.dialogs.actions import AckQDialog, DownQDialog, QDialog
from alignak_app.widgets.dock.events import send_event
from alignak_app.widgets.panel.history import HistoryQWidget

logger = getLogger(__name__)


class HostQWidget(QWidget):
    """
        Class who create QWidget to display host data
    """

    def __init__(self, parent=None):
        super(HostQWidget, self).__init__(parent)
        self.setStyleSheet(app_css)
        # Fields
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
        self.buttons = {
            'acknowledge': QPushButton(),
            'downtime': QPushButton(),
            'history': QPushButton()
        }
        self.history_widget = None

    def set_data(self, hostname):
        """
        Set data of host and service

        :param hostname: name of host to display
        :type hostname: str
        """

        host_and_services = data_manager.get_host_with_services(hostname)
        self.host_item = host_and_services['host']
        self.service_items = host_and_services['services']

    def initialize(self):
        """
        Initialize QWidget

        """

        layout = QHBoxLayout()
        self.setLayout(layout)

        # Add Qwidgets
        layout.addWidget(self.get_host_icon_widget())

        layout.addWidget(self.get_actions_widget())

        layout.addWidget(self.get_last_check_widget())

        layout.addWidget(self.get_variables_widget())

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

        action_title = QLabel('Actions:')
        action_title.setObjectName('title')
        layout.addWidget(action_title)

        self.buttons['acknowledge'].setIcon(QIcon(get_image('acknowledge')))
        self.buttons['acknowledge'].clicked.connect(lambda: self.add_acknowledge(self.host_item))
        layout.addWidget(self.buttons['acknowledge'])

        self.buttons['downtime'].setIcon(QIcon(get_image('downtime')))
        self.buttons['downtime'].clicked.connect(lambda: self.add_downtime(self.host_item))
        layout.addWidget(self.buttons['downtime'])

        self.buttons['history'].setIcon(QIcon(get_image('time')))
        self.buttons['history'].clicked.connect(self.show_history)
        layout.addWidget(self.buttons['history'])

        layout.setAlignment(Qt.AlignCenter)

        return widget

    def add_acknowledge(self, host_item):  # pragma: no cover
        """
        Create AckQDialog and manage acknowledge

        :param host_item: Host item
        :type host_item: alignak_app.models.item_host.Host
        """

        user = data_manager.database['user']

        comment = _('Host %s acknowledged by %s, from Alignak-app') % (
            host_item.name,
            user.name
        )

        ack_dialog = AckQDialog()
        ack_dialog.initialize('host', host_item.name, comment)

        if ack_dialog.exec_() == QDialog.Accepted:
            sticky = ack_dialog.sticky
            notify = ack_dialog.notify
            comment = str(ack_dialog.ack_comment_edit.toPlainText())

            data = {
                'action': 'add',
                'host': host_item.item_id,
                'service': None,
                'user': user.item_id,
                'comment': comment,
                'notify': notify,
                'sticky': sticky
            }

            post = app_backend.post('actionacknowledge', data)

            send_event('ACK', 'Acknowledge for %s is done' % host_item.name)
            data_manager.update_item_data(
                'host',
                host_item.item_id,
                {'ls_acknowledged': True}
            )
            logger.debug('ACK answer for %s: %s', host_item.name, post)

            try:
                self.buttons['acknowledge'].setEnabled(False)
            except RuntimeError as e:
                logger.warning('Can\'t disable Acknowledge btn: %s', e)
        else:
            logger.info('Acknowledge for %s cancelled...', host_item.name)

    def add_downtime(self, host_item):  # pragma: no cover
        """
        Create AckQDialog and manage acknowledge

        :param host_item: Host item
        :type host_item: alignak_app.models.item_host.Host
        """

        user = data_manager.database['user']

        comment = _('Schedule downtime by %s, from Alignak-app') % user.name

        downtime_dialog = DownQDialog()
        downtime_dialog.initialize('host', host_item.name, comment)

        if downtime_dialog.exec_() == QDialog.Accepted:
            fixed = downtime_dialog.fixed
            duration = downtime_dialog.duration_to_seconds()
            start_stamp = downtime_dialog.start_time.dateTime().toTime_t()
            end_stamp = downtime_dialog.end_time.dateTime().toTime_t()
            comment = downtime_dialog.comment_edit.toPlainText()

            data = {
                'action': 'add',
                'host': host_item.item_id,
                'service': None,
                'user': user.item_id,
                'fixed': fixed,
                'duration': duration,
                'start_time': start_stamp,
                'end_time': end_stamp,
                'comment': comment,
            }

            post = app_backend.post('actiondowntime', data)

            send_event('DOWNTIME', 'Downtime for %s is done' % host_item.name)
            data_manager.update_item_data(
                'host',
                host_item.item_id,
                {'ls_downtimed': True}
            )
            logger.debug('DOWNTIME answer for %s: %s', host_item.name, post)

            try:
                self.buttons['downtime'].setEnabled(False)
            except RuntimeError as e:
                logger.warning('Can\'t disable Downtime btn: %s', e)
        else:
            logger.info('Downtime for %s cancelled...', host_item.name)

    def show_history(self):
        """
        Create and show HistoryQWidget

        """

        self.history_widget = HistoryQWidget(self)
        self.history_widget.initialize(self.host_item.name, self.host_item.item_id)
        self.history_widget.app_widget.show()

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
        check_title = QLabel('My last check')
        check_title.setObjectName('itemtitle')
        check_title.setFixedHeight(30)
        layout.addWidget(check_title, 0, 0, 1, 2)

        # State
        state_title = QLabel("State:")
        state_title.setObjectName('title')
        layout.addWidget(state_title, 1, 0, 1, 1)

        layout.addWidget(self.labels['state_icon'], 1, 1, 1, 1)

        # When last check
        when_title = QLabel("When:")
        when_title.setObjectName('title')
        layout.addWidget(when_title, 2, 0, 1, 1)

        layout.addWidget(self.labels['ls_last_check'], 2, 1, 1, 1)

        # Output
        output_title = QLabel("Output")
        output_title.setObjectName('title')
        layout.addWidget(output_title, 3, 0, 1, 1)

        self.labels['ls_output'].setObjectName('output')
        self.labels['ls_output'].setWordWrap(True)
        layout.addWidget(self.labels['ls_output'], 3, 1, 1, 1)

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
        check_title = QLabel('My variables')
        check_title.setObjectName('itemtitle')
        check_title.setFixedHeight(30)
        layout.addWidget(check_title, 0, 0, 1, 2)

        # Realm
        realm_title = QLabel("Realm:")
        realm_title.setObjectName('title')
        layout.addWidget(realm_title, 1, 0, 1, 1)

        layout.addWidget(self.labels['realm'], 1, 1, 1, 1)

        # Address
        address_title = QLabel("Host address:")
        address_title.setObjectName('title')
        layout.addWidget(address_title, 2, 0, 1, 1)

        layout.addWidget(self.labels['address'], 2, 1, 1, 1)

        # Business impact
        address_title = QLabel("Business impact:")
        address_title.setObjectName('title')
        layout.addWidget(address_title, 3, 0, 1, 1)

        layout.addWidget(self.labels['business_impact'], 3, 1, 1, 1)

        # Notes
        notes_title = QLabel("Notes:")
        notes_title.setObjectName('title')
        layout.addWidget(notes_title, 4, 0, 1, 1)

        self.labels['notes'].setWordWrap(True)
        layout.addWidget(self.labels['notes'], 4, 1, 1, 1)

        return widget

    def update_widget(self, hostname):
        """
        Update HostQWidget data and QLabels

        """

        self.set_data(hostname)

        icon_name = get_real_host_state_icon(self.service_items)
        icon_pixmap = QPixmap(get_image(icon_name))

        self.labels['host_icon'].setPixmap(QPixmap(icon_pixmap))
        self.labels['host_name'].setText('%s' % self.host_item.name.capitalize())

        icon_name = get_icon_name(
            'host',
            self.host_item.data['ls_state'],
            self.host_item.data['ls_acknowledged'],
            self.host_item.data['ls_downtimed']
        )
        pixmap_icon = QPixmap(get_image(icon_name))
        final_icon = pixmap_icon.scaled(32, 32, Qt.KeepAspectRatio)
        self.labels['state_icon'].setPixmap(final_icon)

        since_last_check = get_time_diff_since_last_timestamp(
            self.host_item.data['ls_last_check']
        )
        self.labels['ls_last_check'].setText(since_last_check)
        self.labels['ls_output'].setText(self.host_item.data['ls_output'])

        self.labels['realm'].setText(self.host_item.data['_realm'])
        self.labels['address'].setText(self.host_item.data['address'])
        self.labels['business_impact'].setText(str(self.host_item.data['business_impact']))
        self.labels['notes'].setText(self.host_item.data['notes'])

        if self.host_item.data['ls_acknowledged'] or 'UP' in self.host_item.data['ls_state'] \
                or not data_manager.database['user'].data['can_submit_commands']:
            self.buttons['acknowledge'].setEnabled(False)
        else:
            self.buttons['acknowledge'].setEnabled(True)

        if self.host_item.data['ls_downtimed'] \
                or not data_manager.database['user'].data['can_submit_commands']:
            self.buttons['downtime'].setEnabled(False)
        else:
            self.buttons['downtime'].setEnabled(True)

        if any(
                history_item.item_id == self.host_item.item_id for
                history_item in data_manager.database['history']):
            self.buttons['history'].setEnabled(True)
            self.buttons['history'].setToolTip(_('History is available'))
        else:
            self.buttons['history'].setToolTip(_('History is not available, please wait...'))
            self.buttons['history'].setEnabled(False)
