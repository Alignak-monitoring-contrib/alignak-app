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
    DataManager manage alignak data provided by BackendQRunnable
"""

import datetime
from logging import getLogger

from alignak_app.core.items import LiveSynthesis

logger = getLogger(__name__)


class DataManager(object):
    """
        Class who store alignak data
    """

    def __init__(self):
        self.database = {
            'history': [],
            'notifications': [],
            'livesynthesis': [],
            'alignakdaemon': [],
            'host': [],
            'service': [],
            'user': [],
        }
        self.old_notifications = []

    def is_ready(self):
        """
        Check if DataManager is filled and ready

        :return: if ready or not
        :rtype: bool
        """

        if self.database['user'] and self.database['host'] and \
                self.database['service'] and self.database['alignakdaemon'] and \
                self.database['livesynthesis']:
            return True

        return False

    def update_item_database(self, item_type, items_list):
        """
        Update an item type in database

        :param item_type: type of item to update
        :type item_type: str
        :param items_list: list of items for the wanted type
        :type items_list: list | dict
        """

        logger.info("Update database: %s", item_type)

        self.database[item_type] = items_list

    def get_item(self, item_type, key, value=None):
        """
        Return the wanted item for item type who contain the value

        :param item_type: type of wanted item
        :type item_type: str
        :param key: key contained in item
        :type key: str
        :param value: value of the key if needed
        :type value: str
        :return: wanted item
        :rtype: alignak_app.models.item_model.ItemModel
        """

        items = self.database[item_type]

        for item in items:
            if value:
                if item.data[key] == value:
                    return item
            else:
                if item.name == key:
                    return item
                if item.item_id == key:
                    return item

        return None

    def get_synthesis_count(self):
        """
        Get on "synthesis" endpoint and return the states of hosts and services

        :return: states of hosts and services.
        :rtype: dict
        """

        synthesis_count = LiveSynthesis.get_synthesis_count_model()

        live_synthesis = self.database['livesynthesis']

        if live_synthesis:
            for item in live_synthesis:
                realm = item.data
                synthesis_count['hosts']['up'] += realm['hosts_up_soft']
                synthesis_count['hosts']['up'] += realm['hosts_up_hard']

                synthesis_count['hosts']['unreachable'] += realm['hosts_unreachable_soft']
                synthesis_count['hosts']['unreachable'] += realm['hosts_unreachable_hard']

                synthesis_count['hosts']['down'] += realm['hosts_down_soft']
                synthesis_count['hosts']['down'] += realm['hosts_down_hard']

                synthesis_count['hosts']['acknowledge'] += realm['hosts_acknowledged']
                synthesis_count['hosts']['downtime'] += realm['hosts_in_downtime']

                synthesis_count['services']['ok'] += realm['services_ok_soft']
                synthesis_count['services']['ok'] += realm['services_ok_hard']

                synthesis_count['services']['warning'] += realm['services_warning_soft']
                synthesis_count['services']['warning'] += realm['services_warning_hard']

                synthesis_count['services']['critical'] += realm['services_critical_soft']
                synthesis_count['services']['critical'] += realm['services_critical_hard']

                synthesis_count['services']['unknown'] += realm['services_unknown_soft']
                synthesis_count['services']['unknown'] += realm['services_unknown_hard']

                synthesis_count['services']['unreachable'] += realm['services_unreachable_soft']
                synthesis_count['services']['unreachable'] += realm['services_unreachable_hard']

                synthesis_count['services']['acknowledge'] += realm['services_acknowledged']
                synthesis_count['services']['downtime'] += realm['services_in_downtime']

        logger.info('Store current states...')

        return synthesis_count

    def get_all_host_name(self):
        """
        Collect and return all names of all hosts

        :return: all names of all hosts
        :rtype: list
        """

        host_names = []
        for host in self.database['host']:
            host_names.append(host.name)

        return host_names

    def get_host_services(self, host_id):
        """

        :param host_id:
        :return:
        """

        services_of_host = []
        for service in self.database['service']:
            if service.data['host'] == host_id:
                services_of_host.append(service)

        return services_of_host

    def get_host_with_services(self, host_name):
        """
        Returns the desired host and all its services

        :param host_name: desired host
        :type host_name: str
        :return dict with host data and its associated services
        :rtype: dict
        """

        host = self.get_item('host', host_name)

        services_host = self.get_host_services(host.item_id)

        host_data = {
            'host': host,
            'services': services_host
        }

        return host_data

    def get_events(self):
        """
        Get the last events

        :ret
        """

        events = data_manager.database['notifications']
        logger.debug('%s founded: ', str(events))

        notifications_to_send = []
        for event in events:
            # If the notification has not already been sent to the last check
            if event.item_id not in self.old_notifications:
                message_split = event.data['message'].split(';')
                item_type = 'HOST' if 'HOST' in message_split[0] else 'SERVICE'
                host = message_split[1]
                if 'SERVICE' in item_type:
                    service = message_split[2]
                    state = message_split[3]
                    output = message_split[5]
                else:
                    service = ''
                    state = message_split[2]
                    output = message_split[4]

                # Convert updated date to user local time
                gmt_time = datetime.datetime.strptime(
                    event.data['_updated'], "%a, %d %b %Y %H:%M:%S GMT"
                )
                local_time = gmt_time.replace(
                    tzinfo=datetime.timezone.utc) \
                    .astimezone(tz=None) \
                    .strftime("%a, %d %b %Y %H:%M:%S %Z")

                # Define message
                if service:
                    message = "%s(%s) [%s]: %s - %s" % (
                        service, host, state, output, local_time
                    )
                else:
                    message = "%s [%s]: %s - %s" % (host, state, output, local_time)

                notifications_to_send.append(
                    {'event_type': state, 'message': message}
                )

                self.old_notifications.append(event.item_id)

                return notifications_to_send

        return []


# Creating "data_manager" variable.
data_manager = DataManager()
