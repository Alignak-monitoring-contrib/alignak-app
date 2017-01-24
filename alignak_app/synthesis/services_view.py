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
    App Synthesis manage widget for Synthesis QWidget.
"""

import datetime

from logging import getLogger

from alignak_app.synthesis.service import Service
from alignak_app.core.action_manager import ACK, DOWNTIME, PROCESS

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QScrollArea  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QVBoxLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout, QLabel  # pylint: disable=no-name-in-module
    from PyQt5.Qt import Qt  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QScrollArea  # pylint: disable=import-error
    from PyQt4.Qt import QWidget, QVBoxLayout  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout, QLabel  # pylint: disable=import-error
    from PyQt4.Qt import Qt  # pylint: disable=import-error


logger = getLogger(__name__)


class ServicesView(QWidget):
    """
        Class who create the Synthesis QWidget.
    """

    def __init__(self, action_manager, app_backend, parent=None):
        super(ServicesView, self).__init__(parent)
        self.setToolTip('Services View')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.current_host = None
        self.action_manager = action_manager
        self.app_backend = app_backend
        self.services_widget = []

    def display_services(self, services, host):  # pylint: disable=too-many-locals
        """
        Display services.

        :param services: services of a specific host from app_backend
        :type services: dict
        :param host: host to which the services belong
        :type host: dict
        """

        logger.info('Create Services View')
        self.current_host = host

        # Clean all items before
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        service_title = QLabel('<b>Services of ' + host['name'] + '</b>')
        self.layout.addWidget(service_title)
        self.layout.setAlignment(service_title, Qt.AlignCenter)

        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        # Reset pos and QWidget List
        self.services_widget = []
        pos = 0

        if not services:
            logger.warning('Services not Found ! ')

            output_service = QLabel('Services not available .... Search for a host before.')
            layout.addWidget(output_service, 0, 0)
        else:
            for service in services:
                # Create Service QWidget
                service_widget = Service()
                service_widget.initialize(service)
                service_widget.acknowledged.connect(self.add_acknowledge)
                service_widget.downtimed.connect(self.add_downtime)

                # Update buttons
                self.update_service_buttons(service_widget)
                layout.addWidget(service_widget, pos, 0)
                pos += 1

                # Add to QWidget list
                self.services_widget.append(service_widget)

        logger.debug('Number of services: ' + str(pos))

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)

        self.layout.addWidget(scroll)
        self.show()

    def update_services(self):
        """
        Manage update of each Service QWidget in QWidget List

        """

        if self.services_widget:
            for service_widget in self.services_widget:
                cur_service = service_widget.service
                updated_service = self.app_backend.get_service(
                    self.current_host['_id'],
                    cur_service['_id']
                )
                service_widget.update_service(updated_service)
                self.update_service_buttons(service_widget)

    def update_service_buttons(self, service):
        """
        Update buttons of the service who has emit action

        :param service: service QWidget
        :type service: Service
        """

        if 'OK' in service.service['ls_state']:
            service.acknowledge_btn.setEnabled(False)
        elif service.service['ls_acknowledged'] or \
                service.service['display_name'] in self.action_manager.acks_to_check['services']:
            service.acknowledge_btn.setEnabled(False)
        else:
            service.acknowledge_btn.setEnabled(True)

        if 'OK' in service.service['ls_state']:
            service.downtime_btn.setEnabled(False)
        if service.service['ls_downtimed'] or \
                service.service['display_name'] in \
                self.action_manager.downtimes_to_check['services']:
            service.downtime_btn.setEnabled(False)
        else:
            service.downtime_btn.setEnabled(True)

    def add_acknowledge(self):  # pragma: no cover, no testability
        """
        Handle action for "acknowledge_btn"

        """

        # Get service who emit SIGNAL
        service = self.sender().service

        if self.current_host:
            user = self.app_backend.get_user()

            comment = 'Service %s acknowledged by %s, from Alignak-app' % (
                service['name'],
                user['name']
            )

            data = {
                'action': 'add',
                'host': self.current_host['_id'],
                'service': service['_id'],
                'user': user['_id'],
                'comment': comment
            }

            post = self.app_backend.post(ACK, data)
            item_process = {
                'action': PROCESS,
                'name': service['name'],
                'post': post
            }
            self.action_manager.add_item(item_process)

            item_action = {
                'action': ACK,
                'host_id': self.current_host['_id'],
                'service_id': service['_id']
            }
            self.action_manager.add_item(item_action)

            self.sender().acknowledge_btn.setEnabled(False)

    def add_downtime(self):  # pragma: no cover, no testability
        """
        Handle action for "downtime_btn"

        """

        service = self.sender().service

        if self.current_host:
            user = self.app_backend.get_user()

            comment = 'Schedule downtime by %s, from Alignak-app' % user['name']

            start_time = datetime.datetime.now()
            end_time = start_time + datetime.timedelta(days=1)

            data = {
                'action': 'add',
                'host': self.current_host['_id'],
                'service': service['_id'],
                'user': user['_id'],
                'comment': comment,
                'start_time': start_time.timestamp(),
                'end_time': end_time.timestamp(),
                'fixed': True
            }

            post = self.app_backend.post(DOWNTIME, data)
            item_process = {
                'action': PROCESS,
                'name': service['name'],
                'post': post
            }
            self.action_manager.add_item(item_process)

            item_action = {
                'action': DOWNTIME,
                'host_id': self.current_host['_id'],
                'service_id': service['_id']
            }
            self.action_manager.add_item(item_action)

            self.sender().downtime_btn.setEnabled(False)
