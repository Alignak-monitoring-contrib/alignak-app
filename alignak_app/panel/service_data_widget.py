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
    TODO
"""

from logging import getLogger

from alignak_app.core.utils import get_image_path, get_css, get_time_diff_since_last_timestamp
from alignak_app.core.backend import app_backend
from alignak_app.core.data_manager import data_manager
from alignak_app.models.item_model import get_icon_item
from alignak_app.panel.actions import AckQDialog, DownQDialog, QDialog
from alignak_app.dock.events_widget import events_widget

from PyQt5.Qt import QLabel, QWidget, QIcon, Qt, QPushButton  # pylint: disable=no-name-in-module
from PyQt5.Qt import QPixmap, QVBoxLayout, QGridLayout  # pylint: disable=no-name-in-module
from PyQt5.Qt import QTreeWidget, QTreeWidgetItem  # pylint: disable=no-name-in-module

logger = getLogger(__name__)


class ServiceDataQWidget(QWidget):
    """
        TODO
    """

    def __init__(self, parent=None):
        super(ServiceDataQWidget, self).__init__(parent)
        self.setStyleSheet(get_css())
        self.setFixedWidth(200)
        # Fields
        self.service_item = None
        self.host_id = None
        self.labels = {
            'service_icon': QLabel(),
            'service_name': QLabel(),
            'ls_last_check': QLabel(),
            'ls_output': QLabel(),
            'business_impact': QLabel(),
        }
        self.buttons = {
            'acknowledge': QPushButton(),
            'downtime': QPushButton()
        }

    def initialize(self):
        """
        Initialize QWidget

        """

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(self.get_icon_widget())
        layout.addWidget(self.get_last_check_widget())
        layout.addWidget(self.get_actions_widget())
        self.hide()

    def get_icon_widget(self):
        """
        Return QWidget with its icon and name

        :return: widget with icon and name
        :rtype: QWidget
        """

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Host Icon
        layout.addWidget(self.labels['service_icon'])
        layout.setAlignment(self.labels['service_icon'], Qt.AlignCenter)

        # Host Name
        self.labels['service_name'].setObjectName('hostname')
        layout.addWidget(self.labels['service_name'])
        layout.setAlignment(self.labels['service_name'], Qt.AlignCenter)

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
        check_title = QLabel('My last check')
        check_title.setObjectName('hosttitle')
        check_title.setFixedHeight(30)
        layout.addWidget(check_title, 0, 0, 1, 2)

        # When last check
        when_title = QLabel("When:")
        when_title.setObjectName('title')
        layout.addWidget(when_title, 2, 0, 1, 1)

        layout.addWidget(self.labels['ls_last_check'], 2, 1, 1, 1)

        # Output
        output_title = QLabel("Output")
        output_title.setObjectName('title')
        output_title.setWordWrap(True)
        layout.addWidget(output_title, 3, 0, 1, 1)

        self.labels['ls_output'].setObjectName('output')
        layout.addWidget(self.labels['ls_output'], 3, 1, 1, 1)

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

        self.buttons['acknowledge'].setIcon(QIcon(get_image_path('acknowledge')))
        self.buttons['acknowledge'].clicked.connect(
            lambda: self.add_acknowledge(self.service_item, self.host_id)
        )
        layout.addWidget(self.buttons['acknowledge'])

        self.buttons['downtime'].setIcon(QIcon(get_image_path('downtime')))
        self.buttons['downtime'].clicked.connect(
            lambda: self.add_downtime(self.service_item, self.host_id)
        )
        layout.addWidget(self.buttons['downtime'])

        layout.setAlignment(Qt.AlignCenter)

        return widget

    def add_acknowledge(self, service_item, host_id):
        """
        Create AckQDialog and manage acknowledge

        :param service_item: Service item
        :type service_item: alignak_app.models.item_host.Service
        :param host_id: id of attached host
        :type host_id: str
        """

        user = data_manager.database['user']

        comment = _('Service %s acknowledged by %s, from Alignak-app') % (
            service_item.name,
            user.name
        )

        ack_dialog = AckQDialog()
        ack_dialog.initialize('service', service_item.name, comment)

        if ack_dialog.exec_() == QDialog.Accepted:
            sticky = ack_dialog.sticky
            notify = ack_dialog.notify
            comment = str(ack_dialog.ack_comment_edit.toPlainText())

            data = {
                'action': 'add',
                'host': host_id,
                'service': service_item.item_id,
                'user': user.item_id,
                'comment': comment,
                'notify': notify,
                'sticky': sticky
            }

            post = app_backend.post('actionacknowledge', data)

            events_widget.add_event('OK', 'Acknowledge for %s is done' % service_item.name)
            logger.debug('ACK answer for %s: %s', service_item.name, post)

            try:
                self.buttons['acknowledge'].setEnabled(False)
            except RuntimeError as e:
                logger.warning('Can\'t disable Acknowledge btn: %s', e)
        else:
            logger.info('Acknowledge for %s cancelled...', service_item.name)

    def add_downtime(self, service_item, host_id):
        """
        Create AckQDialog and manage acknowledge

        :param service_item: Service item
        :type service_item: alignak_app.models.item_host.Service
        :param host_id: id of attached host
        :type host_id: str
        """

        user = data_manager.database['user']

        comment = _('Downtime on %s by %s, from Alignak-app') % (service_item.name, user.name)

        downtime_dialog = DownQDialog()
        downtime_dialog.initialize('service', service_item.name, comment)

        if downtime_dialog.exec_() == QDialog.Accepted:
            fixed = downtime_dialog.fixed
            duration = downtime_dialog.duration_to_seconds()
            start_stamp = downtime_dialog.start_time.dateTime().toTime_t()
            end_stamp = downtime_dialog.end_time.dateTime().toTime_t()
            comment = downtime_dialog.comment_edit.toPlainText()

            data = {
                'action': 'add',
                'host': host_id,
                'service': service_item.item_id,
                'user': user.item_id,
                'fixed': fixed,
                'duration': duration,
                'start_time': start_stamp,
                'end_time': end_stamp,
                'comment': comment,
            }

            post = app_backend.post('actiondowntime', data)

            events_widget.add_event('OK', 'Downtime for %s is done' % service_item.name)
            logger.debug('DOWN answer for %s: %s', service_item.name, post)

            try:
                self.buttons['downtime'].setEnabled(False)
            except RuntimeError as e:
                logger.warning('Can\'t disable Downtime btn: %s', e)
        else:
            logger.info('Downtime for %s cancelled...', service_item.name)

    def update_widget(self, service, host_id):
        """
        Update ServiceDataQWidget

        :param service: Service item with its data
        :type service: alignak_app.models.item_service.Service
        :param host_id: id of attached host
        :type host_id: str
        """

        self.service_item = service
        self.host_id = host_id

        icon_name = get_icon_item(
            'service',
            self.service_item.data['ls_state'],
            self.service_item.data['ls_acknowledged'],
            self.service_item.data['ls_downtimed']
        )
        icon_pixmap = QPixmap(get_image_path(icon_name))

        self.labels['service_icon'].setPixmap(QPixmap(icon_pixmap))
        self.labels['service_name'].setText('%s' % self.service_item.name)

        since_last_check = get_time_diff_since_last_timestamp(
            self.service_item.data['ls_last_check']
        )
        self.labels['ls_last_check'].setText(since_last_check)
        self.labels['ls_output'].setText(self.service_item.data['ls_output'])

        self.labels['business_impact'].setText(str(self.service_item.data['business_impact']))

        if self.service_item.data['ls_acknowledged'] or 'UP' in self.service_item.data['ls_state'] \
                or not data_manager.database['user'].data['can_submit_commands']:
            self.buttons['acknowledge'].setEnabled(False)
        else:
            self.buttons['acknowledge'].setEnabled(True)

        if self.service_item.data['ls_downtimed'] \
                or not data_manager.database['user'].data['can_submit_commands']:
            self.buttons['downtime'].setEnabled(False)
        else:
            self.buttons['downtime'].setEnabled(True)

        self.show()
