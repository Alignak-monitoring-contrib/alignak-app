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

import unittest2
import sys

from alignak_app.widgets.banner import BannerManager


from PyQt5.QtWidgets import QApplication


class TestBanner(unittest2.TestCase):
    """
        This file test methods of BannerManager class.
    """

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""

        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_banner_manager_creation(self):
        """BannerManager creation"""

        under_test = BannerManager()

        self.assertFalse(under_test.banners)
        self.assertFalse(under_test.banners_to_send)
        self.assertIsNone(under_test.timer)

        under_test.start()
        self.assertIsNotNone(under_test.timer)

        under_test.timer.stop()

    def test_banner_manager_add_banners(self):
        """BannerManager Add Banners"""

        under_test = BannerManager()

        self.assertFalse(under_test.banners)
        self.assertFalse(under_test.banners_to_send)

        under_test.add_banner('OK', 'Test message')

        self.assertFalse(under_test.banners)
        self.assertTrue(under_test.banners_to_send)

        under_test.add_banner('WARN', 'Test message')
        under_test.add_banner('ALERT', 'Test message')

        self.assertTrue(len(under_test.banners_to_send) == 3)

    def test_banner_manager_remove_banners(self):
        """BannerManager Send and Remove Banners"""

        under_test = BannerManager()
        under_test.start()

        under_test.add_banner('OK', 'Test message')

        # Banner is not send and not visible
        self.assertFalse(under_test.banners)
        self.assertTrue(under_test.banners_to_send)

        under_test.check_banners()

        # Banner is send and visible
        self.assertTrue(under_test.banners)
        self.assertFalse(under_test.banners_to_send)

        banner = under_test.banners[0]

        under_test.remove_banner(banner)

        # There is no banner left
        self.assertFalse(under_test.banners)
        self.assertFalse(under_test.banners_to_send)
