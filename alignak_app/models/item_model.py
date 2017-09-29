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
    TODO
"""


from logging import getLogger


logger = getLogger(__name__)


class ItemModel(object):
    """
        TODO
    """

    def __init__(self):
        self.item_type = 'model'
        self.item_id = ''
        self.name = ''
        self.data = None

    def create(self, _id, data, name=None):
        """
        TODO
        :param _id:
        :param data:
        :param name:

        """

        self.item_id = _id
        self.data = data

        if name:
            self.name = data['name']

    def get_data(self, key):
        """
        TODO
        :param key:
        :return:
        """

        return self.data[key]

    def update_data(self, key, new_value):
        """
        TODO
        :param key:
        :param new_value:
        :return:
        """

        self.data[key] = new_value
