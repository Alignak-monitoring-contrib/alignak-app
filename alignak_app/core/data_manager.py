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
    DataManager manage and store the Alignak data provided by BackendQthread
"""

from logging import getLogger


logger = getLogger(__name__)


class DataManager(object):
    """
        Class who store Alignak data
    """

    def __init__(self):
        self.database = self.get_database_model()
        self.history_database = self.get_history_database_model()

    @staticmethod
    def get_database_model():
        """
        Return database model

        :return: database model
        :rtype: dict
        """

        return {
            'host': {},
            'service': {},
            'alignakdaemon': {},
            'livesynthesis': {},
            'user': {},
            'history': {}
        }

    @staticmethod
    def get_history_database_model():
        """
        Return history database model

        :return: history database model
        :rtype: dict
        """

        return {
            'history': [],
            'notification': []
        }

    def update_item_type(self, item_type, data):
        """
        Update the wanted item type with data

        :param item_type: type of item define in database model
        :type item_type: str
        :param data: data to update
        :type data: dict
        """

        logger.info('Update [%s] database...', item_type)

        for d in data:
            self.database[item_type][d['_id']] = d

    def get_item(self, item_type, item_id):
        """
        Get the wanted item by "_id"

        :param item_type: type of item define in database model
        :type item_type: str
        :param item_id: "_id" of wanted item
        :type item_id: str
        :return: the wanted item data
        :rtype: dict
        """

        logger.debug("Get item %s in %s", item_id, item_type)

        if item_id in self.database[item_type]:
            return self.database[item_type][item_id]

    def update_history_item(self, history_type, data):
        """
        TODO
        :param history_type:
        :param data:
        :return:
        """

        if data != self.history_database[history_type]:
            self.history_database[history_type] = data

    def get_synthesis_count(self):
        """
        Get on "synthesis" endpoint and return the states of hosts and services

        :return: states of hosts and services.
        :rtype: dict
        """

        live_synthesis = {
            'hosts': {
                'up': 0,
                'down': 0,
                'unreachable': 0,
                'acknowledge': 0,
                'downtime': 0
            },
            'services': {
                'ok': 0,
                'critical': 0,
                'unknown': 0,
                'warning': 0,
                'unreachable': 0,
                'acknowledge': 0,
                'downtime': 0
            }
        }

        if self.database['livesynthesis']:
            for realm in self.database['livesynthesis']:
                realm_item = self.get_item('livesynthesis', realm)
                live_synthesis['hosts']['up'] += realm_item['hosts_up_soft']
                live_synthesis['hosts']['up'] += realm_item['hosts_up_hard']

                live_synthesis['hosts']['unreachable'] += realm_item['hosts_unreachable_soft']
                live_synthesis['hosts']['unreachable'] += realm_item['hosts_unreachable_hard']

                live_synthesis['hosts']['down'] += realm_item['hosts_down_soft']
                live_synthesis['hosts']['down'] += realm_item['hosts_down_hard']

                live_synthesis['hosts']['acknowledge'] += realm_item['hosts_acknowledged']
                live_synthesis['hosts']['downtime'] += realm_item['hosts_in_downtime']

                live_synthesis['services']['ok'] += realm_item['services_ok_soft']
                live_synthesis['services']['ok'] += realm_item['services_ok_hard']

                live_synthesis['services']['warning'] += realm_item['services_warning_soft']
                live_synthesis['services']['warning'] += realm_item['services_warning_hard']

                live_synthesis['services']['critical'] += realm_item['services_critical_soft']
                live_synthesis['services']['critical'] += realm_item['services_critical_hard']

                live_synthesis['services']['unknown'] += realm_item['services_unknown_soft']
                live_synthesis['services']['unknown'] += realm_item['services_unknown_hard']

                live_synthesis['services']['unreachable'] += realm_item['services_unreachable_soft']
                live_synthesis['services']['unreachable'] += realm_item['services_unreachable_hard']

                live_synthesis['services']['acknowledge'] += realm_item['services_acknowledged']
                live_synthesis['services']['downtime'] += realm_item['services_in_downtime']

        return live_synthesis


# Creating "data_manager" variable.
data_manager = DataManager()
