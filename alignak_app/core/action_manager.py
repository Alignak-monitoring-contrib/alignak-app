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
    Action Manager manage actions requests
"""

from logging import getLogger


logger = getLogger(__name__)

ACK = 'actionacknowledge'
DOWNTIME = 'actiondowntime'
PROCESS = 'processed'


class ActionManager(object):
    """
        Class who check items to see if actions are done
    """

    def __init__(self, app_backend):
        self.app_backend = app_backend
        self.acks_to_check = {
            'hosts': [],
            'services': []
        }
        self.downtimes_to_check = {
            'hosts': [],
            'services': []
        }
        self.processed_to_check = []
        self.acknowledged = []
        self.downtimed = []

    def check_items(self):  # pragma: no cover, this is not testable
        """
        Check items to see if actions are done

        :return: dict of ACK, DOWNTIME and PROCESSED who are done
        :rtype: dict
        """

        done_actions = {
            ACK: {
                'hosts': [],
                'services': []
            },
            DOWNTIME: {
                'hosts': [],
                'services': []
            },
            PROCESS: []
        }

        # Check hosts acknowledges
        if self.acks_to_check['hosts']:
            logger.debug('Hosts ACK: %s', self.acks_to_check['hosts'])
            for item in self.acks_to_check['hosts']:
                # Get host
                host = self.app_backend.get_host('_id', item['host_id'], ['ls_acknowledged'])
                if host['ls_acknowledged']:
                    self.acks_to_check['hosts'].remove(item)
                    done_actions[ACK]['hosts'].append(item)
        # Check services acknowledges
        if self.acks_to_check['services']:
            logger.debug('Services ACK: %s', self.acks_to_check['services'])
            for item in self.acks_to_check['services']:
                # Get service
                service = self.app_backend.get_service(
                    item['host_id'],
                    item['service_id'],
                    ['ls_acknowledged']
                )
                if service['ls_acknowledged']:
                    self.acks_to_check['services'].remove(item)
                    done_actions[ACK]['services'].append(item)

        # Check host downtimes
        if self.downtimes_to_check['hosts']:
            logger.debug('Hosts DOWN: %s', self.downtimes_to_check['hosts'])
            for item in self.downtimes_to_check['hosts']:
                # Get host
                host = self.app_backend.get_host('_id', item['host_id'], ['ls_downtimed'])
                if host['ls_downtimed']:
                    self.downtimes_to_check['hosts'].remove(item)
                    done_actions[DOWNTIME]['hosts'].append(item)
        # Check services downtimes
        if self.downtimes_to_check['services']:
            logger.debug('Services DOWN: %s', self.downtimes_to_check['services'])
            for item in self.downtimes_to_check['services']:
                # Get service
                service = self.app_backend.get_service(
                    item['host_id'],
                    item['service_id'],
                    ['ls_downtimed']
                )
                if service['ls_downtimed']:
                    self.downtimes_to_check['services'].remove(item)
                    done_actions[DOWNTIME]['services'].append(item)

        # Check process
        if self.processed_to_check:
            logger.debug('Item PROCESS: %s', self.processed_to_check)
            for item in self.processed_to_check:
                resp = self.app_backend.backend.get(item['post']['_links']['self']['href'])
                if resp[PROCESS]:
                    self.processed_to_check.remove(item)
                    done_actions[PROCESS].append(item)

        return done_actions

    def add_item(self, item):
        """
        Add item in ActionManager

        :param item: item to add
            - for actions
            item = {
                'action': ACK, DOWNTIME
                'host_id': id of host,
                'service_id': id of service if needed
            }
            - for processed
            item = {
                'action': PROCESS
                'name': name of an item (host or service)
                'post': href of action POST
            }
        :type item: dict
        """

        if item:
            logger.debug('Add item %s', item)
            if ACK in item['action']:
                if not item['service_id']:
                    self.acks_to_check['hosts'].append(item)
                else:
                    self.acks_to_check['services'].append(item)
            elif DOWNTIME in item['action']:
                if not item['service_id']:
                    self.downtimes_to_check['hosts'].append(item)
                else:
                    self.downtimes_to_check['services'].append(item)
            elif PROCESS in item['action']:
                self.processed_to_check.append(item)
            else:
                logger.error('Endpoint %s is not valid', item['action'])
        else:
            logger.error('Item is %s', item)
