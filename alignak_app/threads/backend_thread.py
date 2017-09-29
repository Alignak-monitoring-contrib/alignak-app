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
        self.requests_models = None
        self.request_nb = 0
        self.cur_host_id = None

    def set_requests_models(self):
        """
        Define the requests models for each endpoints.

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
        user_projection = {
            '_realm', 'is_admin', 'back_role_super_admin', 'alias', 'name', 'notes', 'email',
            'can_submit_commands', 'token', 'host_notifications_enabled',
            'service_notifications_enabled', 'host_notification_period',
            'service_notification_period', 'host_notification_options',
            'service_notification_options',
        }

        self.requests_models = {
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
            'user': {
                'params': {'where': json.dumps({'token': app_backend.backend.token})},
                'projection': user_projection
            },
            'history': {
                'params': {
                    # 'where': json.dumps({'host': self.cur_host_id}),
                    'sort': '-_id',
                },
                'projection': {'service_name': 1, 'message': 1, 'type': 1}
            }
        }

    def run(self):
        """
        Override Method: Trigger when QThread.start() is called.
        - Make AppBackend requests and store results in DataManager

        """

        logger.info("Run BackendQThread...")
        # FOR TESTS
        self.request_nb += 1
        print("--------- Request N° %d ---------------" % self.request_nb)

        # Set each requests parameters
        self.set_requests_models()

        # Get the database model
        backend_database = data_manager.get_database_model()

        # Requests on each endpoint defined in model
        for endpoint in self.requests_models:
            all_items = True
            if 'user' in endpoint:
                all_items = False
            if 'history' not in endpoint:
                request = app_backend.get(
                    endpoint,
                    params=self.requests_models[endpoint]['params'],
                    projection=self.requests_models[endpoint]['projection'],
                    all_items=all_items
                )
                backend_database[endpoint] = request['_items']

        # Update DataManager
        for item_type in backend_database:
            print(item_type)
            print(backend_database[item_type])
            data_manager.update_item_type(
                item_type,
                backend_database[item_type]
            )

        for host in backend_database['host']:
            self.requests_models['history']['params']['where'] = json.dumps({
                'host': host['_id']}),
            request = app_backend.get(
                'history',
                params=self.requests_models['history']['params'],
                projection=self.requests_models['history']['projection'],
                all_items=False
            )
            backend_database['history'][host['_id']] = request['_items']

        data_manager.update_history_item('history', backend_database['history'])

        self.update_data.emit(data_manager)
