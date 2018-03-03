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
    Live Synthesis
    ++++++++++++++
    Live Synthesis manage creation of livesynthesis item for backend ``livesynthesis`` endpoint
"""


from logging import getLogger

from alignak_app.items.item import Item

logger = getLogger(__name__)


class LiveSynthesis(Item):
    """
        Class who create livesynthesis item
    """

    def __init__(self):
        super(LiveSynthesis, self).__init__()
        self.item_type = 'livesynthesis'

    @staticmethod
    def get_request_model():
        """
        Return the request model for livesynthesis requests

        :return: request model for livesynthesis endpoint
        :rtype: dict
        """

        request = {
            'endpoint': 'livesynthesis',
            'params': None,
            'projection': None
        }

        return request

    @staticmethod
    def get_synthesis_count_model():
        """
        Return the synthesis count model

        :return: synthesis count model
        :rtype: dict
        """

        synthesis_count_model = {
            'hosts': {
                'up': 0,
                'down': 0,
                'unreachable': 0,
                'acknowledge': 0,
                'downtime': 0,
                'not_monitored': 0
            },
            'services': {
                'ok': 0,
                'critical': 0,
                'unknown': 0,
                'warning': 0,
                'unreachable': 0,
                'acknowledge': 0,
                'downtime': 0,
                'not_monitored': 0
            }
        }

        return synthesis_count_model
