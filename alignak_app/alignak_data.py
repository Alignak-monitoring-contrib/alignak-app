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


logger = getLogger(__name__)


class AlignakData(object):
    """
        Class who collect informations with Backend-Client and returns data for
        Alignak-App.
    """

    def __init__(self):
        self.backend = None

    def log_to_backend(self, config):
        """
        Connect to backend with credentials in settings.cfg.

        :param config: parser config who contains settings
        :type config: :class:`~configparser.ConfigParser`
        """

        # Credentials
        username = config.get('Backend', 'username')
        password = config.get('Backend', 'password')

        # Backend login
        backend_url = config.get('Backend', 'backend_url')
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
