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
    Item
    ++++
    Item is parent class for all items objects:

    * :class:`Daemon <alignak_app.items.daemon.Daemon>`,
    * :class:`Event <alignak_app.items.event.Event>`,
    * :class:`History <alignak_app.items.history.History>`,
    * :class:`Host <alignak_app.items.host.Host>`,
    * :class:`LiveSynthesis <alignak_app.items.livesynthesis.LiveSynthesis>`,
    * :class:`Period <alignak_app.items.period.Period>`,
    * :class:`Realm <alignak_app.items.realm.Realm>`,
    * :class:`Service <alignak_app.items.service.Service>`,
    * :class:`User <alignak_app.items.user.User>`,
"""


from logging import getLogger

logger = getLogger(__name__)


class Item(object):
    """
        Class who create an item
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

    def update_data(self, key, new_value):
        """
        Update data of the wanted key

        :param key: key to update
        :type key: str
        :param new_value: new value of the key
        """

        self.data[key] = new_value

    def get_tooltip(self):
        """
        Return the tooltip message depending state and actions

        :return: toottip message
        :rtype: str
        """

        action = ''
        if self.data['ls_downtimed']:
            action = _('downtimed')
        if self.data['ls_acknowledged']:
            action = _('acknowledged')
        if not self.data['active_checks_enabled'] and not self.data['passive_checks_enabled']:
            action = _('not monitored')

        if action:
            return _('%s is %s and %s') % (self.name.capitalize(), self.data['ls_state'], action)

        return _('%s is %s') % (self.name.capitalize(), self.data['ls_state'])


def get_icon_name(item_type, state, acknowledge, downtime, monitored):
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
    :param monitored: define if host is monitored or not (0 is not monitored, 1 or 2 is monitored)
    :type monitored: int
    :return: icon name for icon
    :rtype: str
    """

    if downtime:
        return 'downtime'
    if acknowledge:
        return 'acknowledge'
    if monitored == 0:
        if 'host' in item_type:
            return 'hosts_not_monitored'

        return 'services_not_monitored'

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
        logger.error('Wrong KEY for get_icon_name(): %s', e)
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

    :param services: list of Service() items
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
            'all_services_critical',
            'all_services_none'
        ]
        state_lvl = []

        for service in services:
            state_lvl.append(service.data['_overall_state_id'])

        max_state_lvl = max(state_lvl)

        try:
            return icon_names[max_state_lvl]
        except IndexError as e:  # pragma: no cover
            logger.error('get_real_host_state_icon: unkown real state, icon not found: %s', e)
            return icon_names[5]

    logger.error('Empty services in get_real_host_state_icon()')

    return 'all_services_none'


def get_host_msg_and_event_type(host_and_services):
    """
    Return corresponding event icon to number of services who are in alert

    :param host_and_services: Host() item and its Service() items
    :type host_and_services: dict
    :return: event type and message
    :rtype: dict
    """

    host_msg = host_and_services['host'].get_tooltip()

    event_messages = [
        {
            'message': _('%s. You have nothing to do.') % (
                host_msg
            ),
            'event_type': 'OK'
        },
        {
            'message': _('%s and his services are ok or acknowledged.') % (
                host_msg
            ),
            'event_type': 'INFO'
        },
        {
            'message': _('%s and his services are ok or downtimed.') % (
                host_msg
            ),
            'event_type': 'INFO'
        },
        {
            'message': _('%s, some services may be unknown.') % (
                host_msg
            ),
            'event_type': 'WARNING'
        },
        {
            'message': _('%s, some services may be in critical condition or unreachable !') % (
                host_msg
            ),
            'event_type': 'DOWN'
        },
        {
            'message': _('%s, some services are not monitored.') % (
                host_msg
            ),
            'event_type': 'DOWN'
        }
    ]
    state_lvl = []

    for service in host_and_services['services']:
        state_lvl.append(service.data['_overall_state_id'])

    try:
        max_state_lvl = max(state_lvl)
        msg_and_event_type = event_messages[max_state_lvl]
    except IndexError as e:
        logger.error('get_host_msg_and_event_type(): empty services, %s', e)
        return {
            'message': _('Host is %s.') % host_msg,
            'event_type': host_and_services['host'].data['ls_state']
        }
    except ValueError as e:
        logger.warning('No services found for this host: %s', e)
        return {
            'message': _('No services.'),
            'event_type': 'OK'
        }

    return msg_and_event_type
