#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2
import configparser as cfg

from alignak_app.application import AlignakApp
from alignak_app.alignak_data import AlignakData

class TestApplication(unittest2.TestCase):
    """
        This file test methods of AlignakApp class.
    """

    def test_initialization(self):
        under_test = AlignakApp()

        # Test initialization of Class and assert items are created.
        self.assertIsNone(under_test.Config)
        self.assertIsNone(under_test.backend_data)
        self.assertIsNotNone(under_test.up_item)
        self.assertIsNotNone(under_test.down_item)
        self.assertIsNotNone(under_test.quit_item)

    def test_alignak_config(self):
        # Assert Config is None before read
        under_test = AlignakApp()
        self.assertIsNone(under_test.Config)

        # Assert Config is NOT None after read
        under_test.read_configuration()
        self.assertIsNotNone(under_test.Config)

    def test_get_state(self):
        under_test = AlignakApp()

        Config = cfg.ConfigParser()
        Config.read('./etc/settings.cfg')
        under_test.Config = Config

        under_test.backend_data = AlignakData()
        under_test.backend_data.log_to_backend(under_test.Config)

        # UP and DOWN must be Integer and positive
        UP, DOWN = under_test.get_state()

        self.assertIsInstance(UP, int)
        self.assertIsInstance(DOWN, int)
        self.assertGreater(UP, -1)
        self.assertGreater(DOWN, -1)



