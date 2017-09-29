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
        self.database = {
            'history': [],
            'notifications': [],
            'livesynthesis': [],
            'alignakdaemon': [],
            'host': [],
            'service': [],
            'user': [],
        }

    def update_item_database(self, item_type, items_list):
        """
        TODO
        :param item_type:
        :param items_list:
        :return:
        """

        self.database[item_type] = items_list

    def get_item(self, item_type, key, value):
        """
        TODO
        :param item_type:
        :param key:
        :param value:
        :return:
        """

        items = self.database[item_type]

        for item in items:
            if item.data[key] == value:
                return item


# Creating "data_manager" variable.
data_manager = DataManager()
