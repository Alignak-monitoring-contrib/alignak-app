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
    Host Synthesis display data of choosen host in Synthesis
"""


from logging import getLogger

from alignak_app.core.utils import get_image_path, get_app_config
from alignak_app.core.utils import get_diff_since_last_check, get_date_from_timestamp
from alignak_app.core.action_manager import ACK, DOWNTIME, PROCESS
from alignak_app.widgets.banner import send_banner
from alignak_app.synthesis.service import Service
from alignak_app.synthesis.actions import Acknowledge, Downtime
from alignak_app.synthesis.service_widget_item import ServiceListWidgetItem

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QStackedWidget  # pylint: disable=no-name-in-module
from PyQt5.Qt import QIcon, QPixmap, QListWidget, QDialog  # pylint: disable=no-name-in-module
from PyQt5.Qt import QTimer, Qt, QCheckBox, QTextEdit  # pylint: disable=no-name-in-module
from PyQt5.QtGui import QFont  # pylint: disable=no-name-in-module


logger = getLogger(__name__)


class HostSynthesis(QWidget):
    """
        Class who create the HostSynthesis QWidget for host and its services.
    """

    state = {
        True: 'Yes',
        False: 'No'
    }

    def __init__(self, action_manager, parent=None):
        super(HostSynthesis, self).__init__(parent)
        self.app_backend = action_manager.app_backend
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
            self.host = backend_data['host']

            main_layout = QVBoxLayout(self)
            main_layout.addWidget(self.get_host_widget(backend_data))
            if backend_data['services']:
                main_layout.addWidget(self.get_services_widget(backend_data))
            else:
                nothing = QLabel('<b>No services defined for this host.</b>')
                nothing.setFixedHeight(400)
                main_layout.addWidget(nothing)
                main_layout.setAlignment(nothing, Qt.AlignHCenter)

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
        host_widget.setObjectName('host')
        host_layout = QGridLayout(host_widget)

        overall_state_img = QLabel()
        overall_state_img.setPixmap(self.get_real_state_icon(backend_data['services']))
        overall_state_img.setScaledContents(True)
        overall_state_img.setToolTip(self.get_real_state_text(backend_data['services']))
        host_layout.addWidget(overall_state_img, 0, 0, 2, 1)
        host_layout.setAlignment(overall_state_img, Qt.AlignCenter)

        # Hostname
        host_name = QLabel()
        if get_app_config('Alignak', 'webui'):
            host_name.setText(
                '<h2><a href="%s" style="color: black;text-decoration: none;">%s</a></h2>' % (
                    get_app_config('Alignak', 'webui') +
                    '/host/' +
                    backend_data['host']['name'],
                    backend_data['host']['alias'],
                )
            )
        else:
            host_name.setText('<h2>%s</h2>' % backend_data['host']['alias'])

        host_name.setTextInteractionFlags(Qt.TextBrowserInteraction)
        host_name.setOpenExternalLinks(True)
        host_name.setObjectName('hostname')
        host_name.setToolTip('Host is %s. See in WebUI ?' % backend_data['host']['ls_state'])
        host_layout.addWidget(host_name, 2, 0, 1, 1)
        host_layout.setAlignment(host_name, Qt.AlignCenter)

        # Real State
        host_real_state = QLabel()
        host_real_state.setPixmap(self.get_host_icon(backend_data['host']))
        host_real_state.setFixedSize(48, 48)
        host_real_state.setScaledContents(True)
        host_real_state.setToolTip(self.get_host_tooltip(backend_data['host']))
        host_layout.addWidget(host_real_state, 3, 0, 1, 1)
        host_layout.setAlignment(host_real_state, Qt.AlignCenter)

        real_state = QLabel('Host real state, excluding services')
        host_layout.addWidget(real_state, 4, 0, 1, 1)
        host_layout.setAlignment(real_state, Qt.AlignCenter)

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

        since_last_check = get_diff_since_last_check(backend_data['host']['ls_last_state_changed'])
        diff_last_check = get_diff_since_last_check(backend_data['host']['ls_last_check'])
        host_last_check = QLabel(
            '<b>Since:</b> %s <b>Last check:</b> %s' % (since_last_check, diff_last_check)
        )
        host_layout.addWidget(host_last_check, 0, 2, 1, 2)

        date_output = get_date_from_timestamp(backend_data['host']['ls_last_check'])
        output = QTextEdit(
            '<b>Output:</b> [%s] %s' % (date_output, backend_data['host']['ls_output'])
        )
        output.setObjectName('output')
        output.setTextInteractionFlags(Qt.TextSelectableByMouse)
        output.setFont(QFont('Times', 13))
        host_layout.addWidget(output, 1, 2, 1, 2)

        address = QLabel('<b>Address:</b> %s' % backend_data['host']['address'])
        host_layout.addWidget(address, 2, 2, 1, 1)

        stars_widget = Service.get_stars_widget(
            int(backend_data['host']['business_impact'])
        )
        host_layout.addWidget(stars_widget, 2, 3, 1, 1)
        host_layout.setAlignment(stars_widget, Qt.AlignLeft)

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
        acknowledge_btn.setIcon(QIcon(get_image_path('hosts_acknowledge')))
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
        downtime_btn.setIcon(QIcon(get_image_path('hosts_downtime')))
        downtime_btn.setFixedSize(32, 32)
        downtime_btn.setToolTip('Schedule a downtime for this host')
        downtime_btn.clicked.connect(self.add_downtime)
        if backend_data['host']['ls_downtimed'] or \
                backend_data['host']['_id'] in self.action_manager.downtimed:
            downtime_btn.setEnabled(False)
        host_layout.addWidget(downtime_btn, 1, 1, 1, 1)

    def filter_services(self):
        """
        Filter services State / Aggregation

        """

        for i in range(self.services_list.count()):
            sender_filter = str(self.sender().text()).split(':')[0]
            item_aggregation = str(self.services_list.item(i).aggregation)
            item_state = str(self.services_list.item(i).state)

            if sender_filter == item_aggregation:
                if self.sender().isChecked() \
                        and self.check_boxes[item_state].isChecked() \
                        and item_aggregation:
                    self.services_list.item(i).setHidden(False)
                else:
                    self.services_list.item(i).setHidden(True)
            if sender_filter == item_state and self.check_boxes[item_aggregation].isChecked():
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
        services_widget.setObjectName('services')
        services_layout = QGridLayout(services_widget)

        # Add aggregation filters and get current row
        row = self.add_aggregations_filters(services_layout, backend_data['services'])

        # Get number of each state for services
        services_stats = self.get_services_state_number(backend_data['services'])

        states = ['OK', 'UNKNOWN', 'WARNING', 'UNREACHABLE', 'CRITICAL', 'ACKNOWLEDGE', 'DOWNTIME']
        i_row = 1

        for state in states:
            # Create states CheckBox
            self.check_boxes[state] = QCheckBox(
                '%s: %d (%.02f%%)' % (
                    state, services_stats['nb'][state], services_stats['percent'][state]
                )
            )
            self.check_boxes[state].setIcon(QIcon(get_image_path('services_%s' % state.lower())))
            self.check_boxes[state].setObjectName(state)
            self.check_boxes[state].setChecked(True)
            self.check_boxes[state].stateChanged.connect(self.filter_services)
            services_layout.addWidget(self.check_boxes[state], row + i_row, 0, 1, 1)
            i_row += 1

        row += 1
        self.generate_services_qwidgets(row, services_layout, backend_data['services'])

        return services_widget

    def add_aggregations_filters(self, services_layout, services_list):
        """
        Add aggregations filter and return current row to maintain layout

        :param services_layout: layout of services
        :type services_layout: QGridLayout
        :param services_list: list of service dict
        :type services_list: list
        :return: current row
        :rtype: int
        """

        col = 1
        row = 0
        aggregations = ['Global']

        for service in services_list:
            if service['aggregation']:
                if service['aggregation'] not in aggregations:
                    aggregations.append(service['aggregation'])

        for aggregation in aggregations:
            self.check_boxes[aggregation] = QCheckBox(aggregation)
            self.check_boxes[aggregation].setIcon(QIcon(get_image_path('tree')))
            self.check_boxes[aggregation].setObjectName('aggregation')
            self.check_boxes[aggregation].setChecked(True)
            self.check_boxes[aggregation].stateChanged.connect(self.filter_services)
            services_layout.addWidget(self.check_boxes[aggregation], row, col, 1, 1)

            col += 1
            if col == 6:
                row += 1
                col = 1

        # Filters title
        if row == 0:
            row = 1
        filter_title = QLabel('States / Filters')
        services_layout.addWidget(filter_title, 0, 0, row, 1)
        services_layout.setAlignment(filter_title, Qt.AlignCenter | Qt.AlignBottom)

        return row

    def generate_services_qwidgets(self, row, services_layout, services_list):
        """
        Generate Service QWidgets, add them to QStackedWidget and QListWidget

        :param row: current row for services layout
        :type row: int
        :param services_layout: layout for services
        :type services_layout: QGridLayout
        :param services_list: list of services dict
        :type services_list: list
        """

        # Init QStackedWidget and QListWidget
        self.stack = QStackedWidget()
        self.services_list = QListWidget()
        self.services_list.setMinimumHeight(155)
        self.services_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        services_layout.addWidget(self.services_list, row, 1, 7, 5)
        services_layout.addWidget(self.stack, row + 7, 0, 1, 6)

        # Sorted services
        def get_key(item):
            """
            Get keys function to sort services

            :param item: item to sort
            :type item dict
            :return: item name in lowerCase to get InsensitiveCase
            :rtype: str
            """

            return item['name'].lower()

        sorted_services = sorted(services_list, key=get_key)

        # Fill QStackedWidget and QListWidget
        for service in sorted_services:
            # Service QWidget
            service_widget = Service()
            service_widget.initialize(service)

            # Connect ACK button
            service_widget.acknowledge_btn.clicked.connect(self.add_acknowledge)
            service_widget.acknowledge_btn.setObjectName(
                'service:%s:%s' % (
                    service['_id'],
                    ServiceListWidgetItem.get_service_name(service),
                )
            )
            if 'OK' in service['ls_state'] \
                    or service['ls_acknowledged'] \
                    or service['_id'] in self.action_manager.acknowledged:
                service_widget.acknowledge_btn.setEnabled(False)

            # Connect DOWN button
            service_widget.downtime_btn.clicked.connect(self.add_downtime)
            service_widget.downtime_btn.setObjectName(
                'service:%s:%s' % (
                    service['_id'],
                    ServiceListWidgetItem.get_service_name(service))
            )
            if service['ls_downtimed'] or service['_id'] in self.action_manager.downtimed:
                service_widget.downtime_btn.setEnabled(False)

            # Add widget to QStackedWidget
            self.stack.addWidget(service_widget)

            # Add item to QListWidget
            list_item = ServiceListWidgetItem()
            list_item.initialize(service)

            self.services_list.addItem(list_item)

        self.services_list.currentRowChanged.connect(self.display_current_service)

    @staticmethod
    def get_services_state_number(services):
        """
        Return the number / percentage of each state for host services

        :param services: list of host services dict
        :type: list
        :return: dict of services number / percentage
        :rtype: dict
        """

        nb_state = {
            'OK': 0,
            'UNKNOWN': 0,
            'WARNING': 0,
            'UNREACHABLE': 0,
            'CRITICAL': 0,
            'ACKNOWLEDGE': 0,
            'DOWNTIME': 0
        }
        percent_nb = {
            'OK': 0,
            'UNKNOWN': 0,
            'WARNING': 0,
            'UNREACHABLE': 0,
            'CRITICAL': 0,
            'ACKNOWLEDGE': 0,
            'DOWNTIME': 0
        }

        services_sum = 0
        for service in services:
            if service['ls_acknowledged']:
                nb_state['ACKNOWLEDGE'] += 1
            elif service['ls_downtimed']:
                nb_state['DOWNTIME'] += 1
            else:
                nb_state[service['ls_state']] += 1
            services_sum += 1

        for state in nb_state:
            try:
                percent_nb[state] = float(nb_state[state]) * 100.0 / float(services_sum)
            except ZeroDivisionError as e:
                logger.error('%s', e)

        services_stats = {
            'nb': nb_state,
            'percent': percent_nb
        }

        return services_stats

    def display_current_service(self, index):
        """
        Display the current selected Service QWidget

        :param index: index of QStackedWidget
        :type index: int
        """

        self.stack.setCurrentIndex(index)

    def add_acknowledge(self):  # pragma: no cover, no testability pylint: disable=too-many-locals
        """
        Handle action for "acknowledge_btn"

        """

        # Get who emit SIGNAL
        button = self.sender()
        item_type = str(button.objectName().split(':')[0])
        item_name = str(button.objectName().split(':')[2])

        if self.host:
            host_id = self.host['_id']

            if 'service' in item_type:
                service_id = str(button.objectName().split(':')[1])
                self.action_manager.acknowledged.append(service_id)
            else:
                service_id = None
                self.action_manager.acknowledged.append(host_id)

            user = self.app_backend.get_user(projection=['_id', 'name'])

            comment = '%s %s acknowledged by %s, from Alignak-app' % (
                item_type.capitalize(),
                item_name,
                user['name']
            )

            ack_dialog = Acknowledge()
            ack_dialog.initialize(item_type, item_name, comment)

            if ack_dialog.exec_() == QDialog.Accepted:
                sticky = ack_dialog.sticky
                notify = ack_dialog.notify
                comment = str(ack_dialog.ack_comment_edit.toPlainText())

                data = {
                    'action': 'add',
                    'host': host_id,
                    'service': service_id,
                    'user': user['_id'],
                    'comment': comment,
                    'notify': notify,
                    'sticky': sticky
                }

                post = self.app_backend.post(ACK, data)
                item_process = {
                    'action': PROCESS,
                    'name': item_name,
                    'post': post
                }
                self.action_manager.add_item(item_process)

                item_action = {
                    'action': ACK,
                    'host_id': host_id,
                    'service_id': service_id
                }
                self.action_manager.add_item(item_action)

                try:
                    button.setEnabled(False)
                except RuntimeError as e:
                    logger.warning('Can\'t disable Acknowledge btn: %s', e)
            else:
                logger.info('Acknowledge for %s cancelled...', item_name)

    def add_downtime(self):  # pragma: no cover, no testability  pylint: disable=too-many-locals
        """
        Handle action for "downtime_btn"

        """

        # Get who emit SIGNAL
        button = self.sender()
        item_type = str(button.objectName().split(':')[0])
        item_name = str(button.objectName().split(':')[2])

        if self.host:
            host_id = self.host['_id']

            if 'service' in item_type:
                service_id = str(button.objectName().split(':')[1])
                self.action_manager.downtimed.append(service_id)
            else:
                service_id = None
                self.action_manager.downtimed.append(host_id)

            user = self.app_backend.get_user(projection=['_id', 'name'])

            comment = 'Schedule downtime by %s, from Alignak-app' % user['name']

            downtime_dialog = Downtime()
            downtime_dialog.initialize(item_type, item_name, comment)

            if downtime_dialog.exec_() == QDialog.Accepted:
                fixed = downtime_dialog.fixed
                duration = downtime_dialog.duration_to_seconds()
                start_stamp = downtime_dialog.start_time.dateTime().toTime_t()
                end_stamp = downtime_dialog.end_time.dateTime().toTime_t()
                comment = downtime_dialog.comment_edit.toPlainText()

                data = {
                    'action': 'add',
                    'host': host_id,
                    'service': service_id,
                    'user': user['_id'],
                    'fixed': fixed,
                    'duration': duration,
                    'start_time': start_stamp,
                    'end_time': end_stamp,
                    'comment': comment,
                }

                post = self.app_backend.post(DOWNTIME, data)
                item_process = {
                    'action': PROCESS,
                    'name': item_name,
                    'post': post
                }
                self.action_manager.add_item(item_process)

                item_action = {
                    'action': DOWNTIME,
                    'host_id': host_id,
                    'service_id': service_id
                }
                self.action_manager.add_item(item_action)

                try:
                    button.setEnabled(False)
                except RuntimeError as e:
                    logger.warning('Can\'t disable Downtime btn: %s', e)
            else:
                logger.info('Downtime for %s cancelled...', item_name)

    def check_action_manager(self):  # pragma: no cover, no testability
        """
        Check ActionManager and send banner if items to send

        """

        items_to_send = self.action_manager.check_items()

        actions = [ACK, DOWNTIME]

        if items_to_send:
            # Send PROCESS
            if items_to_send[PROCESS]:
                logger.debug('PROCESS to send: %s', items_to_send[PROCESS])
                for item in items_to_send[PROCESS]:
                    requested_action = item['post']['_links']['self']['title'].replace(
                        'Action', '')
                    action_title = requested_action.capitalize()
                    send_banner('INFO', '%s for %s is processed...' % (action_title, item['name']))

            # Send ACKs and DOWNTIMEs
            for action in actions:
                title = action.replace('action', '').capitalize()
                # For Hosts
                if items_to_send[action]['hosts']:
                    logger.debug('%s to send: %s', action, items_to_send[action]['hosts'])
                    for item in items_to_send[action]['hosts']:
                        host = self.app_backend.get_host('_id', item['host_id'], ['name'])
                        send_banner('OK', '%s for %s is done !' % (title, host['name']))
                # For Services
                if items_to_send[action]['services']:
                    logger.debug('%s to send: %s', action, items_to_send[action]['services'])
                    for item in items_to_send[action]['services']:
                        service = self.app_backend.get_service(
                            item['host_id'],
                            item['service_id'],
                            ['name']
                        )
                        send_banner('OK', '%s for %s is done !' % (title, service['name']))

    @staticmethod
    def get_host_icon(host):
        """
        Return QPixmap with the icon corresponding to the status.

        :param host: host data from AppBackend
        :type host: dict
        :return: QPixmap with image
        :rtype: QPixmap
        """

        if host['ls_acknowledged']:
            icon_name = 'hosts_acknowledge'
        elif host['ls_downtimed']:
            icon_name = 'hosts_downtimed'
        else:
            icon_name = 'hosts_%s' % host['ls_state'].lower()

        icon = QPixmap(get_image_path(icon_name))

        return icon

    @staticmethod
    def get_host_tooltip(host):
        """
        Return tooltip text for Host real state

        :param host: host data from Backend
        :type host: dict
        :return: tooltip of host real state
        :rtype: str
        """

        if host['ls_acknowledged'] and not host['ls_downtimed']:
            tooltip = 'Host is %s and acknowledged !' % host['ls_state']
        elif host['ls_downtimed'] and not host['ls_acknowledged']:
            tooltip = 'Host is %s and downtimed !' % host['ls_state']
        elif host['ls_acknowledged'] and host['ls_downtimed']:
            tooltip = 'Host is %s and acknowledged ! A downtime is scheduled !' % host['ls_state']
        else:
            tooltip = 'Host is %s' % host['ls_state']

        return tooltip

    @staticmethod
    def get_result_overall_state_id(list_text, services):
        """
        Return text from result of maximum overall state

        :param list_text: list of text to return
        :type list_text: list
        :param services: list of service dict from backend
        :type services: list
        :return: the resulting text
        :rtype: str
        """

        state_lvl = []
        for service in services:
            state_lvl.append(service['_overall_state_id'])

        result = max(state_lvl)

        return list_text[result]

    def get_real_state_text(self, services):
        """
        Return real state text corresponding to max overall state

        :return: the real state text
        :rtype: str
        """

        if services:
            overall_texts = [
                'Host and its services are ok',
                'Host and its services are ok or acknowledged',
                'Host and its services are ok or downtimed',
                'Host or some of its services are warning or unknown',
                'Host or some of its services are critical !',
            ]

            text_result = self.get_result_overall_state_id(overall_texts, services)
        else:
            text_result = 'No services found for this host.'

        return text_result

    def get_real_state_icon(self, services):
        """
        Calculate real state and return QPixmap

        :param services: list of service dict
        :type services: list
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

            text_result = self.get_result_overall_state_id(icon_names, services)

            icon = QPixmap(get_image_path(text_result))
        else:
            logger.warning(
                'Services not found. Can\'t get real state icon for %s', self.host['name']
            )
            icon = QPixmap(get_image_path('all_services_none'))

        return icon
