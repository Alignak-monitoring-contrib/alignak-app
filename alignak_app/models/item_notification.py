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


import sys
import locale
import datetime
import json

from logging import getLogger

from alignak_app.models.item_model import ItemModel
from alignak_app.core.data_manager import data_manager


logger = getLogger(__name__)


class Notification(ItemModel):
    """
        TODO
    """

    def __init__(self):
        super(Notification, self).__init__()
        self.item_type = 'notification'

    @staticmethod
    def get_request_model():
        """
        TODO
        :return:
        """

        notification_projection = {
            'message', '_updated'
        }

        # Backend use time format in "en_US", so switch if needed
        if "en_US" not in locale.getlocale(locale.LC_TIME) and 'win32' not in sys.platform:
            locale.setlocale(locale.LC_TIME, "en_US.utf-8")
            logger.warning("App set locale to %s ", locale.getlocale(locale.LC_TIME))

        # Define time for the last 30 minutes for notifications
        time_interval = (datetime.datetime.utcnow() - datetime.timedelta(minutes=30)) \
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
