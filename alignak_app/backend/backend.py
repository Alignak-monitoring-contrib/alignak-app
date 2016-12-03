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
    Alignak Backend manage connexion and access to backend.
"""

import json
import sys
from logging import getLogger

from alignak_backend_client.client import Backend, BackendException

from alignak_app.core.utils import get_app_config

logger = getLogger(__name__)


class AlignakBackend(object):
    """
        Class who collect informations with Backend-Client and returns data for
        Alignak-App.
    """

    def __init__(self):
        self.backend = None
        self.states = {}

    def login(self):
        """
        Connect to backend with credentials in settings.cfg.

        """

        # Credentials
        username = get_app_config('Backend', 'username')
        password = get_app_config('Backend', 'password')

        # Create Backend object
        backend_url = get_app_config('Backend', 'backend_url')
        self.backend = Backend(backend_url)

        logger.debug('Backend URL : ' + backend_url)
        logger.info('Try to connect to backend...')

        if username and password:
            # Username & password : not recommended
            try:
                connect = self.backend.login(username, password)
                logger.debug('Connection : ' + str(connect))
            except BackendException as e:  # pragma: no cover
                sys.exit(e)
        elif username and not password:
            # Username as token : recommended
            self.backend.authenticated = True
            self.backend.token = username
        else:
            # Else exit
            self.exit_error()

    def get(self, endpoint, params=None):
        """
        Collect state of Hosts, via backend API.

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :param params: dict of parameters for the backend API
        :type params: dict
        """

        request = None

        if not params:
            params = {'where': json.dumps({'_is_template': False})}

        # Request
        try:
            request = self.backend.get_all(
                endpoint,
                params
            )
        except BackendException as e:
            logger.warning('Alignak-app failed to collect hosts... \n' + str(e))

        return request

    def get_item(self, item, endpoint, params=None):
        """
        Get a wanted host or service item.

        :param item: name of wanted item : host or service
        :type item: str
        :param endpoint: corresponding endpoint
        :type endpoint: str
        :param params: requested params
        :type params: dict
        :return: None if not found or item dict
        """

        result = self.get(endpoint, params)

        item_result = None

        for current_item in result['_items']:
            print(current_item['name'])
            if current_item['name'] == item:
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

    def get_all_states(self):
        """
        Check the hosts and services states.

        :return: each number of states for hosts and services.
        :rtype: dict
        """

        if not self.backend.authenticated:
            logger.warning('Connection to backend is lost, application will try to reconnect !')
            self.login()

        logger.info('GET state of Host and Services...')

        # Initialize dicts for states
        states = {
            'hosts': {
                'up': 0,
                'down': 0,
                'unreachable': 0
            },
            'services': {
                'ok': 0,
                'critical': 0,
                'unknown': 0,
                'warning': 0
            }
        }

        all_hosts = self.get('host')
        all_services = self.get('service')

        for host in all_hosts['_items']:
            if 'UP' in host['ls_state']:
                states['hosts']['up'] += 1
            if 'UNREACHABLE' in host['ls_state']:
                states['hosts']['unreachable'] += 1
            if 'DOWN' in host['ls_state']:
                states['hosts']['down'] += 1
        for service in all_services['_items']:
            if 'OK' in service['ls_state']:
                states['services']['ok'] += 1
            if 'WARNING' in service['ls_state']:
                states['services']['warning'] += 1
            if 'CRITICAL' in service['ls_state']:
                states['services']['critical'] += 1
            if 'UNKNOWN' in service['ls_state']:
                states['services']['unknown'] += 1

        self.states['hosts'] = states['hosts']
        self.states['services'] = states['services']

        return states

    @staticmethod
    def exit_error(error=''):
        """
        Exit the app if login to backend fails.

        :param error: exception
        :type error: str
        """

        logger.error(
            'Connection to Backend has failed. ' +
            str(error) +
            '\nCheck [Backend] section in configuration file.'
        )
        sys.exit(
            '\nConnection to Backend has failed...' +
            '\nPlease, check your settings and logs.'
        )
