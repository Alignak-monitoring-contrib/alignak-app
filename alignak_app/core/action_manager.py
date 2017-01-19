#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016:
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
    Action Manager manage actions requests
"""

from logging import getLogger


logger = getLogger(__name__)

ACK = 'actionacknowledge'
DOWNTIME = 'actiondowntime'


class ActionManager(object):
    """
        Class who check items to see if actions are done
    """

    def __init__(self, app_backend):
        self.app_backend = app_backend
        self.acks_to_check = []
        self.downtimes_to_check = []

    def check_items(self):
        """
        Check items to see if actions are done

        :return: dict of ACK and DOWNTIME who are done
        :rtype: dict
        """

        done_actions = {
            ACK: [],
            DOWNTIME: []
        }

        # Check acknowledges
        if self.acks_to_check:
            for host in self.acks_to_check:
                cur_host = self.app_backend.get_host(host)
                if cur_host['ls_acknowledged']:
                    self.acks_to_check.remove(host)
                    done_actions[ACK].append(host)

        # Check downtimes scheduled
        if self.downtimes_to_check:
            for host in self.downtimes_to_check:
                cur_host = self.app_backend.get_host(host)
                if cur_host['ls_downtimed']:
                    self.downtimes_to_check.remove(host)
                    done_actions[DOWNTIME].append(host)

        return done_actions

    def add_item(self, item, endpoint):
        """
        Add item in ActionManager

        :param item: item to add
        :type item: TODO
        :param endpoint: endpoint to check
        :type endpoint: str

        """

        if ACK in endpoint:
            self.acks_to_check.append(item)
            logger.info('Begin to check %s...', item)
        elif DOWNTIME in endpoint:
            self.downtimes_to_check.append(item)
            logger.info('Begin to check %s...', item)
        else:
            logger.error('Endpoint %s is not valid. Expect: %s or %s', endpoint, ACK, DOWNTIME)
