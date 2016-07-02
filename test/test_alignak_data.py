#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest2
import configparser as cfg

from alignak_app.alignak_data import AlignakData, Backend

class TestAlignakData(unittest2.TestCase):
    """
        This file test methods of AlignakData class
    """

    def test_connection(self):
        under_test = AlignakData()

        Config = cfg.ConfigParser()
        Config.read('./etc/settings.cfg')
        for conf in Config:
            print(Config.items(conf))

        under_test.log_to_backend(Config)

        # Compare config url and backend
        self.assertEquals(under_test.backend.url_endpoint_root, Config.get('Backend', 'backend_url'))
        # Test if all is empty
        self.assertFalse(under_test.current_hosts)
        self.assertFalse(under_test.current_services)

    def test_if_hosts_and_services(self):
        under_test = AlignakData()

        Config = cfg.ConfigParser()
        Config.read('./etc/settings.cfg')

        under_test.log_to_backend(Config)

        self.assertTrue(under_test.get_host_state())
        self.assertTrue(under_test.get_service_state())

