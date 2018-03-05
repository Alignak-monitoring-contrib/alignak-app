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


import unittest2

from alignak_app.utils.time import get_time_diff_since_last_timestamp


class TestTime(unittest2.TestCase):
    """
        This file test the Time funtions
    """

    def test_get_time_diff_since_last_timestamp(self):
        """Get Time Diff since Last Timestamp"""

        under_test = get_time_diff_since_last_timestamp(1509134069)

        self.assertIsInstance(under_test, str)
        self.assertTrue('ago' in under_test)

        under_test = get_time_diff_since_last_timestamp(float())

        self.assertIsInstance(under_test, str)
        self.assertEqual('<span style="color: red;">Not yet checked!</span>', under_test)