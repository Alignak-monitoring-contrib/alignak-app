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
    BackendThread manage backend threads and requests
"""

import json

from logging import getLogger

from PyQt5.Qt import QRunnable  # pylint: disable=no-name-in-module

from alignak_app.core.backend import app_backend
from alignak_app.core.data_manager import data_manager

from alignak_app.models.item_user import User
from alignak_app.models.item_host import Host
from alignak_app.models.item_service import Service
from alignak_app.models.item_daemon import Daemon
from alignak_app.models.item_livesynthesis import LiveSynthesis
from alignak_app.models.item_history import History
from alignak_app.models.item_notification import Notification

logger = getLogger(__name__)


class BackendQRunnable(QRunnable):
    """
        Class who create a QThread to trigger requests
    """

    def __init__(self, task):
        super(BackendQRunnable, self).__init__()
        self.task = task

    def run(self):
        """
        Run the QRunnable. Trigger actions depending on the selected task
        :return:
        """

        if 'user' in self.task:
            self.query_user_data()
        elif 'host' in self.task:
            self.query_hosts_data()
        elif 'service' in self.task:
            self.query_services_data()
        elif 'alignakdaemon' in self.task:
            self.query_daemons_data()
        elif 'livesynthesis' in self.task:
            self.query_livesynthesis_data()
        elif 'history' in self.task:
            self.query_history_data()
        elif 'notifications' in self.task:
            self.query_notifications_data()
        else:
            logger.error("Tasks is unknown: %s", self.task)

    @staticmethod
    def query_user_data():
        """
        Launch request for "user" endpoint

        """

        user = User()

        request_data = user.get_request_model()

        request = app_backend.get(
            request_data['endpoint'],
            request_data['params'],
            request_data['projection']
        )

        user.create(
            request['_items'][0]['_id'],
            request['_items'][0],
            request['_items'][0]['name']
        )

        data_manager.update_item_database('user', user)

    @staticmethod
    def query_hosts_data():
        """
        Launch request for "host" endpoint

        """

        request_data = Host.get_request_model()

        request = app_backend.get(
            request_data['endpoint'],
            request_data['params'],
            request_data['projection'],
            all_items=True
        )

        hosts_list = []
        for item in request['_items']:
            host = Host()

            host.create(
                item['_id'],
                item,
                item['name'],
            )
            hosts_list.append(host)

        data_manager.update_item_database('host', hosts_list)

    @staticmethod
    def query_services_data():
        """
        Launch request for "service" endpoint

        """

        request_data = Service.get_request_model()

        request = app_backend.get(
            request_data['endpoint'],
            request_data['params'],
            request_data['projection'],
            all_items=True
        )

        services_list = []
        for item in request['_items']:
            service = Service()

            service.create(
                item['_id'],
                item,
                item['name'],
            )

            services_list.append(service)

        data_manager.update_item_database('service', services_list)

    @staticmethod
    def query_daemons_data():
        """
        Launch request for "alignakdaemon" endpoint

        """

        request_data = Daemon.get_request_model()

        request = app_backend.get(
            request_data['endpoint'],
            request_data['params'],
            request_data['projection'],
            all_items=True
        )

        daemons_list = []
        for item in request['_items']:
            daemon = Daemon()

            daemon.create(
                item['_id'],
                item,
                item['name'],
            )

            daemons_list.append(daemon)

        data_manager.update_item_database('alignakdaemon', daemons_list)

    @staticmethod
    def query_livesynthesis_data():
        """
        Launch request for "livesynthesis" endpoint

        """

        request_data = LiveSynthesis.get_request_model()

        request = app_backend.get(
            request_data['endpoint'],
            request_data['params'],
            request_data['projection'],
            all_items=True
        )

        livesynthesis = []
        for item in request['_items']:
            synthesis = LiveSynthesis()

            synthesis.create(
                item['_id'],
                item,
            )

            livesynthesis.append(synthesis)

        data_manager.update_item_database('livesynthesis', livesynthesis)

    @staticmethod
    def query_history_data():
        """
        Launch request for "history" endpoint but only for hosts in "data_manager"

        """

        request_data = History.get_request_model()

        history_list = []
        for host in data_manager.database['host']:
            request_data['params']['where'] = json.dumps({
                'host': host.item_id})

            request = app_backend.get(
                request_data['endpoint'],
                request_data['params'],
                request_data['projection'],
                all_items=False
            )

            history = History()

            history.create(
                host.item_id,
                request['_items'],
                host.name,
            )

            history_list.append(history)

        data_manager.update_item_database('history', history_list)

    @staticmethod
    def query_notifications_data():
        """
        Launch request for "history" endpoint but only for notifications of current user

        """

        request_data = Notification.get_request_model()

        request = app_backend.get(
            request_data['endpoint'],
            request_data['params'],
            request_data['projection'],
            all_items=False
        )

        notifications = []
        for item in request['_items']:
            message_split = item['message'].split(';')
            user = message_split[0].split(':')[1].strip()
            if 'imported_admin' in user:
                user = 'admin'
            if user == data_manager.database['user'].name:
                notification = Notification()

                notification.create(
                    item['_id'],
                    item,
                )

                notifications.append(notification)

        data_manager.update_item_database('notifications', notifications)
