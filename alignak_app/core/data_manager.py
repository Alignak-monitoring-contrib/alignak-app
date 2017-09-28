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


class DataManager(object):
    """
        Class who store Alignak data
    """

    def __init__(self):
        self.database = {
            'host': {},
            'service': {}
        }

    def update_item_type(self, item_type, data):
        """
        Update the wanted item type with data

        :param item_type:
        :param data:
        :return:
        """

        for d in data:
            self.database[item_type][d['_id']] = d

    def get_item(self, item_type, item_id):
        """
        Get the wanted item by "_id"

        :param item_type:
        :param item_id:
        :return:
        """

        if item_id in self.database[item_type]:
            return self.database[item_type][item_id]
