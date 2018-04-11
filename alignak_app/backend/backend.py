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
from alignak_app.backend.ws_client import WSClient

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
        self.ws_client = WSClient()

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
            connection_test = self.get('user', {'projection': json.dumps({'name': 1})})

            self.connected = bool(connection_test)
            if not check:
                logger.info('Connection by token: %s', self.connection_status[self.connected])
        else:
            logger.warning(
                'Connection to Backend has failed.\n'
                'Check [Alignak] section in configuration file or use login window of application.'
            )

        if self.connected and not check:
            self.ws_client.login(self.user['token'])

        return self.connected

    def get(self, endpoint, params=None, projection=None, all_items=False):
        """
        GET on alignak Backend REST API

        :param endpoint: endpoint (API URL)
        :type endpoint: str
        :param params: dict of parameters for the app_backend API
        :type params: dict|None
        :param projection: list of field to get, if None, get all
        :type projection: list|None
        :param all_items: make GET on all items
        :type all_items: bool
        :return: request response
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

    def acknowledge(self, item, sticky, notify, comment):  # pragma: no cover
        """
        Prepare data for acknowledge and POST on backend API or WS if available

        :param item: item to acknowledge: host | service
        :type item: alignak_app.items.host.Host | alignak_app.items.service.Service
        :param sticky: define if ack is sticky or not
        :type sticky: bool
        :param notify: define if ack should notify user or not
        :type notify: bool
        :param comment: comment of ack
        :type comment: str
        :return: request response
        :rtype: dict
        """

        user = data_manager.database['user']

        if self.ws_client.auth:
            if item.item_type == 'service':
                command = 'ACKNOWLEDGE_SVC_PROBLEM'
                host = data_manager.get_item('host', '_id', item.data['host'])
                element = host.name
                item_name = item.name
            else:
                command = 'ACKNOWLEDGE_HOST_PROBLEM'
                element = item.name
                item_name = item.name
            if sticky:
                sticky = '2'
            else:
                sticky = '1'
            if notify:
                notify = '1'
            else:
                notify = '0'
            persistent = '0'

            parameters = ';'.join([item_name, sticky, notify, persistent, user.name, comment])
            data = {
                'command': command,
                'element': element,
                'parameters': parameters
            }
            request = self.ws_client.post('command', params=data)
        else:
            data = {
                'action': 'add',
                'user': user.item_id,
                'comment': comment,
                'notify': notify,
                'sticky': sticky
            }
            if item.item_type == 'service':
                data['host'] = item.data['host']
                data['service'] = item.item_id
            else:
                data['host'] = item.item_id
                data['service'] = None

            request = self.post('actionacknowledge', data)

        return request

    # pylint: disable=too-many-arguments
    def downtime(self, item, fixed, duration, start_stamp, end_stamp, comment):  # pragma: no cover
        """
        Prepare data for downtime and POST on backend API or WS if available

        :param item: item to downtime: host | service
        :type item: alignak_app.items.host.Host | alignak_app.items.service.Service
        :param fixed: define if donwtime is fixed or not
        :type fixed: bool
        :param duration: duration timestamp of downtime
        :type duration: int
        :param start_stamp: start timestamp of downtime
        :type start_stamp: int
        :param end_stamp: end timestamp of downtime
        :type end_stamp: int
        :param comment: comment of downtime
        :type comment: str
        :return: request response
        :rtype: dict
        """

        if self.ws_client.auth:
            if item.item_type == 'service':
                host = data_manager.get_item('host', '_id', item.data['host'])
                element = host.name
            else:
                element = item.name
            if fixed:
                fixed = '1'
            else:
                fixed = '0'
            item_name = item.name
            trigger_id = '0'
            parameters = ';'.join(
                [item_name, str(start_stamp), str(end_stamp), fixed, trigger_id, str(duration),
                 data_manager.database['user'].name, comment]
            )
            data = {
                'command': 'SCHEDULE_SVC_DOWNTIME' if item.item_type == 'service' else
                           'SCHEDULE_HOST_DOWNTIME',
                'element': element,
                'parameters': parameters
            }
            request = self.ws_client.post('command', params=data)
        else:
            data = {
                'action': 'add',
                'user': data_manager.database['user'].item_id,
                'fixed': fixed,
                'duration': duration,
                'start_time': start_stamp,
                'end_time': end_stamp,
                'comment': comment,
            }

            if item.item_type == 'service':
                data['host'] = item.data['host']
                data['service'] = item.item_id
            else:
                data['host'] = item.item_id
                data['service'] = None

            request = app_backend.post('actiondowntime', data)

        return request

    def query_realms(self):
        """
        Launch a request on ``realm`` endpoint

        """

        request_model = Realm.get_request_model()

        request = self.get(
            request_model['endpoint'],
            request_model['params'],
            request_model['projection']
        )

        if request:
            realms_list = []
            for backend_item in request['_items']:
                realm = Realm()

                realm.create(
                    backend_item['_id'],
                    backend_item,
                    backend_item['name'],
                )
                realms_list.append(realm)

            if realms_list:
                data_manager.update_database('realm', realms_list)
            if 'OK' in request['_status']:
                data_manager.db_is_ready[request_model['endpoint']] = True

    def query_timeperiods(self):
        """
        Launch a request on ``timeperiod`` endpoint

        """

        request_model = Period.get_request_model()

        request = self.get(
            request_model['endpoint'],
            request_model['params'],
            request_model['projection']
        )

        if request:
            periods_list = []
            for backend_item in request['_items']:
                period = Period()

                period.create(
                    backend_item['_id'],
                    backend_item,
                    backend_item['name'],
                )
                periods_list.append(period)

            if periods_list:
                data_manager.update_database('timeperiod', periods_list)
            if 'OK' in request['_status']:
                data_manager.db_is_ready[request_model['endpoint']] = True

    def query_user(self):
        """
        Launch request on "user" endpoint. Only for current App user.

        """

        request_model = User.get_request_model(self.backend.token)

        request = self.get(
            request_model['endpoint'],
            request_model['params'],
            request_model['projection']
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
                data_manager.db_is_ready[request_model['endpoint']] = True

    def query_hosts(self):
        """
        Launch request on "host" endpoint, add hosts in problems if needed

        """

        request_model = Host.get_request_model()

        request = self.get(
            request_model['endpoint'],
            request_model['params'],
            request_model['projection'],
            all_items=True
        )

        if request:
            hosts_list = []
            for backend_item in request['_items']:
                host = Host()

                host.create(
                    backend_item['_id'],
                    backend_item,
                    backend_item['name'],
                )
                hosts_list.append(host)

                # If host is a problem, add / update it
                if data_manager.is_problem('host', backend_item):
                    if data_manager.get_item('problems', host.item_id):
                        data_manager.update_item_data('problems', host.item_id, host.data)
                    else:
                        data_manager.database['problems'].append(host)

            data_manager.db_is_ready['problems']['host'] = True

            if hosts_list:
                data_manager.update_database('host', hosts_list)
            if 'OK' in request['_status']:
                data_manager.db_is_ready[request_model['endpoint']] = True

    def query_services(self, host_id=None):
        """
        Launch request for "service" endpoint. If ``host_id`` is given, only services related to
        host are added / updated

        :param host_id: "_id" of host
        :type host_id: str
        """

        request_model = Service.get_request_model(host_id)

        request = self.get(
            request_model['endpoint'],
            request_model['params'],
            request_model['projection'],
            all_items=True
        )

        if request:
            services_list = []
            for backend_item in request['_items']:
                service = Service()

                service.create(
                    backend_item['_id'],
                    backend_item,
                    backend_item['name'],
                )

                # Add / update only services of host "if host_id"
                if host_id:
                    if not data_manager.get_item('service', service.item_id):
                        data_manager.database['service'].append(service)
                    else:
                        data_manager.update_item_data('service', service.item_id, service.data)

            # If not item ID, update all database
            if services_list and not host_id:
                data_manager.update_database('service', services_list)
            if 'OK' in request['_status']:
                data_manager.db_is_ready[request_model['endpoint']] = True

    def query_services_problems(self, state):
        """
        Launch requests on "service" endpoint to get items with "ls_state = state"

        Wanted states are: ``WARNING``, ``CRITICAL`` and ``UNKNOWN``

        :param state: state of service
        :type state: str
        """

        # Services
        services_projection = [
            'name', 'host', 'alias', 'ls_state', 'ls_output', 'ls_acknowledged', 'ls_downtimed'
        ]

        params = {'where': json.dumps({'_is_template': False, 'ls_state': state})}
        request = self.get(
            'service',
            params,
            services_projection,
            all_items=True
        )

        if request:
            for backend_item in request['_items']:
                if data_manager.is_problem('service', backend_item):
                    service = Service()
                    service.create(
                        backend_item['_id'],
                        backend_item,
                        backend_item['name']
                    )

                    if data_manager.get_item('problems', service.item_id):
                        data_manager.update_item_data('problems', service.item_id, service.data)
                    else:
                        data_manager.database['problems'].append(service)
            # Problems state is ready
            data_manager.db_is_ready['problems'][state] = True
            logger.info("Update database[problems] for %s services...", state)

    def query_alignakdaemons(self):
        """
        Launch request on "alignakdaemon" endpoint

        """

        request_model = Daemon.get_request_model()

        request = self.get(
            request_model['endpoint'],
            request_model['params'],
            request_model['projection'],
            all_items=True
        )

        if request:
            daemons_list = []
            for backend_item in request['_items']:
                daemon = Daemon()

                daemon.create(
                    backend_item['_id'],
                    backend_item,
                    backend_item['name'],
                )

                daemons_list.append(daemon)

            if daemons_list:
                data_manager.update_database('alignakdaemon', daemons_list)
            if 'OK' in request['_status']:
                data_manager.db_is_ready[request_model['endpoint']] = True

    def query_livesynthesis(self):
        """
        Launch request on "livesynthesis" endpoint

        """

        request_model = LiveSynthesis.get_request_model()

        request = self.get(
            request_model['endpoint'],
            request_model['params'],
            request_model['projection'],
            all_items=True
        )

        if request:
            livesynthesis = []
            for backend_item in request['_items']:
                synthesis = LiveSynthesis()

                synthesis.create(
                    backend_item['_id'],
                    backend_item,
                )

                livesynthesis.append(synthesis)

            if livesynthesis:
                data_manager.update_database('livesynthesis', livesynthesis)
            if 'OK' in request['_status']:
                data_manager.db_is_ready[request_model['endpoint']] = True

    def query_history(self, hostname=None, host_id=None):
        """
        Launch request on "history" endpoint but only for hosts in "data_manager"

        :param hostname: name of host we want history
        :type hostname: str
        :param host_id: id of host for history
        :type host_id: str
        """

        request_model = History.get_request_model()

        if hostname and host_id:
            request_model['params']['where'] = json.dumps({
                'host': host_id})
            request_model['params']['max_results'] = 25

            request = self.get(
                request_model['endpoint'],
                request_model['params'],
                request_model['projection'],
                all_items=False
            )

            if request:
                logger.debug('Add / Update history for %s (%s)', hostname, host_id)
                if data_manager.get_item('history', host_id):
                    data_manager.update_item_data('history', host_id, request['_items'])
                else:
                    host_history = History()

                    host_history.create(
                        host_id,
                        request['_items'],
                        hostname,
                    )
                    data_manager.database['history'].append(host_history)
        else:  # pragma: no cover, too long to test
            history_list = []
            for history in data_manager.database['history']:
                request_model['params']['where'] = json.dumps({
                    'host': history.item_id})
                request_model['params']['max_results'] = 25

                request = self.get(
                    request_model['endpoint'],
                    request_model['params'],
                    request_model['projection'],
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

        request_model = Event.get_request_model()

        request = self.get(
            request_model['endpoint'],
            request_model['params'],
            request_model['projection'],
            all_items=False
        )

        if request:
            notifications = []
            for backend_item in request['_items']:
                message_split = backend_item['message'].split(';')
                user = message_split[0].split(':')[1].strip()
                if 'imported_admin' in user:
                    user = 'admin'
                if user == data_manager.database['user'].name:
                    notification = Event()

                    notification.create(
                        backend_item['_id'],
                        backend_item,
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


# Creation of "app_backend" object
app_backend = BackendClient()
