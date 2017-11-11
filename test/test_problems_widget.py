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

import sys

import unittest2

from PyQt5.Qt import QApplication

from alignak_app.pyqt.panel.widgets.problems import ProblemsQWidget, QWidget


class TestDataManager(unittest2.TestCase):
    """
        This file test the ProblemsQWidget class.
    """

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize(self):
        """Initialize ProblemsQWidget"""

        under_test = ProblemsQWidget()

        self.assertIsNotNone(under_test.layout)
        self.assertTrue(under_test.problem_widget)
        self.assertTrue(under_test.problems_title)
        self.assertTrue(under_test.headers_list)
        self.assertEqual(
            ['Item Type', 'Host', 'Service', 'State', 'Actions', 'Output'],
            under_test.headers_list
        )

        under_test.initialize()

        self.assertIsNotNone(under_test.layout)
        self.assertTrue(under_test.problem_widget)
        self.assertTrue(under_test.problems_title)
        self.assertTrue(under_test.headers_list)
        self.assertEqual(
            ['Item Type', 'Host', 'Service', 'State', 'Actions', 'Output'],
            under_test.headers_list
        )
        self.assertEqual('title', under_test.problems_title.objectName())

    def test_get_problems_widget_title(self):
        """Get problems Widget Title"""

        problems_widget_test = ProblemsQWidget()

        under_test = problems_widget_test.get_problems_widget_title()

        self.assertIsInstance(under_test, QWidget)

