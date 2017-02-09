#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016:
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
    Host Synthesis display data of choosen host in Synthesis
"""

import datetime

from logging import getLogger

from alignak_app.core.utils import get_image_path, get_diff_since_last_check
from alignak_app.core.action_manager import ACK, DOWNTIME, PROCESS
from alignak_app.widgets.banner import send_banner
from alignak_app.synthesis.service import Service

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QApplication  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QPushButton, QLabel  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout, QVBoxLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QStackedWidget, QScrollArea  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QIcon, QPixmap, QListWidget  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QTimer, QListWidgetItem, Qt, QCheckBox  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QApplication  # pylint: disable=import-error
    from PyQt4.Qt import QWidget, QPushButton, QLabel  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout, QVBoxLayout  # pylint: disable=import-error
    from PyQt4.Qt import QStackedWidget, QScrollArea  # pylint: disable=import-error
    from PyQt4.Qt import QIcon, QPixmap, QListWidget  # pylint: disable=import-error
    from PyQt4.Qt import QTimer, QListWidgetItem, Qt, QCheckBox  # pylint: disable=import-error


logger = getLogger(__name__)


class HostSynthesis(QWidget):
    """
        Class who create the HostSynthesis QWidget for host and its services.
    """

    def __init__(self, app_backend, action_manager, parent=None):
        super(HostSynthesis, self).__init__(parent)
        self.app_backend = app_backend
        self.action_manager = action_manager
        self.host = {}
        self.stack = None
        self.services_list = None
        self.check_boxes = {}

    def initialize(self, backend_data):
        """
        Inititalize the QWidget

        """

        if backend_data:
            main_layout = QVBoxLayout(self)
            self.host = backend_data['host']

            host_widget = self.get_host_widget(backend_data)
            main_layout.addWidget(host_widget)
            main_layout.setAlignment(host_widget, Qt.AlignCenter)

            main_layout.addWidget(self.get_services_widget(backend_data))

            action_timer = QTimer(self)
            action_timer.start(4000)
            action_timer.timeout.connect(self.check_action_manager)

    def get_host_widget(self, backend_data):
        """
        Return QWidget for host

        :param backend_data: data of AppBackend
        :type backend_data: dict
        :return: QWidget with with host data
        :rtype: QWidget
        """

        host_widget = QWidget()
        host_layout = QGridLayout(host_widget)

        # Overall State
        host_services_status = QLabel('Host Services Status')
        host_layout.addWidget(host_services_status, 0, 0, 1, 1)

        host_overall_state = QLabel()
        host_overall_state.setPixmap(self.get_real_state_icon(backend_data['services']))
        host_overall_state.setFixedSize(72, 72)
        host_overall_state.setScaledContents(True)
        host_layout.addWidget(host_overall_state, 1, 0, 1, 1)

        # Hostname
        host_name = QLabel('<h2>%s</h2>' % backend_data['host']['alias'])
        host_layout.addWidget(host_name, 2, 0, 1, 1)

        # Real State
        host_real_state = QLabel()
        host_real_state.setPixmap(self.get_host_icon(backend_data['host']['ls_state']))
        host_real_state.setFixedSize(48, 48)
        host_real_state.setScaledContents(True)
        host_layout.addWidget(host_real_state, 3, 0, 1, 1)

        real_state = QLabel('Host real state, excluding services')
        host_layout.addWidget(real_state, 4, 0, 1, 1)

        # Buttons
        self.create_buttons(host_layout, backend_data)
        self.create_host_details(host_layout, backend_data)

        return host_widget

    @staticmethod
    def create_host_details(host_layout, backend_data):
        """
        Create QLabels for host details

        :param host_layout: layout of QWidget
        :type host_layout: QGridLayout
        :param backend_data: data of AppBackend
        :type backend_data: dict
        """

        # Host details
        acknowledge = QLabel('<b>Acknowledged:</b> %s' % backend_data['host']['ls_acknowledged'])
        host_layout.addWidget(acknowledge, 0, 2, 1, 1)

        downtime = QLabel('<b>Downtimed:</b> %s' % backend_data['host']['ls_downtimed'])
        host_layout.addWidget(downtime, 1, 2, 1, 1)

        diff_last_check = get_diff_since_last_check(backend_data['host']['ls_last_check'])
        host_last_check = QLabel('<b>Last check:</b> %s' % str(diff_last_check))
        host_layout.addWidget(host_last_check, 2, 2, 1, 1)

        output = QLabel(backend_data['host']['ls_output'])
        output.setObjectName('output')
        output.setTextInteractionFlags(Qt.TextSelectableByMouse)
        scroll = QScrollArea()
        scroll.setWidget(output)
        scroll.setObjectName('output')
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setMinimumWidth(500)
        scroll.setMaximumHeight(60)
        host_layout.addWidget(scroll, 3, 2, 1, 2)

        alias = QLabel('<b>Alias:</b> %s' % backend_data['host']['alias'])
        host_layout.addWidget(alias, 0, 3, 1, 1)

        address = QLabel('<b>Address:</b> %s' % backend_data['host']['address'])
        host_layout.addWidget(address, 1, 3, 1, 1)

        business_impact = QLabel('<b>Importance:</b> %s' % backend_data['host']['business_impact'])
        host_layout.addWidget(business_impact, 2, 3, 1, 1)

        parents = QLabel('<b>Parents:</b> %s' % backend_data['host']['parents'])
        host_layout.addWidget(parents, 0, 4, 1, 1)

    def create_buttons(self, host_layout, backend_data):
        """
        Create QPushButtons for Acknowledge and Donwtime actions

        :param host_layout: layout of QWidget
        :type host_layout: QGridLayout
        :param backend_data: data of AppBackend
        :type backend_data: dict
        """

        # ACK
        acknowledge_btn = QPushButton()
        acknowledge_btn.setObjectName(
            'host:%s:%s' % (backend_data['host']['_id'], backend_data['host']['name'])
        )
        acknowledge_btn.setIcon(QIcon(get_image_path('acknowledged')))
        acknowledge_btn.setFixedSize(32, 32)
        acknowledge_btn.setToolTip('Acknowledge this host')
        acknowledge_btn.clicked.connect(self.add_acknowledge)
        if 'UP' in backend_data['host']['ls_state'] \
                or backend_data['host']['ls_acknowledged'] \
                or backend_data['host']['_id'] in self.action_manager.acknowledged:
            acknowledge_btn.setEnabled(False)
        host_layout.addWidget(acknowledge_btn, 0, 1, 1, 1)

        # DOWN
        downtime_btn = QPushButton()
        downtime_btn.setObjectName(
            'host:%s:%s' % (backend_data['host']['_id'], backend_data['host']['name'])
        )
        downtime_btn.setIcon(QIcon(get_image_path('downtime')))
        downtime_btn.setFixedSize(32, 32)
        downtime_btn.setToolTip('Schedule a downtime for this host')
        downtime_btn.clicked.connect(self.add_downtime)
        if 'UP' in backend_data['host']['ls_state'] \
                or backend_data['host']['ls_downtimed'] \
                or backend_data['host']['_id'] in self.action_manager.downtimed:
            downtime_btn.setEnabled(False)
        host_layout.addWidget(downtime_btn, 1, 1, 1, 1)

    def sort_services_list(self):
        """
        Sort services. If State is check, services with this state are displayed. Else they not.

        """

        for i in range(self.services_list.count()):
            if self.sender().objectName() in self.services_list.item(i).text():
                if self.sender().isChecked():
                    self.services_list.item(i).setHidden(False)
                else:
                    self.services_list.item(i).setHidden(True)

    def get_services_widget(self, backend_data):
        """
        Return QWidget for services

        :param backend_data: data of AppBackend
        :type backend_data: dict
        :return: QWidget with Service in QStackedWidget
        :rtype: QWidget
        """

        services_widget = QWidget()
        services_layout = QGridLayout(services_widget)

        self.check_boxes['OK'] = QCheckBox('OK')
        self.check_boxes['OK'].setObjectName('OK')
        self.check_boxes['OK'].setChecked(True)
        self.check_boxes['OK'].stateChanged.connect(self.sort_services_list)
        services_layout.addWidget(self.check_boxes['OK'], 0, 0, 1, 1)

        self.check_boxes['UNKNOWN'] = QCheckBox('UNKNOWN')
        self.check_boxes['UNKNOWN'].setObjectName('UNKNOWN')
        self.check_boxes['UNKNOWN'].setChecked(True)
        self.check_boxes['UNKNOWN'].stateChanged.connect(self.sort_services_list)
        services_layout.addWidget(self.check_boxes['UNKNOWN'], 0, 1, 1, 1)

        self.check_boxes['WARNING'] = QCheckBox('WARNING')
        self.check_boxes['WARNING'].setObjectName('WARNING')
        self.check_boxes['WARNING'].setChecked(True)
        self.check_boxes['WARNING'].stateChanged.connect(self.sort_services_list)
        services_layout.addWidget(self.check_boxes['WARNING'], 0, 2, 1, 1)

        self.check_boxes['UNREACHABLE'] = QCheckBox('UNREACHABLE')
        self.check_boxes['UNREACHABLE'].setObjectName('UNREACHABLE')
        self.check_boxes['UNREACHABLE'].setChecked(True)
        self.check_boxes['UNREACHABLE'].stateChanged.connect(self.sort_services_list)
        services_layout.addWidget(self.check_boxes['UNREACHABLE'], 0, 3, 1, 1)

        self.check_boxes['CRITICAL'] = QCheckBox('CRITICAL')
        self.check_boxes['CRITICAL'].setObjectName('CRITICAL')
        self.check_boxes['CRITICAL'].setChecked(True)
        self.check_boxes['CRITICAL'].stateChanged.connect(self.sort_services_list)
        services_layout.addWidget(self.check_boxes['CRITICAL'], 0, 4, 1, 1)

        # Init Vars
        self.stack = QStackedWidget()
        self.services_list = QListWidget()

        services_layout.addWidget(self.services_list, 1, 0, 1, 5)
        services_layout.addWidget(self.stack, 2, 0, 1, 5)

        pos = 0
        for service in backend_data['services']:
            # Service QWidget
            service_widget = Service()
            service_widget.initialize(service)

            # Connect ACK button
            service_widget.acknowledge_btn.clicked.connect(self.add_acknowledge)
            service_widget.acknowledge_btn.setObjectName(
                'service:%s:%s' % (service['_id'], service['display_name'])
            )
            if 'OK' in service['ls_state'] \
                    or service['ls_acknowledged'] \
                    or service['_id'] in self.action_manager.acknowledged:
                service_widget.acknowledge_btn.setEnabled(False)

            # Connect DOWN button
            service_widget.downtime_btn.clicked.connect(self.add_downtime)
            service_widget.downtime_btn.setObjectName(
                'service:%s:%s' % (service['_id'], service['display_name'])
            )
            if 'OK' in service['ls_state'] \
                    or service['ls_downtimed'] \
                    or service['_id'] in self.action_manager.downtimed:
                service_widget.downtime_btn.setEnabled(False)

            # Add widget to QStackedWidget
            self.stack.addWidget(service_widget)

            # Add item to QListWidget
            list_item = QListWidgetItem()
            list_item.setText('%s: %s' % (service['display_name'], service['ls_state']))
            list_item.setIcon(
                QIcon(get_image_path('services_%s' % service['ls_state']))
            )
            self.services_list.addItem(list_item)
            self.services_list.insertItem(pos, list_item)

            pos += 1

        self.services_list.currentRowChanged.connect(self.display_current_service)

        return services_widget

    def display_current_service(self, index):
        """
        Display the current selected Service QWidget

        :param index: index of QStackedWidget
        :type index: int
        """

        self.stack.setCurrentIndex(index)

    def add_acknowledge(self):  # pragma: no cover, no testability
        """
        Handle action for "acknowledge_btn"

        """

        # Get who emit SIGNAL
        item_type = str(self.sender().objectName().split(':')[0])

        if self.host:
            host_id = self.host['_id']

            if 'service' in item_type:
                service_id = str(self.sender().objectName().split(':')[1])
                self.action_manager.acknowledged.append(service_id)
            else:
                service_id = None
                self.action_manager.acknowledged.append(host_id)

            user = self.app_backend.get_user()

            comment = '%s %s acknowledged by %s, from Alignak-app' % (
                item_type.capitalize(),
                str(self.sender().objectName().split(':')[2]),
                user['name']
            )

            data = {
                'action': 'add',
                'host': host_id,
                'service': service_id,
                'user': user['_id'],
                'comment': comment
            }

            post = self.app_backend.post(ACK, data)
            item_process = {
                'action': PROCESS,
                'name': str(self.sender().objectName().split(':')[2]),
                'post': post
            }
            self.action_manager.add_item(item_process)

            item_action = {
                'action': ACK,
                'host_id': host_id,
                'service_id': service_id
            }
            self.action_manager.add_item(item_action)

            self.sender().setEnabled(False)

    def add_downtime(self):  # pragma: no cover, no testability
        """
        Handle action for "downtime_btn"

        """

        # Get who emit SIGNAL
        item_type = str(self.sender().objectName().split(':')[0])

        if self.host:
            host_id = self.host['_id']

            if 'service' in item_type:
                service_id = str(self.sender().objectName().split(':')[1])
                self.action_manager.downtimed.append(service_id)
            else:
                service_id = None
                self.action_manager.downtimed.append(host_id)

            user = self.app_backend.get_user()

            comment = 'Schedule downtime by %s, from Alignak-app' % user['name']

            start_time = datetime.datetime.now()
            end_time = start_time + datetime.timedelta(days=1)

            data = {
                'action': 'add',
                'host': host_id,
                'service': service_id,
                'user': user['_id'],
                'comment': comment,
                'start_time': start_time.timestamp(),
                'end_time': end_time.timestamp(),
                'fixed': True
            }

            post = self.app_backend.post(DOWNTIME, data)
            item_process = {
                'action': PROCESS,
                'name': str(self.sender().objectName().split(':')[2]),
                'post': post
            }
            self.action_manager.add_item(item_process)

            item_action = {
                'action': DOWNTIME,
                'host_id': self.current_host['_id'],
                'service_id': service_id
            }
            self.action_manager.add_item(item_action)

            self.sender().setEnabled(False)

    def check_action_manager(self):  # pragma: no cover, no testability
        """
        Check ActionManager and send banner if items to send

        """

        items_to_send = self.action_manager.check_items()

        actions = [ACK, DOWNTIME]

        if items_to_send:

            # Send ACKs and DOWNTIMEs
            for action in actions:
                title = action.replace('action', '').capitalize()
                # For Hosts
                if items_to_send[action]['hosts']:
                    logger.debug('%s to send: %s', action, items_to_send[action]['hosts'])
                    for item in items_to_send[action]['hosts']:
                        host = self.app_backend.get_host(item['host_id'], '_id')
                        send_banner('OK', '%s for %s is done !' % (title, host['name']))
                # For Services
                if items_to_send[action]['services']:
                    logger.debug('%s to send: %s', action, items_to_send[action]['services'])
                    for item in items_to_send[action]['services']:
                        service = self.app_backend.get_service(item['host_id'], item['service_id'])
                        send_banner('OK', '%s for %s is done !' % (title, service['name']))
            # Send PROCESS
            if items_to_send[PROCESS]:
                logger.debug('PROCESS to send: %s', items_to_send[PROCESS])
                for item in items_to_send[PROCESS]:
                    requested_action = item['post']['_links']['self']['title'].replace(
                        'Action', '')
                    action_title = requested_action.capitalize()
                    send_banner('INFO', '%s for %s is processed...' % (action_title, item['name']))

    @staticmethod
    def get_host_icon(state):
        """
        Return QPixmap with the icon corresponding to the status.

        :param state: state of the host.
        :type state: str
        :return: QPixmap with image
        :rtype: QPixmap
        """

        if 'UP' in state:
            icon_name = 'hosts_up'
        elif 'UNREACHABLE' in state:
            icon_name = 'hosts_unreach'
        elif 'DOWN' in state:
            icon_name = 'hosts_down'
        else:
            icon_name = 'unvalid'

        icon = QPixmap(get_image_path(icon_name))

        return icon

    @staticmethod
    def get_real_state_icon(services):
        """
        Calculate real state and return QPixmap

        :param services: dict of services
        :type services: dict
        :return: QPixmap with right icon state
        :rtype: QPixmap
        """

        if services:
            icon_names = [
                'all_services_ok',
                'all_services_ok',
                'all_services_ok',
                'all_services_warning',
                'all_services_critical'
            ]
            state_lvl = []
            for service in services:
                state_lvl.append(service['_overall_state_id'])

            result = max(state_lvl)

            icon = QPixmap(get_image_path(icon_names[result]))
        else:
            icon = QPixmap(get_image_path('unvalid'))

        return icon
