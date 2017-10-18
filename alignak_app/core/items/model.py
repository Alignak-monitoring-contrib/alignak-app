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
    ItemModel manage creation of items
"""


from logging import getLogger


logger = getLogger(__name__)


class ItemModel(object):
    """
        Class who create item
    """

    def __init__(self):
        self.item_type = 'model'
        self.item_id = ''
        self.name = ''
        self.data = None

    def create(self, _id, data, name=None):
        """
        Create wanted item

        :param _id: id of the item. Often equal to id in alignak backend
        :type _id: str
        :param data: data of the item
        :type data: dict | list
        :param name: name of the item if available
        :type name: str
        """

        self.item_id = _id
        self.data = data

        if name:
            self.name = name

    def get_data(self, key):
        """
        Return key data of item

        :param key: the key who contain the wanted data
        :type key: str
        :return: the wanted data
        """

        return self.data[key]

    def update_data(self, key, new_value):
        """
        Update data of the wanted key

        :param key: key to update
        :type key: str
        :param new_value: new value of the key
        """

        self.data[key] = new_value


def get_icon_name(item_type, state, acknowledge, downtime):
    """
    Return icon for a host or a service item

    :param item_type: type of item: host | service
    :type item_type: str
    :param state: state of item
    :type state: str
    :param acknowledge: if item is acknowledged or not
    :type acknowledge: bool
    :param downtime: if item is downtimed
    :type downtime: bool
    :return: icon name for icon
    :rtype: str
    """

    if downtime:
        return 'downtime'
    if acknowledge:
        return 'acknowledge'

    available_icons = {
        'host': {
            'UP': 'hosts_up',
            'UNREACHABLE': 'hosts_unreachable',
            'DOWN': 'hosts_down',
        },
        'service': {
            'OK': 'services_ok',
            'WARNING': 'services_warning',
            'CRITICAL': 'services_critical',
            'UNKNOWN': 'services_unknown',
            'UNREACHABLE': 'services_unreachable'
        }
    }
    try:
        return available_icons[item_type][state]
    except KeyError as e:
        logger.error('Wrong KEY for get_icon(): %s', e)
        return 'error'


def get_icon_name_from_state(item_type, state):
    """
    Return icon name from state for host or service

    :param item_type: type of item: host or service
    :type item_type: str
    :param state: state of item
    :type state: str
    :return:
    """

    if state == 'DOWNTIME':
        return 'downtime'
    if state == 'ACKNOWLEDGE':
        return 'acknowledge'

    return '%ss_%s' % (item_type, state.lower())


def get_real_host_state_icon(services):
    """
    Return corresponding icon to number of services who are in alert

    :param services: list of Service items
    :type services: list
    :return: icon corresponding to state
    :rtype: str
    """

    if services:
        icon_names = [
            'all_services_ok',
            'all_services_ok',
            'all_services_ok',
            'all_services_warning',
            'all_services_critical'
        ]
        state_lvl = []

        for service in services:
            state_lvl.append(service.data['_overall_state_id'])

        max_state_lvl = max(state_lvl)

        return icon_names[max_state_lvl]

    logger.error('Empty services in get_real_host_state_icon()')
    return 'error'
