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
    History
    +++++++
    History manage creation of history item for backend ``history`` endpoint
"""

from logging import getLogger

from alignak_app.items.item import Item

logger = getLogger(__name__)


class History(Item):
    """
        Class who create a history item
    """

    def __init__(self):
        super(History, self).__init__()
        self.item_type = 'history'

    @staticmethod
    def get_request_model():
        """
        Return the request model for history requests

        :return: request model for history endpoint
        :rtype: dict
        """

        request_model = {
            'endpoint': 'history',
            'params': {
                'sort': '-_id',
            },
            'projection': ['service_name', 'message', 'type']
        }

        return request_model

    @staticmethod
    def get_history_icon_name_from_message(message, event_type):
        """
        Return icon name related to message or event type

        :param message: message of an history event
        :type message: str
        :param event_type: type of history event
        :type event_type: str
        :return: icon name
        :rtype: str
        """

        if 'ack' in event_type:
            icon_name = 'acknowledge'
        elif 'downtime' in event_type:
            icon_name = 'downtime'
        elif 'comment' in event_type:
            icon_name = 'edit'
        elif 'request' in event_type:
            icon_name = 'request'
        else:
            if 'UP' in message:
                icon_name = 'hosts_up'
            elif 'DOWN' in message:
                icon_name = 'hosts_down'
            elif 'UNREACHABLE' in message:
                icon_name = 'services_unreachable'
            elif 'OK' in message:
                icon_name = 'services_ok'
            elif 'WARNING' in message:
                icon_name = 'services_warning'
            elif 'CRITICAL' in message:
                icon_name = 'services_critical'
            elif 'UNKNOWN' in message:
                icon_name = 'services_unknown'
            else:
                icon_name = 'error'

        return icon_name
