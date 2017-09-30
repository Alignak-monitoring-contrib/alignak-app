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

from logging import getLogger


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

    def is_filled(self):
        """
        Check if dtata manager is filled (ready)
        :return:
        """

        filled = False
        if self.database['user'] and self.database['host'] and \
                self.database['service'] and self.database['alignakdaemon'] and \
                self.database['livesynthesis']:
            filled = True

        return filled

    def update_item_database(self, item_type, items_list):
        """
        Update an item type in database

        :param item_type: type of item to update
        :type item_type: str
        :param items_list: list of items for the wanted type
        :type items_list: list | dict
        """

        self.database[item_type] = items_list

    def get_item(self, item_type, key, value=None):
        """
        Return the wanted item for item type who contain the value

        :param item_type:
        :param key:
        :param value:
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


# Creating "data_manager" variable.
data_manager = DataManager()
