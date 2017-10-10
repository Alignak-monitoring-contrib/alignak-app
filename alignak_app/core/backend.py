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
    App Backend manage connexion and access to app_backend.
"""

import json
from logging import getLogger

from alignak_backend_client.client import Backend, BackendException

from alignak_app.core.utils import get_app_config
from alignak_app.core.data_manager import data_manager

logger = getLogger(__name__)


class AppBackend(object):
    """
        Class who collect informations with Backend-Client and returns data for
        Alignak-App.
    """

    def __init__(self):
        self.backend = None
        self.user = {}
        self.connected = False
        self.app = None

    def login(self, username=None, password=None):
        """
        Connect to app_backend with credentials in settings.cfg.

        :param username: name or token of user
        :type username: str
        :param password: password of user. If token given, this parameter is useless
        :type password: str
        :return: True if connected or False if not
        :rtype: bool
        """

        # Credentials
        if not username and not password:
            if data_manager.is_ready():
                username = data_manager.database['user'].name
            else:
                username = get_app_config('Alignak', 'username')
                password = get_app_config('Alignak', 'password')

        # Create Backend object
        backend_url = get_app_config('Alignak', 'backend')
        processes = int(get_app_config('Alignak', 'processes'))

        self.backend = Backend(backend_url, processes=processes)

        logger.debug('Backend URL : %s', backend_url)
        logger.info('Try to connect to app_backend...')

        if username and password:
            # Username & password : not recommended, without "widgets.login.py" form.
            try:
                self.connected = self.backend.login(username, password)
                if self.connected:
                    self.user['username'] = username
                    self.user['token'] = self.backend.token
                logger.info('Connection by password: %s', str(self.connected))
            except BackendException as e:  # pragma: no cover
                logger.error('Connection to Backend has failed: %s', str(e))
        elif username and not password:
            # Username as token : recommended
            self.backend.authenticated = True
            if self.user:
                self.backend.token = self.user['token']
            else:
                self.backend.token = username
                self.user['token'] = username

            # Make backend connected to test token
            self.connected = True
            user = self.get('livesynthesis')

            self.connected = bool(user)
            if not self.connected:
                return False

            logger.info('Connection by token: %s', str(self.connected))
        else:
            # Else exit
            logger.error(
                'Connection to Backend has failed.\nCheck [Backend] section in configuration file.'
            )
            return False

        return self.connected

    def get(self, endpoint, params=None, projection=None, all_items=False):
        """
        GET on alignak Backend REST API.

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :param params: dict of parameters for the app_backend API
        :type params: dict|None
        :param projection: list of field to get, if None, get all
        :type projection: list|None
        :param all_items: make GET on all items
        :type all_items: bool
        :return desired request of app_backend
        :rtype: dict
        """

        request = None

        if params is None:
            params = {'max_results': 50}
        if projection is not None:
            generate_proj = {}
            for field in projection:
                generate_proj[field] = 1
            params['projection'] = json.dumps(generate_proj)

        if self.connected:
            # Request
            try:
                if not all_items:
                    request = self.backend.get(
                        endpoint,
                        params
                    )
                else:
                    request = self.backend.get_all(
                        endpoint,
                        params
                    )
                logger.debug('GET: %s', endpoint)
                logger.debug('..with params: %s', str(params))
                logger.debug('...Response > %s', str(request['_status']))
            except BackendException as e:
                logger.warning('First GET failed: %s', str(e))
                logger.warning('...Request: %s', str(request))
                try:
                    request = self.backend.get(
                        endpoint,
                        params
                    )
                    logger.debug('GET (Retry): %s', endpoint)
                    logger.debug('..with params: %s', str(params))
                    logger.debug('...Response > %s', str(request['_status']))
                except BackendException as e:
                    logger.error('GET failed: %s', str(e))
                    logger.error('...Request: %s', str(request))
                    logger.warning('Application checks the connection with the Backend...')
                    self.connected = False
                    if self.app:
                        if not self.app.reconnect_mode:
                            self.app.reconnecting.emit(str(e))
                    return request

        return request

    def post(self, endpoint, data, headers=None):  # pragma: no cover - Post already test by client
        """
        POST on alignak Backend REST API

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :param data: properties of item to create | add
        :type data: dict
        :param headers: headers (example: Content-Type)
        :type headers: dict|None
        :return: response (creation information)
        :rtype: dict
        """

        request = None

        if self.connected:
            try:
                request = self.backend.post(endpoint, data, headers=headers)
                logger.debug('POST on %s', endpoint)
                logger.debug('..with data: %s', str(data))
                logger.debug('...Response > %s', str(request['_status']))
            except BackendException as e:
                logger.error('POST failed: %s', str(e))
                logger.warning('Application checks the connection with the Backend...')
                self.connected = False
                if not self.app.reconnect_mode:
                    self.app.reconnecting.emit(str(e))
                return request

        return request

    def patch(self, endpoint, data, headers):
        """
        PATCH on alignak Backend REST API

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :param data: properties of item to update
        :type data: dict
        :param headers: headers (example: Content-Type). 'If-Match' required
        :type headers: dict
        :return: dictionary containing patch response from the backend
        :rtype: dict
        """

        request = None

        if self.connected:
            try:
                request = self.backend.patch(endpoint, data, headers=headers, inception=True)
                logger.debug('PATCH on %s', endpoint)
                logger.debug('..with data: %s', str(data))
                logger.debug('...with headers: %s', str(headers))
                logger.debug('....Response > %s', str(request['_status']))
            except BackendException as e:  # pragma: no cover
                logger.error('PATCH failed: %s', str(e))
                logger.warning('Application checks the connection with the Backend...')
                self.connected = False
                if not self.app.reconnect_mode:
                    self.app.reconnecting.emit(str(e))
                return False

        return request

    def get_host(self, key, value, projection=None):
        """
        Return the host corresponding to "key"/"value" pair

        :param key: key corresponding to value
        :type key: str
        :param value: value of key
        :type value: str
        :param projection: list of field to get, if None, get all
        :type projection: list|None
        :return: None if not found or item dict
        :rtype: dict|None
        """

        params = {'where': json.dumps({'_is_template': False, key: value})}

        hosts = self.get('host', params, projection=projection)

        if hosts and hosts['_items']:
            wanted_host = hosts['_items'][0]
        else:
            wanted_host = None

        return wanted_host

    def get_service(self, host_id, service_id, projection=None):
        """
        Returns the desired service of the specified host

        :param host_id: "_id" of host
        :type host_id: str
        :param service_id: "_id" of wanted service
        :type service_id: str
        :param projection: list of field to get, if None, get all
        :type projection: list|None
        :return: wanted service
        :rtype: dict
        """

        params = {
            'where': json.dumps({
                '_is_template': False,
                'host': host_id
            })
        }

        services = self.get('service', params=params, projection=projection)

        wanted_service = None
        if services:
            if services['_items']:
                wanted_service = services['_items'][0]
            for service in services['_items']:
                if service['_id'] == service_id:
                    wanted_service = service

        return wanted_service


# Creating "app_backend" variable.
app_backend = AppBackend()
