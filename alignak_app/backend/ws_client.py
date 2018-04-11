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
    WS Client
    +++++++++
    WS Client manage connection and access to Alignak backend by the Web Service module. It will
    also fill :class:`DataManager <alignak_app.backend.datamanager.DataManager>` in future versions.
"""

import json
from logging import getLogger

import requests

from requests import HTTPError
from requests import ConnectionError as RequestsConnectionError

from alignak_app.utils.config import settings

logger = getLogger(__name__)


class WSClient(object):
    """
        Class who manage Web Service requests
    """

    def __init__(self):
        self.ws_backend = ''
        self.token = ''
        self.auth = None

    def login(self, token):
        """
        Login to Web Service. Used only to ensure that the user token is identical

        :param token: user's token of App
        :type token: str
        """

        self.ws_backend = settings.get_config('Alignak', 'webservice')

        try:
            # WS login
            logger.info("Requesting Web Service authentication with token: %s", token)
            headers = {'Content-Type': 'application/json'}
            params = {'username': token, 'password': ''}
            response = requests.post(
                '/'.join([self.ws_backend, 'login']), json=params, headers=headers
            )

            resp = response.json()

            if '_result' in resp:
                assert token == resp['_result'][0]
                self.token = token
                self.auth = requests.auth.HTTPBasicAuth(self.token, '')
        except (RequestsConnectionError, AssertionError) as exp:
            msg = 'Connection to Web Service on [%s] has failed' % \
                  '/'.join([self.ws_backend, 'login'])
            logger.warning(msg)
            logger.debug(exp)

    def get(self, endpoint, params):  # pragma: no cover
        """
        GET on alignak Backend Web Service

        :param endpoint: WS endpoint
        :type endpoint: str
        :param params: dict of parameters for the WS
        :type params: dict|None
        :return: request result
        :rtype: dict
        """

        request = None

        try:
            request = requests.get(
                '/'.join([self.ws_backend, endpoint]), params=params, auth=self.auth
            )
            logger.info('GET on [%s] web service > %s', endpoint, str(request))

            request.raise_for_status()
            logger.debug('\tparams: [%s]', str(params))

        except RequestsConnectionError as exp:
            logger.error("Backend connection error, error: %s", exp)

        return request.json()

    def post(self, endpoint, params=None):  # pragma: no cover
        """
        Post on alignak Backend Web Service

        :param endpoint: WS endpoint
        :type endpoint: str
        :param params: dict of parameters for the WS
        :type params: dict
        :return: list of properties when query item | list of items when get many items
        :rtype: list
        """

        request = None

        try:
            headers = {'Content-Type': 'application/json'}
            params = json.dumps(params)

            request = requests.post(
                '/'.join([self.ws_backend, endpoint]), data=params, headers=headers, auth=self.auth
            )

            request.raise_for_status()
            logger.info('POST on [%s] backend > %s', endpoint, str(request))
            logger.debug('\tdata: [%s]', str(params))
            logger.debug('\theaders: [%s]', str(headers))
        except (RequestsConnectionError, HTTPError) as exp:
            logger.warning("WS connection error, error: %s", str(exp))

        except Exception as exp:
            logger.exception("WS exception, error: %s", exp)

        return request.json()
