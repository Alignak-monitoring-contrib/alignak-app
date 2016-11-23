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
    Alignak_data manage connexion with backend and his data.
"""

import sys
import json

from logging import getLogger
from alignak_backend_client.client import Backend, BackendException
from alignak_app.utils import get_app_config


logger = getLogger(__name__)


class AlignakData(object):
    """
        Class who collect informations with Backend-Client and returns data for
        Alignak-App.
    """

    def __init__(self):
        self.backend = None
        self.states = {}

    def log_to_backend(self):
        """
        Connect to backend with credentials in settings.cfg.

        """

        # Credentials
        username = get_app_config().get('Backend', 'username')
        password = get_app_config().get('Backend', 'password')

        # Backend login
        backend_url = get_app_config().get('Backend', 'backend_url')
        self.backend = Backend(backend_url)

        logger.info('Try to connect to backend...')
        try:
            connect = self.backend.login(username, password)
            if connect:
                logger.info('Connection to backend : OK.')

            else:
                logger.warning('Connection to backend failed !')
        except BackendException as e:  # pragma: no cover
            logger.error(
                'Connection to Backend has failed. ' +
                str(e) +
                '\nCheck [Backend] section in configuration file.'
            )
            sys.exit(
                '\nConnection to Backend has failed...' +
                '\nPlease, check your settings and logs.'
            )

    def get_host_states(self):
        """
        Collect state of Hosts, via backend API.

        """

        all_host = None
        current_hosts = {}

        # Request
        try:
            params = {'where': json.dumps({'_is_template': False})}
            all_host = self.backend.get_all(
                self.backend.url_endpoint_root + '/host', params)
        except BackendException as e:
            logger.warning('Alignak-app failed to collect hosts... \n' + str(e))

        # Store Data
        if all_host:
            for host in all_host['_items']:
                current_hosts[host['name']] = host['ls_state']

        return current_hosts

    def get_service_states(self):
        """
        Collect state of Services, via backend API.

        """

        all_services = None
        current_services = {}

        # Request
        try:
            params = {'where': json.dumps({'_is_template': False})}
            all_services = self.backend.get_all(
                self.backend.url_endpoint_root + '/service', params)
        except BackendException as e:
            logger.warning('Alignak-app failed to collect services... \n' + str(e))

        # Store Data
        if all_services:
            i = 0
            for service in all_services['_items']:
                i += 1
                service_name = service['name'] + '[' + str(i) + ']'
                current_services[service_name] = service['ls_state']

        return current_services

    def get_state(self):
        """
        Check the hosts and services states.

        :return: each states for hosts and services in two dicts.
        :rtype: dict
        """

        if not self.backend.authenticated:
            logger.warning('Connection to backend is lost, application will try to reconnect !')
            self.log_to_backend()

        logger.info('Collect state of Host and Services...')

        # Initialize dicts for states
        hosts_states = {
            'up': 0,
            'down': 0,
            'unreachable': 0
        }
        services_states = {
            'ok': 0,
            'critical': 0,
            'unknown': 0,
            'warning': 0
        }

        # Collect Hosts state
        hosts_data = self.get_host_states()

        if not hosts_data:
            hosts_states['up'] = -1
        else:
            for _, v in hosts_data.items():
                if 'UP' in v:
                    hosts_states['up'] += 1
                if 'DOWN' in v:
                    hosts_states['down'] += 1
                if 'UNREACHABLE' in v:
                    hosts_states['unreachable'] += 1
            hosts_log = str(hosts_states['up']) + ' host(s) Up, ' \
                + str(hosts_states['down']) + ' host(s) Down, ' \
                + str(hosts_states['unreachable']) + ' host(s) unreachable, '
            logger.info(hosts_log)

        # Collect Services state
        services_data = self.get_service_states()

        if not services_data:
            services_states['ok'] = -1
        else:
            for _, v in services_data.items():
                if 'OK' in v:
                    services_states['ok'] += 1
                if 'CRITICAL' in v:
                    services_states['critical'] += 1
                if 'UNKNOWN' in v:
                    services_states['unknown'] += 1
                if 'WARNING' in v:
                    services_states['warning'] += 1
            services_log = str(services_states['ok']) + ' service(s) Ok, ' \
                + str(services_states['warning']) + ' service(s) Warning, ' \
                + str(services_states['critical']) + ' service(s) Critical, ' \
                + str(services_states['unknown']) + ' service(s) Unknown.'
            logger.info(services_log)

        self.states['hosts'] = hosts_states
        self.states['services'] = services_states

        return hosts_states, services_states
