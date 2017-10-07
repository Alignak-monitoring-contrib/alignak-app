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
    ItemUser manage creation of user item
"""

import json

from logging import getLogger


from alignak_app.models.item_model import ItemModel
from alignak_app.core.backend import app_backend, data_manager


logger = getLogger(__name__)


class User(ItemModel):
    """
        Class who create user item
    """

    def __init__(self):
        super(User, self).__init__()
        self.item_type = 'user'

    @staticmethod
    def get_request_model():
        """
        Return the request model for user requests

        :return: request model for user endpoint
        :rtype: dict
        """

        user_projection = {
            '_realm', 'is_admin', 'back_role_super_admin', 'alias', 'name', 'notes', 'email',
            'can_submit_commands', 'token', 'host_notifications_enabled',
            'service_notifications_enabled', 'host_notification_period',
            'service_notification_period', 'host_notification_options',
            'service_notification_options',
        }

        request = {
            'endpoint': 'user',
            'params': {'where': json.dumps({'token': app_backend.backend.token})},
            'projection': user_projection
        }

        return request

    @staticmethod
    def get_role():
        """
        Get user role

        :return: role of user
        :rtype: str
        """

        role = _('user')

        if data_manager.database['user'].data['is_admin'] or \
                data_manager.database['user'].data['back_role_super_admin']:
            role = _('administrator')
        if data_manager.database['user'].data['can_submit_commands'] and not \
                data_manager.database['user'].data['is_admin'] and not \
                data_manager.database['user'].data['back_role_super_admin']:
            role = _('power')

        return role

    @staticmethod
    def get_realm_name():
        """
        Return realm name or alias

        :return: realm name or alias
        :rtype: str
        """

        if '_realm' in data_manager.database['user'].data:
            endpoint = '/'.join(
                ['realm', data_manager.database['user'].data['_realm']]
            )
            projection = [
                'name',
                'alias'
            ]

            realm = app_backend.get(endpoint, projection=projection)

            if realm:
                if realm['alias']:
                    return realm['alias']

                return realm['name']

        return 'n/a'

    @staticmethod
    def get_period_name(uuid):
        """
        Get the period name or alias

        :param uuid: the Id of the timeperiod
        :type uuid: str
        :return: name or alias of timeperiod
        :rtype: str
        """

        projection = [
            'name',
            'alias'
        ]

        endpoint = '/'.join(['timeperiod', uuid])

        period = app_backend.get(endpoint, projection=projection)

        if period:
            if 'alias' in period:
                return period['alias']

            return period['name']

        return 'n/a'
