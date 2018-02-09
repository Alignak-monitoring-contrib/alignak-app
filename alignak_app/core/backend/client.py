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
    Client manage connection and access to Alignak backend.
"""

import json

from logging import getLogger

from alignak_backend_client.client import Backend, BackendException

from alignak_app.core.backend.data_manager import data_manager
from alignak_app.core.models.daemon import Daemon
from alignak_app.core.models.event import Event
from alignak_app.core.models.history import History
from alignak_app.core.models.host import Host
from alignak_app.core.models.livesynthesis import LiveSynthesis
from alignak_app.core.models.service import Service
from alignak_app.core.models.user import User
from alignak_app.core.utils.config import get_app_config

logger = getLogger(__name__)


class BackendClient(object):
    """
        Class who collect informations with Backend-Client and returns data for Alignak-App.
    """

    def __init__(self):
        self.backend = None
        self.user = {}
        self.connected = False
        self.app = None

    def login(self, username=None, password=None):
        """
        Connect to alignak backend

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
            # Username & password : not recommended, without "login.form.py" form.
            try:
                self.connected = self.backend.login(username, password)
                if self.connected:
                    self.user['username'] = username
                    self.user['token'] = self.backend.token
                logger.info('Connection by password: %s', str(self.connected))
            except BackendException as e:  # pragma: no cover
                logger.error('Connection to Backend has failed: %s', str(e))
        elif username and not password:  # pragma: no cover
            # Username as token : recommended
            self.backend.authenticated = True
            if self.user:
                self.backend.token = self.user['token']
            else:
                self.backend.token = username
                self.user['token'] = username

            # Make backend connected to test token
            self.connected = True
            connection_test = self.get('livesynthesis')

            self.connected = bool(connection_test)
            logger.info('Connection by token: %s', str(self.connected))

            if not self.connected:
                return False
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
            except (BackendException, json.decoder.JSONDecodeError) as e:
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
                except (BackendException, json.decoder.JSONDecodeError) as e:  # pragma: no cover
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

    def get_realm_name(self, endpoint_id):
        """
        Return realm name or alias

        :param endpoint_id: id of endpoint
        :type endpoint_id: str
        :return: realm name or alias
        :rtype: str
        """

        endpoint = '/'.join(
            ['realm', endpoint_id]
        )
        projection = [
            'name',
            'alias'
        ]

        realm = self.get(endpoint, projection=projection)

        if realm:
            if realm['alias']:
                return realm['alias']

            return realm['name']

        return 'n/a'

    def get_period_name(self, endpoint_id):
        """
        Get the period name or alias

        :param endpoint_id: id of endpoint
        :type endpoint_id: str
        :return: name or alias of timeperiod
        :rtype: str
        """

        projection = [
            'name',
            'alias'
        ]

        endpoint = '/'.join(['timeperiod', endpoint_id])

        period = self.get(endpoint, projection=projection)

        if period:
            if 'host' in endpoint or 'service' in endpoint:
                period_items = period['_items'][0]
            else:
                period_items = period

            if 'alias' in period_items:
                return period_items['alias']

            return period_items['name']

        return 'n/a'

    def query_user_data(self):
        """
        Launch request for "user" endpoint

        """

        user = User()

        request_data = user.get_request_model(self.backend.token)

        request = self.get(
            request_data['endpoint'],
            request_data['params'],
            request_data['projection']
        )

        if request:
            user.create(
                request['_items'][0]['_id'],
                request['_items'][0],
                request['_items'][0]['name']
            )
            data_manager.update_database('user', user)

    def query_hosts_data(self):
        """
        Launch request for "host" endpoint

        """

        request_data = Host.get_request_model()

        request = self.get(
            request_data['endpoint'],
            request_data['params'],
            request_data['projection'],
            all_items=True
        )

        hosts_list = []
        if request:
            for item in request['_items']:
                host = Host()

                host.create(
                    item['_id'],
                    item,
                    item['name'],
                )
                hosts_list.append(host)

            if hosts_list:
                data_manager.update_database('host', hosts_list)

    def query_services_data(self):
        """
        Launch request for "service" endpoint

        """

        request_data = Service.get_request_model()

        request = self.get(
            request_data['endpoint'],
            request_data['params'],
            request_data['projection'],
            all_items=True
        )

        if request:
            services_list = []
            for item in request['_items']:
                service = Service()

                service.create(
                    item['_id'],
                    item,
                    item['name'],
                )

                services_list.append(service)

            if services_list:
                data_manager.update_database('service', services_list)

    def query_daemons_data(self):
        """
        Launch request for "alignakdaemon" endpoint

        """

        request_data = Daemon.get_request_model()

        request = self.get(
            request_data['endpoint'],
            request_data['params'],
            request_data['projection'],
            all_items=True
        )

        if request:
            daemons_list = []
            for item in request['_items']:
                daemon = Daemon()

                daemon.create(
                    item['_id'],
                    item,
                    item['name'],
                )

                daemons_list.append(daemon)

            if daemons_list:
                data_manager.update_database('alignakdaemon', daemons_list)

    def query_livesynthesis_data(self):
        """
        Launch request for "livesynthesis" endpoint

        """

        request_data = LiveSynthesis.get_request_model()

        request = self.get(
            request_data['endpoint'],
            request_data['params'],
            request_data['projection'],
            all_items=True
        )

        if request:
            livesynthesis = []
            for item in request['_items']:
                synthesis = LiveSynthesis()

                synthesis.create(
                    item['_id'],
                    item,
                )

                livesynthesis.append(synthesis)

            if livesynthesis:
                data_manager.update_database('livesynthesis', livesynthesis)

    def query_history_data(self):
        """
        Launch request for "history" endpoint but only for hosts in "data_manager"

        """

        request_data = History.get_request_model()

        history_list = []
        for host in data_manager.database['host']:
            request_data['params']['where'] = json.dumps({
                'host': host.item_id})

            request = self.get(
                request_data['endpoint'],
                request_data['params'],
                request_data['projection'],
                all_items=False
            )
            if request:
                history = History()

                history.create(
                    host.item_id,
                    request['_items'],
                    host.name,
                )

                history_list.append(history)

        if history_list:
            data_manager.update_database('history', history_list)

    def query_notifications_data(self):  # pragma: no cover, notifications can be empty
        """
        Launch request for "history" endpoint but only for notifications of current user

        """

        request_data = Event.get_request_model()

        request = self.get(
            request_data['endpoint'],
            request_data['params'],
            request_data['projection'],
            all_items=False
        )

        if request:
            notifications = []
            for item in request['_items']:
                message_split = item['message'].split(';')
                user = message_split[0].split(':')[1].strip()
                if 'imported_admin' in user:
                    user = 'admin'
                if user == data_manager.database['user'].name:
                    notification = Event()

                    notification.create(
                        item['_id'],
                        item,
                    )

                    notifications.append(notification)

            if notifications:
                data_manager.update_database('notifications', notifications)

    def get_backend_status_icon(self):
        """
        Return backend status icon name

        :return: daemon status icon name
        :rtype: str
        """

        if self.connected:
            return Daemon.get_states('ok')

        return Daemon.get_states('ko')


# Creating "app_backend" variable.
app_backend = BackendClient()
