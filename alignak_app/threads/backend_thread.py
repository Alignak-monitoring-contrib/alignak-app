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
import sys
import locale
import datetime

from logging import getLogger

from PyQt5.Qt import QThread, pyqtSignal  # pylint: disable=no-name-in-module

from alignak_app.core.data_manager import data_manager, DataManager
from alignak_app.core.backend import app_backend


logger = getLogger(__name__)


class BackendQThread(QThread):
    """
        Class who create a QThread to trigger requests
    """

    update_data = pyqtSignal(DataManager)

    def __init__(self, parent=None):
        super(BackendQThread, self).__init__(parent)
        self.requests_id_models = None
        self.requests_data_models = None
        self.request_nb = 0
        self.cur_host_id = None

    def set_id_requests_models(self):
        """
        Define the requests models for endpoints items with "_id".

        """

        hosts_projection = [
            'name', 'alias', 'ls_state', '_id', 'ls_acknowledged', 'ls_downtimed', 'ls_last_check',
            'ls_output', 'address', 'business_impact', 'parents', 'ls_last_state_changed'
        ]
        services_projection = [
            'name', 'alias', 'display_name', 'ls_state', 'ls_acknowledged', 'ls_downtimed',
            'ls_last_check', 'ls_output', 'business_impact', 'customs', '_overall_state_id',
            'aggregation', 'ls_last_state_changed'
        ]
        daemons_projection = ['alive', 'type', 'name']

        self.requests_id_models = {
            'host': {
                'params': {'where': json.dumps({'_is_template': False})},
                'projection': hosts_projection
            },
            'service': {
                'params': {'where': json.dumps({'_is_template': False})},
                'projection': services_projection
            },
            'alignakdaemon': {
                'params': None,
                'projection': daemons_projection
            },
            'livesynthesis': {
                'params': None,
                'projection': None
            },
        }

    def set_data_requests_models(self):
        """
        Define the requests models for endpoints items with simple data.

        """

        user_projection = {
            '_realm', 'is_admin', 'back_role_super_admin', 'alias', 'name', 'notes', 'email',
            'can_submit_commands', 'token', 'host_notifications_enabled',
            'service_notifications_enabled', 'host_notification_period',
            'service_notification_period', 'host_notification_options',
            'service_notification_options',
        }
        notification_projection = {
            'message', '_updated'
        }

        # Backend use time format in "en_US", so switch if needed
        if "en_US" not in locale.getlocale(locale.LC_TIME) and 'win32' not in sys.platform:
            locale.setlocale(locale.LC_TIME, "en_US.utf-8")
            logger.warning("App set locale to %s ", locale.getlocale(locale.LC_TIME))

        # Define time for the last 30 minutes for notifications
        time_interval = (datetime.datetime.utcnow() - datetime.timedelta(minutes=30)) \
            .strftime("%a, %d %b %Y %H:%M:%S GMT")

        self.requests_data_models = {
            'user': {
                'params': {'where': json.dumps({'token': app_backend.backend.token})},
                'projection': user_projection
            },
            'history': {
                'params': {
                    'sort': '-_id',
                },
                'projection': {'service_name': 1, 'message': 1, 'type': 1}
            },
            'notifications': {
                'params': {
                    'where': json.dumps({
                        'type': 'monitoring.notification',
                        '_updated': {"$gte": time_interval}
                    }),
                    'sort': '-_updated'
                },
                'projection': notification_projection
            }
        }

    def run(self):
        """
        Override Method: Trigger when QThread.start() is called.
        - Make AppBackend requests and store results in DataManager

        """

        logger.info("Run BackendQThread...")
        # Set each requests parameters
        self.set_id_requests_models()
        self.set_data_requests_models()

        # Update
        self.update_items_id_database()
        self.update_database()

        # Display results
        self.update_data.emit(data_manager)

    def update_items_id_database(self):
        """
        Update items with "_id" fields:
        - "host", "service", "alignakdaemon" and "livesynthesis"

        """

        # host, service, alignakdaemon and livesynthesis
        backend_id_database = data_manager.get_item_id_model()

        # Requests on each endpoint defined in model
        for endpoint in self.requests_id_models:
            request = app_backend.get(
                endpoint,
                params=self.requests_id_models[endpoint]['params'],
                projection=self.requests_id_models[endpoint]['projection'],
                all_items=True
            )
            backend_id_database[endpoint] = request['_items']

        # Update DataManager
        for item_type in backend_id_database:
            data_manager.update_id_item(
                item_type,
                backend_id_database[item_type]
            )

    def update_database(self):
        """
        Update items with simple data:
        - "user", "history" and "notification"

        """

        backend_database = data_manager.get_item_data_model()

        # Request user
        request = app_backend.get(
            'user',
            params=self.requests_data_models['user']['params'],
            projection=self.requests_data_models['user']['projection'],
            all_items=False
        )
        backend_database['user'] = request['_items'][0]

        # Request for history
        for host_id in data_manager.item_id_database['host']:
            self.requests_data_models['history']['params']['where'] = json.dumps({
                'host': host_id}),
            request = app_backend.get(
                'history',
                params=self.requests_data_models['history']['params'],
                projection=self.requests_data_models['history']['projection'],
                all_items=False
            )
            backend_database['history'][host_id] = request['_items']

        # Request for notification
        request = app_backend.get(
            'history',
            params=self.requests_data_models['notifications']['params'],
            projection=self.requests_data_models['notifications']['projection'],
            all_items=False
        )

        notifications = []
        for notif in request['_items']:
            message_split = notif['message'].split(';')
            user = message_split[0].split(':')[1]
            if 'imported_admin' in user:
                user = 'admin'
            # If notification is for the current user
            if user == data_manager.get_user()['name']:
                notifications.append(notif)

        backend_database['notifications'] = notifications

        # Update DataManager
        for item_type in backend_database:
            data_manager.update_data_item(
                item_type,
                backend_database[item_type]
            )
