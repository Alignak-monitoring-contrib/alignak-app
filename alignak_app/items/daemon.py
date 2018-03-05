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
    Daemon
    ++++++
    Daemon manage creation of daemon item for backend ``alignakdaemon`` endpoint
"""


from logging import getLogger

from alignak_app.backend.datamanager import data_manager
from alignak_app.items.item import Item

logger = getLogger(__name__)


class Daemon(Item):
    """
        Class who create a daemon item
    """

    def __init__(self):
        super(Daemon, self).__init__()
        self.item_type = 'alignakdaemon'

    @staticmethod
    def get_request_model():
        """
        Return the request model for alignakdaemon requests

        :return: request model for alignakdaemon endpoint
        :rtype: dict
        """

        daemons_projection = [
            'alive', 'type', 'name', 'reachable', 'spare', 'address', 'port', 'passive',
            'last_check'
        ]

        request_model = {
            'endpoint': 'alignakdaemon',
            'params': None,
            'projection': daemons_projection
        }

        return request_model

    @staticmethod
    def get_daemons_names():
        """
        Returns all the names of daemons

        :return: all the names of daemons
        :rtype: list
        """

        return [
            'poller',
            'receiver',
            'reactionner',
            'arbiter',
            'scheduler',
            'broker'
        ]

    @staticmethod
    def get_states(status):
        """
        Return states of daemons or backend

        :param status: status of item
        :type status: str
        :return: the status string
        :rtype: str
        """

        states = {
            'ok': 'connected',
            'flapping': 'flapping',
            'ko': 'disconnected',
            'not_connect': 'not_connect',
        }

        return states[status]

    @staticmethod
    def get_daemons_status_icon():
        """
        Return daemons status icon name

        :return: daemons status icon name
        :rtype: str
        """

        alignak_daemons = data_manager.database['alignakdaemon']

        daemons_down = 0
        daemons_nb = len(alignak_daemons)
        for daemon in alignak_daemons:
            daemons_nb += 1
            if not daemon.data['alive']:
                daemons_down += 1

        if daemons_down == daemons_nb:
            status = 'ko'
        elif daemons_down > 0:
            status = 'flapping'
        else:
            status = 'ok'

        if daemons_nb == 0:
            status = 'not_connect'

        return Daemon.get_states(status)
