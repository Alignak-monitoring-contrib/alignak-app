#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2018:
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
    Backend
    +++++++
    Backend manage connection and access to Alignak backend. It also fill
    :class:`DataManager <alignak_app.backend.datamanager.DataManager>`.
"""

import json

from logging import getLogger

from alignak_backend_client.client import Backend, BackendException

from alignak_app.backend.datamanager import data_manager

from alignak_app.items.daemon import Daemon
from alignak_app.items.event import Event
from alignak_app.items.history import History
from alignak_app.items.host import Host
from alignak_app.items.livesynthesis import LiveSynthesis
from alignak_app.items.service import Service
from alignak_app.items.user import User
from alignak_app.items.realm import Realm
from alignak_app.items.period import Period

from alignak_app.utils.config import settings

logger = getLogger(__name__)


class BackendClient(object):
    """
        Class who collect informations with Backend-Client and returns data for Alignak-App.
    """

    connection_status = {
        True: 'Success',
        False: 'Failure'
    }

    def __init__(self):
        self.backend = None
        self.connected = False
        self.user = {}

    def login(self, username=None, password=None, proxies=None, check=False):
        """
        Connect to alignak backend

        :param username: name or token of user
        :type username: str
        :param password: password of user. If token given, this parameter is useless
        :type password: str
        :param proxies: dictionnary for proxy
        :type proxies: dict
        :param check: define if login is a check or a first login
        :type check: bool
        :return: True if connected or False if not
        :rtype: bool
        """

        # Credentials
        if not username and not password:
            if 'token' in self.user:
                username = self.user['token']

        # Create Backend object
        backend_url = settings.get_config('Alignak', 'backend')
        processes = int(settings.get_config('Alignak', 'processes'))

        self.backend = Backend(backend_url, processes=processes)

        logger.debug('Backend URL : %s', backend_url)
        if not check:
            logger.info('Try to connect to the Alignak backend...')

        if username and password:
            # Username & password : not recommended, without login QDialog
            try:
                self.connected = self.backend.login(username, password, proxies=proxies)
                if self.connected:
                    self.user['username'] = username
                    self.user['token'] = self.backend.token
                logger.info('Connection by password: %s', self.connection_status[self.connected])
            except BackendException:  # pragma: no cover
                logger.error('Connection to Backend has failed !')
        elif username and not password:
            # Username as token : recommended
            if 'token' in self.user:
                self.backend.set_token(self.user['token'])
            else:
                self.backend.set_token(username)
                self.user['token'] = username

            # Make backend connected to test token
            self.connected = True
            connection_test = self.get('alignak', {'projection': json.dumps({'name': 1})})

            self.connected = bool(connection_test)
            if not check:
                logger.info('Connection by token: %s', self.connection_status[self.connected])
        else:
            logger.warning(
                'Connection to Backend has failed.\n'
                'Check [Alignak] section in configuration file or use login window of application.'
            )

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
        :return: desired request of app_backend
        :rtype: dict
        """

        request = None

        if self.connected:
            if params is None:
                params = {'max_results': 50}
            if projection is not None:
                generate_proj = {}
                for field in projection:
                    generate_proj[field] = 1
                params['projection'] = json.dumps(generate_proj)
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
                logger.info('GET on [%s] backend > %s', endpoint, str(request['_status']))
                logger.debug('\tparams: [%s]', str(params))
            except BackendException:
                self.connected = False
        else:
            logger.info('App is not connected to backend !')

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
                logger.info('POST on [%s] backend > %s', endpoint, str(request['_status']))
                logger.debug('\tdata: [%s]', str(data))
                logger.debug('\theaders: [%s]', str(headers))
            except BackendException:
                self.connected = False
        else:
            logger.info('App is not connected to backend !')

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
                logger.info('PATCH on [%s] backend > %s', endpoint, str(request['_status']))
                logger.debug('\tdata: [%s]', str(data))
                logger.debug('\theaders: [%s]', str(headers))
            except BackendException:
                self.connected = False
        else:
            logger.info('App is not connected to backend !')

        return request

    def query_realms(self):
        """
        Launch a request on ``realm`` endpoint

        """

        request_data = Realm.get_request_model()

        request = self.get(
            request_data['endpoint'],
            request_data['params'],
            request_data['projection']
        )

        if request:
            realms_list = []
            for item in request['_items']:
                realm = Realm()

                realm.create(
                    item['_id'],
                    item,
                    item['name'],
                )
                realms_list.append(realm)

            if realms_list:
                data_manager.update_database('realm', realms_list)
            if 'OK' in request['_status']:
                data_manager.db_is_ready[request_data['endpoint']] = True

    def query_timeperiods(self):
        """
        Launch a request on ``timeperiod`` endpoint

        """

        request_data = Period.get_request_model()

        request = self.get(
            request_data['endpoint'],
            request_data['params'],
            request_data['projection']
        )

        if request:
            periods_list = []
            for item in request['_items']:
                period = Period()

                period.create(
                    item['_id'],
                    item,
                    item['name'],
                )
                periods_list.append(period)

            if periods_list:
                data_manager.update_database('timeperiod', periods_list)
            if 'OK' in request['_status']:
                data_manager.db_is_ready[request_data['endpoint']] = True

    def query_user(self):
        """
        Launch request on "user" endpoint. Only for current App user.

        """

        request_data = User.get_request_model(self.backend.token)

        request = self.get(
            request_data['endpoint'],
            request_data['params'],
            request_data['projection']
        )

        if request:
            if request['_items']:
                user = User()

                user.create(
                    request['_items'][0]['_id'],
                    request['_items'][0],
                    request['_items'][0]['name']
                )

                data_manager.update_database('user', user)

            if 'OK' in request['_status']:
                data_manager.db_is_ready[request_data['endpoint']] = True

    def query_hosts(self):
        """
        Launch request on "host" endpoint

        """

        request_data = Host.get_request_model()

        request = self.get(
            request_data['endpoint'],
            request_data['params'],
            request_data['projection'],
            all_items=True
        )

        if request:
            hosts_list = []
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
            if 'OK' in request['_status']:
                data_manager.db_is_ready[request_data['endpoint']] = True

    def query_services(self, host_id=None):
        """
        Launch request for "service" endpoint

        :param host_id: "_id" of host, needed to get only host services
        :type host_id: str
        """

        request_data = Service.get_request_model(host_id)

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

                if host_id:
                    if not data_manager.get_item('service', service.item_id):
                        # Append service if not in list
                        data_manager.database['service'].append(service)
                    else:
                        # Else we update existing item
                        data_manager.update_item_data('service', service.item_id, service.data)

            if services_list and not host_id:
                # If not item ID, update all database
                data_manager.update_database('service', services_list)
            if 'OK' in request['_status']:
                data_manager.db_is_ready[request_data['endpoint']] = True

    def query_problems(self, states):
        """
        Launch requests on "service" endpoint to get items in problems and add hosts in problems:

        * **Hosts**: ``DOWN``, ``UNREACHABLE``
        * **Services**: ``WARNING``, ``CRITICAL``, ``UNKNOWN``
        """

        # Reset if states is equal to 3 (WARNING, CRITICAL, UNKNOWN)
        if len(states) == 3:
            data_manager.new_database['problems'] = []

        # Services
        services_projection = [
            'name', 'host', 'alias', 'ls_state', 'ls_output', 'ls_acknowledged', 'ls_downtimed'
        ]

        for state in states:
            params = {'where': json.dumps({'_is_template': False, 'ls_state': state})}
            request = self.get(
                'service',
                params,
                services_projection,
                all_items=True
            )
            if request:
                for item in request['_items']:
                    if not item['ls_acknowledged'] and not item['ls_downtimed']:
                        service = Service()
                        service.create(
                            item['_id'],
                            item,
                            item['name']
                        )
                        data_manager.new_database['problems'].append(service)

        # If new problems
        if data_manager.new_database['problems']:
            # Append states
            data_manager.db_is_ready['problems'].append(states)

            # If problems is the last, add hosts to problems
            if len(data_manager.db_is_ready['problems']) > 2:
                for host in data_manager.database['host']:
                    if host.data['ls_state'] in ['DOWN', 'UNREACHABLE'] and \
                            not host.data['ls_acknowledged'] and \
                            not host.data['ls_downtimed'] and \
                            not data_manager.get_item('problems', host.item_id):
                        data_manager.new_database['problems'].append(host)

                # Update "problems" database
                data_manager.database['problems'] = []
                while data_manager.new_database['problems']:
                    data_manager.database['problems'].append(
                        data_manager.new_database['problems'].pop()
                    )
                logger.info("Update database[problems]...")
            if len(data_manager.db_is_ready['problems']) > 3:
                data_manager.db_is_ready['problems'] = []

    def query_alignakdaemons(self):
        """
        Launch request on "alignakdaemon" endpoint

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
            if 'OK' in request['_status']:
                data_manager.db_is_ready[request_data['endpoint']] = True

    def query_livesynthesis(self):
        """
        Launch request on "livesynthesis" endpoint

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
            if 'OK' in request['_status']:
                data_manager.db_is_ready[request_data['endpoint']] = True

    def query_history(self, hostname=None, host_id=None):
        """
        Launch request on "history" endpoint but only for hosts in "data_manager"

        :param hostname: name of host we want history
        :type hostname: str
        :param host_id: id of host for history
        :type host_id: str
        """

        request_data = History.get_request_model()

        if hostname and host_id:
            request_data['params']['where'] = json.dumps({
                'host': host_id})

            request = self.get(
                request_data['endpoint'],
                request_data['params'],
                request_data['projection'],
                all_items=False
            )

            if request:
                host_history = History()

                host_history.create(
                    host_id,
                    request['_items'],
                    hostname,
                )
                logger.debug('Add history for %s (%s)', hostname, host_id)
                data_manager.database['history'].append(host_history)
        else:  # pragma: no cover, too long to test
            history_list = []
            for history in data_manager.database['history']:
                request_data['params']['where'] = json.dumps({
                    'host': history.item_id})

                request = self.get(
                    request_data['endpoint'],
                    request_data['params'],
                    request_data['projection'],
                    all_items=False
                )

                if request:
                    host_history = History()

                    host_history.create(
                        history.item_id,
                        request['_items'],
                        history.name,
                    )
                    history_list.append(host_history)

            if history_list:
                data_manager.update_database('history', history_list)

    def query_notifications(self):  # pragma: no cover, notifications can be empty
        """
        Launch request on "history" endpoint.
        Only for 'type': 'monitoring.notification' and for current App user

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
