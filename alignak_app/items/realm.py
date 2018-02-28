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
    Realm
    +++++
    Realm manage creation of realm item for backend ``realm`` endpoint
"""


from logging import getLogger

from alignak_app.items.item import Item

logger = getLogger(__name__)


class Realm(Item):
    """
        Class who create a realm item
    """

    def __init__(self):
        super(Realm, self).__init__()
        self.item_type = 'realm'

    @staticmethod
    def get_request_model():
        """
        Return the request model for realm requests

        :return: request model for realm endpoint
        :rtype: dict
        """

        realms_projection = [
            'name', 'alias'
        ]

        request_model = {
            'endpoint': 'realm',
            'params': None,
            'projection': realms_projection
        }

        return request_model

    def get_display_name(self):
        """
        Return alias or name if available

        :return: name or alias
        :rtype: str
        """

        if 'alias' in self.data:
            return self.data['alias'].title()

        return self.data['name'].title()
