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
    Event
    +++++
    Event manage creation of event item (Notifications collected from ``history`` endpoint)
"""

import datetime
import json
import locale
import sys

from logging import getLogger

from alignak_app.utils.config import settings

from alignak_app.items.item import Item

logger = getLogger(__name__)


class Event(Item):
    """
        Class who create an event item
    """

    def __init__(self):
        super(Event, self).__init__()
        self.item_type = 'notification'

    @staticmethod
    def get_request_model():
        """
        Return the request model for notification requests

        :return: request model for history endpoint (only for notifications)
        :rtype: dict
        """

        notification_projection = {
            'message', '_updated', 'host'
        }

        # Backend use time format in "en_US", so switch if needed
        if "en_US" not in locale.getlocale(locale.LC_TIME) and 'win32' not in sys.platform:
            locale.setlocale(locale.LC_TIME, "en_US.utf-8")
            logger.debug(
                "App set locale to %s for converting date", locale.getlocale(locale.LC_TIME)
            )

        # Define time for the last X minutes define in config file for events
        notif_elapsed = int(settings.get_config('Alignak-app', 'notification_elapsed'))
        time_interval = (datetime.datetime.utcnow() - datetime.timedelta(minutes=notif_elapsed)) \
            .strftime("%a, %d %b %Y %H:%M:%S GMT")

        request_model = {
            'endpoint': 'history',
            'params': {
                'where': json.dumps({
                    'type': 'monitoring.notification',
                    '_updated': {"$gte": time_interval},
                }),
                'sort': '-_updated'
            },
            'projection': notification_projection
        }

        return request_model
