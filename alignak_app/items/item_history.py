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
    ItemHistory manage creation of history item
"""


from logging import getLogger

from alignak_app.items.item_model import ItemModel


logger = getLogger(__name__)


class History(ItemModel):
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