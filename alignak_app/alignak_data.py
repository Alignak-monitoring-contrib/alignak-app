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
        self.current_hosts = {}
        self.current_services = {}
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
                logger.warn('Connection to backend failed !')
        except BackendException as e:
            logger.error(
                'Can\'t connect to Backend. ' +
                str(e) +
                '\nCheck your [settings.cfg] or your backend status.'
            )
            sys.exit()

    def get_host_state(self):
        """
        Collect state of Hosts, via backend API.

        """

        all_host = None

        # Request
        try:
            params = {'where': json.dumps({'_is_template': False})}
            all_host = self.backend.get_all(
                self.backend.url_endpoint_root + '/host', params)
        except BackendException as e:
            logger.error('Can\'t get hosts state \n' + str(e))

        # Store Data
        if all_host:
            for host in all_host['_items']:
                self.current_hosts[host['name']] = host['ls_state']
        else:
            logger.error('AlignakApp has collected 0 hosts !')
        return self.current_hosts

    def get_service_state(self):
        """
        Collect state of Services, via backend API.

        """

        all_services = None

        # Request
        try:
            params = {'where': json.dumps({'_is_template': False})}
            all_services = self.backend.get_all(
                self.backend.url_endpoint_root + '/service', params)
        except BackendException as e:
            logger.error('Can\'t get services state \n' + str(e))

        # Store Data
        if all_services:
            for service in all_services['_items']:
                self.current_services[service['name']] = service['ls_state']
        else:
            logger.error('AlignakApp has collected 0 services !')
        return self.current_services
