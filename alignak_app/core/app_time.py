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
    App Time manage time and date
"""

import time

from logging import getLogger

from datetime import datetime

logger = getLogger(__name__)


def get_time_diff_since_last_timestamp(timestamp):  # pragma: no cover - not testable
    """
    Return the diff between the last time stamp

    :param timestamp: timestamp of the last check
    :type timestamp: float
    :return: time difference formatted
    :rtype: str
    """

    if not timestamp:
        return 'n/a'

    time_delta = int(time.time()) - int(timestamp)

    # If it's now, say it :)
    if time_delta < 3:
        if 0 > time_delta > -4:
            return _('Very soon')
        if time_delta >= 0:
            return _('Just now')

    seconds = int(round(time_delta))
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    months, weeks = divmod(weeks, 4)
    years, months = divmod(months, 12)

    duration = []
    if years > 0:
        duration.append('%dy' % years)
    else:
        if months > 0:
            duration.append('%dM' % months)
        if weeks > 0:
            duration.append('%dw' % weeks)
        if days > 0:
            duration.append('%dd' % days)
        if hours > 0:
            duration.append('%dh' % hours)
        if minutes > 0:
            duration.append('%dm' % minutes)
        if seconds > 0:
            duration.append('%ds' % seconds)

    return ' ' + ' '.join(duration) + ' ago'


def get_date_from_timestamp(timestamp):
    """
    Return date from timestamp
    :param timestamp: timestamp to convert to date
    :type timestamp: int
    :return: corresponding date
    :rtype: str
    """

    if timestamp:
        return datetime.fromtimestamp(timestamp)

    return 'n/a'