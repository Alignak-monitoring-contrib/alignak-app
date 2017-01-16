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
    App Backend manage connexion and access to app_backend.
"""

import json
import sys
from logging import getLogger

from alignak_backend_client.client import Backend, BackendException

from alignak_app.core.utils import get_app_config

logger = getLogger(__name__)


class AppBackend(object):
    """
        Class who collect informations with Backend-Client and returns data for
        Alignak-App.
    """

    def __init__(self):
        self.backend = None
        self.first_check = True
        self.states = {}
        self.user = {}

    def login(self, username=None, password=None):
        """
        Connect to app_backend with credentials in settings.cfg.

        """

        # Credentials
        if not username and not password:
            if self.user:
                username = self.user['token']
            else:
                username = get_app_config('Backend', 'username')
                password = get_app_config('Backend', 'password')

        # Create Backend object
        backend_url = get_app_config('Backend', 'alignak_backend')
        self.backend = Backend(backend_url)

        logger.debug('Backend URL : ' + backend_url)
        logger.info('Try to connect to app_backend...')

        if username and password:
            # Username & password : not recommended, without "widgets.login.py" form.
            try:
                connect = self.backend.login(username, password)
                if connect:
                    self.user['username'] = username
                    self.user['token'] = self.backend.token
                logger.info('Connection by password: ' + str(connect))
            except BackendException as e:  # pragma: no cover
                logger.error(
                    'Connection to Backend has failed. ' +
                    str(e)
                )
                print(e, 'Please, check your [settings.cfg] and logs.')
                sys.exit()
        elif username and not password:
            # Username as token : recommended
            self.backend.authenticated = True
            if self.user:
                self.backend.token = self.user['token']
            else:
                self.backend.token = username
                self.user['token'] = username
            logger.info('Connection by token: ' + str(self.backend.authenticated))

            # Test to check token
            connect = bool(self.get('livesynthesis'))
        else:
            # Else exit
            logger.error(
                'Connection to Backend has failed. ' +
                '\nCheck [Backend] section in configuration file.'
            )
            connect = False

        return connect

    def get(self, endpoint, params=None):
        """
        Collect state of Hosts, via app_backend API.

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :param params: dict of parameters for the app_backend API
        :type params: dict
        :return desired request of app_backend
        :rtype: dict
        """

        request = None

        if not params:
            params = {'max_results': 50}

        # Request
        try:
            request = self.backend.get_all(
                endpoint,
                params
            )
            logger.debug('GET: ' + endpoint)
            logger.debug('..with params: ' + str(params))
            logger.debug('...Response > ' + str(request['_status']))
        except BackendException as e:
            logger.error(str(e))

        return request

    def post(self, endpoint, data, headers=None):
        """

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :param data: properties of item to create
        :type data: dict
        :param headers: headers (example: Content-Type)
        :type headers: dict
        :return: response (creation information)
        :rtype: dict
        """

        resp = None

        try:
            resp = self.backend.post(endpoint, data, headers=headers)
            logger.debug('POST on ' + endpoint)
            logger.debug('..with data: ' + str(data))
            logger.debug('...Response > ' + str(resp))
        except BackendException as e:
            logger.error(str(e))

        return resp

    def get_item(self, item_name, endpoint):
        """
        Get a wanted host or service item.

        :param item_name: name of wanted item : host or service
        :type item_name: str
        :param endpoint: corresponding endpoint
        :type endpoint: str
        :return: None if not found or item dict
        """

        params = {'where': json.dumps({'_is_template': False})}

        result = self.get(endpoint, params)

        item_result = None

        for current_item in result['_items']:
            if current_item['name'] == item_name:
                item_result = current_item

        return item_result

    def get_all_host_data(self, host_name):
        """
        Collect item data and associated services

        :param host_name: desired host
        :type host_name: str
        :return dict with host informations and associated services
        :rtype: dict
        """

        host_data = None

        host = self.get_item(host_name, 'host')

        if host:
            params = {
                'where': json.dumps({
                    '_is_template': False,
                    'host': host['_id']
                })
            }
            services = self.get('service', params=params)

            host_services = services['_items']

            host_data = {
                'host': host,
                'services': host_services
            }

        return host_data

    def get_user(self):
        """
        Retrieve user by token.

        :return user items
        :rtype dict
        """

        params = {
            'where': json.dumps({
                'token': self.user['token']
            })
        }

        user = self.get('user', params)

        return user['_items'][0]

    def synthesis_count(self):
        """
        Check and return the hosts and services states.

        :return: each number of states for hosts and services.
        :rtype: dict
        """

        if not self.backend.authenticated:
            logger.warning('Connection to app_backend is lost, application will try to reconnect !')
            self.login()

        logger.info('GET synthesis count states...')

        # Initialize dicts for states
        states = {
            'hosts': {
                'up': 0,
                'down': 0,
                'unreachable': 0,
                'acknowledge': 0,
                'downtime': 0
            },
            'services': {
                'ok': 0,
                'critical': 0,
                'unknown': 0,
                'warning': 0,
                'unreachable': 0,
                'acknowledge': 0,
                'downtime': 0
            }
        }

        live_synthesis = self.get('livesynthesis')

        if live_synthesis:
            for realm in live_synthesis['_items']:
                states['hosts']['up'] += realm['hosts_up_soft']
                states['hosts']['up'] += realm['hosts_up_hard']

                states['hosts']['unreachable'] += realm['hosts_unreachable_soft']
                states['hosts']['unreachable'] += realm['hosts_unreachable_hard']

                states['hosts']['down'] += realm['hosts_down_soft']
                states['hosts']['down'] += realm['hosts_down_hard']

                states['hosts']['acknowledge'] += realm['hosts_acknowledged']
                states['hosts']['downtime'] += realm['hosts_in_downtime']

                states['services']['ok'] += realm['services_ok_soft']
                states['services']['ok'] += realm['services_ok_hard']

                states['services']['warning'] += realm['services_warning_soft']
                states['services']['warning'] += realm['services_warning_hard']

                states['services']['critical'] += realm['services_critical_soft']
                states['services']['critical'] += realm['services_critical_hard']

                states['services']['unknown'] += realm['services_unknown_soft']
                states['services']['unknown'] += realm['services_unknown_hard']

                states['services']['unreachable'] += realm['services_unreachable_soft']
                states['services']['unreachable'] += realm['services_unreachable_hard']

                states['services']['acknowledge'] += realm['services_acknowledged']
                states['services']['downtime'] += realm['services_in_downtime']

        logger.info('Store current states...')
        self.states['hosts'] = states['hosts']
        self.states['services'] = states['services']

        return states
