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

from PyQt5.Qt import QThread, pyqtSignal  # pylint: disable=no-name-in-module

from alignak_app.core.data_manager import DataManager


class BackendThread(QThread):
    """
        Class who create a QThread to trigger requests
    """

    trigger = pyqtSignal(DataManager)

    def __init__(self, app_backend, parent=None):
        super(BackendThread, self).__init__(parent)
        self.app_backend = app_backend
        self.data_manager = DataManager()
        self.requests_models = None
        self.request_nb = 0

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

        self.requests_models = {
            'host': {
                'params': {'where': json.dumps({'_is_template': False})},
                'projection': hosts_projection
            },
            'service': {
                'params': {'where': json.dumps({'_is_template': False})},
                'projection': services_projection
            }
        }

    def run(self):
        """
        Override Method: Trigger when QThread.start() is called.
        - Make AppBackend requests and store results in DataManager

        """

        self.request_nb += 1
        print("--------- Request N° %d ---------------" % self.request_nb)
        self.set_requests_models()

        backend_data = {
            'host': {},
            'service': {}
        }

        for endpoint in self.requests_models:
            request = self.app_backend.get(
                endpoint,
                params=self.requests_models[endpoint]['params'],
                projection=self.requests_models[endpoint]['projection'],
                all_items=True
            )

            backend_data[endpoint] = request['_items']

        for item_type in backend_data:
            self.data_manager.update_item_type(
                item_type,
                backend_data[item_type]
            )

        self.trigger.emit(self.data_manager)
