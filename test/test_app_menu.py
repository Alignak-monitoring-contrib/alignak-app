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

import unittest2
import configparser as cfg
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from alignak_app.app_menu import AppMenu

class TestAppMenu(unittest2.TestCase):

    def test_initialization(self):
        config = cfg.ConfigParser()
        config.read('./etc/settings.cfg')

        under_test = AppMenu(config)

        self.assertIsNone(under_test.hosts_up_item)
        self.assertIsNone(under_test.hosts_down_item)
        self.assertIsNone(under_test.hosts_unreach_item)
        self.assertIsNone(under_test.services_up_item)
        self.assertIsNone(under_test.services_down_item)
        self.assertIsNone(under_test.services_warning_item)
        self.assertIsNone(under_test.services_unknown_item)
        self.assertIsNotNone(under_test.config)

    def test_build_items(self):
        config = cfg.ConfigParser()
        config.read('./etc/settings.cfg')

        under_test = AppMenu(config)

        under_test.build_items()

        self.assertIsNotNone(under_test.hosts_up_item)
        self.assertIsNotNone(under_test.hosts_down_item)
        self.assertIsNotNone(under_test.hosts_unreach_item)
        self.assertIsNotNone(under_test.services_up_item)
        self.assertIsNotNone(under_test.services_down_item)
        self.assertIsNotNone(under_test.services_warning_item)
        self.assertIsNotNone(under_test.services_unknown_item)

        self.assertIsInstance(under_test.hosts_up_item, Gtk.ImageMenuItem)
        self.assertIsInstance(under_test.services_up_item, Gtk.ImageMenuItem)

    def test_update_menu(self):
        config = cfg.ConfigParser()
        config.read('./etc/settings.cfg')

        under_test = AppMenu(config)

        under_test.build_items()

        hosts_states = {
            'up': 0,
            'down': 0,
            'unreachable': 0
        }
        services_states = {
            'ok': 0,
            'critical': 0,
            'unknown': 0,
            'warning': 0
        }

        under_test.update_hosts_menu(hosts_states, services_states)

        temp_label_host_up = under_test.hosts_up_item.get_label()
        temp_label_host_down = under_test.hosts_down_item.get_label()
        temp_label_host_unreachable = under_test.hosts_unreach_item.get_label()

        temp_label_service_ok = under_test.services_up_item.get_label()
        temp_label_service_warning = under_test.services_warning_item.get_label()
        temp_label_service_critical = under_test.services_down_item.get_label()
        temp_label_service_unknown = under_test.services_unknown_item.get_label()

        hosts_states = {
            'up': 10,
            'down': 10,
            'unreachable': 0
        }

        services_states = {
            'ok': 10,
            'critical': 0,
            'unknown': 0,
            'warning': 10
        }
        under_test.update_hosts_menu(hosts_states, services_states)

        self.assertNotEqual(str(under_test.hosts_up_item.get_label()), str(temp_label_host_up))
        self.assertNotEqual(str(under_test.hosts_down_item.get_label()), str(temp_label_host_down))
        self.assertNotEqual(str(under_test.services_up_item.get_label()), str(temp_label_service_ok))
        self.assertNotEqual(str(under_test.services_warning_item.get_label()), str(temp_label_service_warning))

        self.assertEqual(str(under_test.hosts_unreach_item.get_label()), str(temp_label_host_unreachable))
        self.assertEqual(str(under_test.services_down_item.get_label()), str(temp_label_service_critical))
        self.assertEqual(str(under_test.services_unknown_item.get_label()), str(temp_label_service_unknown))

