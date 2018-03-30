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
    Data Manager
    ++++++++++++
    DataManager manage alignak data provided by
    :class:`Client <alignak_app.backend.backend.BackendClient>`.

    * ``database`` fied contains all data collected by App
    * ``db_is_ready`` fied says to App if database has been filled or not (needed on start)
    * ``old_notifications`` fied store old notifications from backend to avoid sending them again

"""

from logging import getLogger

from alignak_app.utils.time import get_local_datetime_from_date
from alignak_app.items.livesynthesis import LiveSynthesis

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
            'realm': [],
            'timeperiod': [],
            'problems': [],
        }
        self.db_is_ready = {
            'livesynthesis': False,
            'alignakdaemon': False,
            'host': False,
            'user': False,
            'realm': False,
            'timeperiod': False,
            'problems': {'CRITICAL': False, 'WARNING': False, 'UNKNOWN': False},
        }
        self.old_notifications = []
        self.ready = False

    def is_ready(self):
        """
        Check if DataManager is filled and ready

        :return: if ready or current status
        :rtype: str
        """

        for db_name in self.db_is_ready:
            if db_name not in 'problems':
                if self.db_is_ready[db_name]:
                    pass
                else:
                    return _('Collecting %s...') % db_name
            else:
                for problem in self.db_is_ready['problems']:
                    if self.db_is_ready['problems'][problem]:
                        pass
                    else:
                        return _('Collecting %s...') % db_name

        self.ready = True
        return _('READY')

        # return cur_collected

    def update_database(self, item_type, items_list):
        """
        Update an item type in database

        :param item_type: type of item to update
        :type item_type: str
        :param items_list: list of items for the wanted type
        :type items_list: list | dict
        """

        logger.info("Update database[%s]...", item_type)

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
        :rtype: alignak_app.items.item.*
        """

        logger.debug('Get item in database[%s]: key=%s, value=%s', item_type, key, value)

        items = self.database[item_type]

        if value:
            wanted_item = next((item for item in items if item.data[key] == value), None)
            return wanted_item

        wanted_item = next((item for item in items if item.item_id == key), None)

        if not wanted_item:
            wanted_item = next((item for item in items if item.name == key), None)

        return wanted_item

    def remove_item(self, item_type, key, value=None):
        """
        Remove the wanted item in "database[item_type]" who contain the "value" or "key"

        :param item_type: type of wanted item
        :type item_type: str
        :param key: key contained in item
        :type key: str
        :param value: value of the key if needed
        :type value: str
        """

        items = self.database[item_type]

        if value:
            wanted_item = next((item for item in items if item.data[key] == value), None)
        else:
            wanted_item = next((item for item in items if item.item_id == key), None)

        if not wanted_item:
            wanted_item = next((item for item in items if item.name == key), None)

        if not wanted_item:
            logger.error(
                'Can\'t delete item in database[%s]: key=%s, value=%s', item_type, key, value
            )
        else:
            try:
                self.database[item_type].remove(wanted_item)
                logger.info('Remove item in database[%s]: key=%s, value=%s', item_type, key, value)
            except ValueError:
                pass

    def update_item_data(self, item_type, item_id, data):
        """
        Update a single item in database

        :param item_type: type of item (host, service, ...)
        :type data: str
        :param item_id: '_id' of item to update
        :type item_id: str
        :param data: the data to be updated
        :type data: dict
        """

        logger.debug('Update item data in database[%s]:', item_type)
        logger.debug('\t_id: %s', item_id)
        logger.debug('\tdata: %s', data)

        for item in self.database[item_type]:
            if item.item_id == item_id:
                if 'history' in item_type:
                    item.data = data
                else:
                    for key in data:
                        item.data[key] = data[key]

    def get_realm_name(self, realm):
        """
        Return the realm name or alias

        :param realm: wanted realm ``_id``
        :type realm: str
        :return: the wanted realm alias or name if available
        :rtype: str
        """

        if self.database['realm']:
            wanted_realm = self.get_item('realm', realm)

            if wanted_realm:
                return wanted_realm.get_display_name()

        return 'n/a'

    def get_period_name(self, period):
        """
        Return the period name or alias

        :param period: wanted period ``_id``
        :type period: str
        :return: the wanted realm alias or name if available
        :rtype: str
        """

        if self.database['timeperiod']:
            wanted_period = self.get_item('timeperiod', period)

            if wanted_period:
                return wanted_period.get_display_name()

        return 'n/a'

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

                if 'hosts_not_monitored' in realm:
                    synthesis_count['hosts']['not_monitored'] += realm['hosts_not_monitored']

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

                if 'services_not_monitored' in realm:
                    synthesis_count['services']['not_monitored'] += realm['services_not_monitored']

        return synthesis_count

    def get_all_hostnames(self):
        """
        Collect and return all names of all hosts

        :return: all names of all hosts
        :rtype: list
        """

        host_names = []
        for host in self.database['host']:
            host_names.append(host.name)

        logger.debug('List of hosts in database: %s', host_names)

        return host_names

    def get_host_services(self, host_id):
        """
        Return services corresponding to host ID

        :param host_id: '_id' of host
        :type host_id: str
        :return: services corresponding to host ID
        :rtype: list
        """

        host_services = list(
            service for service in self.database['service'] if service.data['host'] == host_id
        )

        return host_services

    def get_host_with_services(self, host_field):
        """
        Returns the desired host and all its services

        :param host_field: field of wanted host: host_id | name
        :type host_field: str
        :return: dict with host data and its associated services
        :rtype: dict
        """

        host = self.get_item('host', host_field)

        services_host = self.get_host_services(host.item_id)

        host_data = {
            'host': host,
            'services': services_host
        }

        return host_data

    def get_events(self):
        """
        Get the last events

        :return: events formated for App to send
        :rtype: list
        """

        events = self.database['notifications']
        logger.debug('Notifications found: %s', str(events))

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
                local_timestamp = get_local_datetime_from_date(event.data['_updated'])
                local_time = local_timestamp.strftime("%a, %d %b %Y %H:%M:%S %Z")

                # Define message
                if service:
                    message = "%s(%s) [%s]: %s - %s" % (
                        service, host, state, output, local_time
                    )
                else:
                    message = "%s [%s]: %s - %s" % (host, state, output, local_time)

                notifications_to_send.append(
                    {'event_type': state, 'message': message, 'host': event.data['host']}
                )

                self.old_notifications.append(event.item_id)

        return notifications_to_send

    def get_items_and_problems(self):
        """
        Return total of items and problems

        :return: dict of problem and total number for each item
        :rtype: dict
        """

        livesynthesis = self.database['livesynthesis']

        hosts_total = 0
        hosts_problems = 0
        hosts_not_monitored = 0
        services_total = 0
        services_problems = 0
        services_not_monitored = 0
        for synth in livesynthesis:
            hosts_total += synth.data['hosts_total']
            hosts_problems += synth.data['hosts_down_soft']
            hosts_problems += synth.data['hosts_down_hard']
            hosts_problems += synth.data['hosts_unreachable_soft']
            hosts_problems += synth.data['hosts_unreachable_hard']
            if 'hosts_not_monitored' in synth.data:
                hosts_not_monitored += synth.data['hosts_not_monitored']

            services_total += synth.data['services_total']
            services_problems += synth.data['services_critical_soft']
            services_problems += synth.data['services_critical_hard']
            services_problems += synth.data['services_warning_soft']
            services_problems += synth.data['services_warning_hard']
            if 'services_not_monitored' in synth.data:
                services_not_monitored += synth.data['services_not_monitored']

        hosts_total = hosts_total - hosts_not_monitored
        services_total = services_total - services_not_monitored
        items_and_problems = {
            'host': {
                'problem': hosts_problems,
                'total': hosts_total
            },
            'service': {
                'problem': services_problems,
                'total': services_total
            },
            'problem': {
                'problem': hosts_problems + services_problems,
                'total': hosts_total + services_total
            }
        }

        logger.debug("Collected problems for livestate: [%s]", items_and_problems)

        return items_and_problems

    def update_problems(self):
        """
        Update hosts and services in "problems" database

        """

        # Update if new hosts are in problem.
        for item in self.database['host']:
            item_in_problem = self.get_item('problems', item.item_id)
            if not item_in_problem and self.is_problem(item.item_type, item.data):
                # Add item to problems
                self.database['problems'].append(item)
            elif item_in_problem and not self.is_problem(item.item_type, item.data):
                # Remove item from problems
                self.database['problems'].remove(item_in_problem)
            elif item_in_problem and self.is_problem(item.item_type, item.data):
                # Update item in problem
                item_in_problem.data = item.data
            else:
                pass

        # Update if new services are in problem.
        for item in self.database['service']:
            item_in_problem = self.get_item('problems', item.item_id)
            if not item_in_problem and self.is_problem(item.item_type, item.data):
                # Add item to problems
                self.database['problems'].append(item)
            elif item_in_problem and not self.is_problem(item.item_type, item.data):
                # Remove item from problems
                self.database['problems'].remove(item_in_problem)
            elif item_in_problem and self.is_problem(item.item_type, item.data):
                # Update item in problem
                item_in_problem.data = item.data
            else:
                pass

    def get_problems(self):
        """
        Update and return items who are in problem: hosts and services

        :return: dict of items in problem, and number for each type of item
        :rtype: dict
        """

        self.update_problems()

        hosts_nb = 0
        services_nb = 0
        problems = self.database['problems']

        # Count problems
        for item in problems:
            if 'service' in item.item_type:
                services_nb += 1
            else:
                hosts_nb += 1

        problems = sorted(problems, key=lambda x: x.data['ls_state'], reverse=True)
        problems = sorted(problems, key=lambda x: x.item_type)

        problems_data = {
            'hosts_nb': hosts_nb,
            'services_nb': services_nb,
            'problems': problems
        }

        logger.debug('Host problems found   : %s', problems_data['hosts_nb'])
        logger.debug('Service problems found: %s', problems_data['services_nb'])

        return problems_data

    @staticmethod
    def is_problem(item_type, backend_item):
        """
        Return True if backend_item is a problem, else return false

        :param item_type: type of item: "host" or "service"
        :type item_type: str
        :param backend_item: item of backend
        :type backend_item: dict
        :return: if item is a problem or not
        :rtype: bool
        """

        if 'service' in item_type:
            if backend_item['ls_state'] in ['CRITICAL', 'WARNING', 'UNKNOWN'] and \
                    not backend_item['ls_acknowledged'] and not backend_item['ls_downtimed']:
                return True
        else:
            if backend_item['ls_state'] in ['DOWN', 'UNREACHABLE'] and \
                    not backend_item['ls_acknowledged'] and not backend_item['ls_downtimed']:
                return True

        return False


# Creation of "data_manager" object
data_manager = DataManager()
