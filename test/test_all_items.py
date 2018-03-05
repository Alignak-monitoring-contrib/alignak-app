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

from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.backend.backend import app_backend
from alignak_app.backend.datamanager import data_manager

from alignak_app.items.daemon import Daemon
from alignak_app.items.event import Event
from alignak_app.items.history import History
from alignak_app.items.host import Host
from alignak_app.items.item import *
from alignak_app.items.livesynthesis import LiveSynthesis
from alignak_app.items.service import Service
from alignak_app.items.user import User
from alignak_app.items.realm import Realm


class TestAllItems(unittest2.TestCase):
    """
        This file test methods of ItemModel class objects
    """

    settings.init_config()
    init_localization()
    app_backend.login()

    # Host data test
    host_list = []
    for i in range(0, 10):
        host = Host()
        host.create(
            '_id%d' % i,
            {
                'name': 'host%d' % i,
                'ls_downtimed': True,
                'ls_acknowledged': True,
                'ls_state': 'UNKNOWN',
                'passive_checks_enabled': False,
                'active_checks_enabled': True
            },
            'host%d' % i
        )
        host_list.append(host)

    # Service data test
    service_list = []
    for i in range(0, 10):
        service = Service()
        service.create(
            '_id%d' % i,
            {
                'name': 'service%d' % i,
                'alias': 'Service %d' % i,
                'host': '_id%d' % i,
                'ls_acknowledged': False,
                'ls_downtimed': False,
                'ls_state': 'CRITICAL',
                'aggregation': 'disk',
                '_overall_state_id': 4,
                'passive_checks_enabled': False,
                'active_checks_enabled': True
            },
            'service%d' % i
        )
        service_list.append(service)

    def test_item_model(self):
        """Create ItemModel"""

        under_test = Item()

        under_test.create('_id', {'ls_state': 'DOWN'}, 'name')

        self.assertTrue('_id' == under_test.item_id)
        self.assertTrue('ls_state' in under_test.data)
        self.assertTrue('DOWN' == under_test.data['ls_state'])
        self.assertTrue('name' == under_test.name)

    def test_item_model_get_data(self):
        """Get Data ItemModel"""

        under_test = Item()

        under_test.create('_id', {'ls_state': 'DOWN', 'ls_acknowledged': True}, 'name')

        data_test = under_test.data['ls_state']

        self.assertTrue('DOWN' == data_test)

    def test_item_model_update_data(self):
        """Update Data ItemModel"""

        under_test = Item()

        under_test.create('_id', {'ls_state': 'DOWN', 'ls_acknowledged': True}, 'name')

        under_test.update_data('ls_acknowledged', False)

        data_test = under_test.data['ls_acknowledged']

        self.assertTrue(data_test is False)

    def test_get_icon_name(self):
        """Get Icon Name"""

        under_test = get_icon_name(
            'host', 'UP', acknowledge=False, downtime=False, monitored=1)
        self.assertEqual('hosts_up', under_test)

        under_test = get_icon_name(
            'service', 'WARNING', acknowledge=False, downtime=False, monitored=1)
        self.assertEqual('services_warning', under_test)

        under_test = get_icon_name(
            'host', 'DOWN', acknowledge=True, downtime=False, monitored=1)
        self.assertEqual('acknowledge', under_test)

        under_test = get_icon_name(
            'service', 'UNREACHABLE', acknowledge=True, downtime=True, monitored=2)
        self.assertEqual('downtime', under_test)

        under_test = get_icon_name(
            'host', 'WRONG_STATUS', acknowledge=False, downtime=False, monitored=1)
        self.assertEqual('error', under_test)

        under_test = get_icon_name(
            'host', 'UP', acknowledge=False, downtime=False, monitored=False + False)
        self.assertEqual('hosts_not_monitored', under_test)

    def test_get_icon_name_from_state(self):
        """Get Icon Name from State"""

        under_test = get_icon_name_from_state('host', 'UP')
        self.assertEqual('hosts_up', under_test)

        under_test = get_icon_name_from_state('service', 'CRITICAL')
        self.assertEqual('services_critical', under_test)

        under_test = get_icon_name_from_state('host', 'ACKNOWLEDGE')
        self.assertEqual('acknowledge', under_test)

        under_test = get_icon_name_from_state('service', 'DOWNTIME')
        self.assertEqual('downtime', under_test)

    def test_get_real_host_state_icon(self):
        """Get Real Host State Icon"""

        # Service data test
        services_test = []
        for i in range(0, 5):
            service = Service()
            service.create(
                '_id%d' % i,
                {'name': 'service%d' % i, '_overall_state_id': i},
                'service%d' % i
            )
            services_test.append(service)
            service = Service()
            service.create(
                'other_id2%d' % i,
                {'name': 'other_service2%d' % i, '_overall_state_id': i},
                'other_service%d' % i
            )
            services_test.append(service)

        under_test = get_real_host_state_icon(services_test)
        self.assertEqual('all_services_critical', under_test)

        under_test = get_real_host_state_icon([])
        self.assertEqual('all_services_none', under_test)

    def test_get_host_msg_and_event_type(self):
        """Get Host Message and Event Type"""

        data_manager.update_database('host', self.host_list)
        data_manager.update_database('service', self.service_list)

        host_and_services = data_manager.get_host_with_services('_id1')

        under_test = get_host_msg_and_event_type(host_and_services)

        self.assertEqual(
            'Host1 is UNKNOWN and acknowledged, '
            'some services may be in critical condition or unreachable !',
            under_test['message']
        )
        self.assertEqual(under_test['event_type'], 'DOWN')

    def test_get_request_history_model(self):
        """Get History Request Model"""

        under_test = History.get_request_model()

        self.assertTrue('endpoint' in under_test)
        self.assertEqual('history', under_test['endpoint'])
        self.assertTrue('params' in under_test)
        self.assertTrue('projection' in under_test)

    def test_get_history_icon_name_from_message(self):
        """Get History Icon from State"""

        under_test = History.get_history_icon_name_from_message('UNKNOWN', 'downtime')
        self.assertEqual('downtime', under_test)

        under_test = History.get_history_icon_name_from_message('UP', 'ack')
        self.assertEqual('acknowledge', under_test)

        under_test = History.get_history_icon_name_from_message('UP', 'event_type')
        self.assertEqual('hosts_up', under_test)

        under_test = History.get_history_icon_name_from_message('DOWN', 'event_type')
        self.assertEqual('hosts_down', under_test)

        under_test = History.get_history_icon_name_from_message('UNREACHABLE', 'event_type')
        self.assertEqual('services_unreachable', under_test)

        under_test = History.get_history_icon_name_from_message('OK', 'event_type')
        self.assertEqual('services_ok', under_test)

        under_test = History.get_history_icon_name_from_message('WARNING', 'event_type')
        self.assertEqual('services_warning', under_test)

        under_test = History.get_history_icon_name_from_message('CRITICAL', 'event_type')
        self.assertEqual('services_critical', under_test)

        under_test = History.get_history_icon_name_from_message('UNKNOWN', 'event_type')
        self.assertEqual('services_unknown', under_test)

        under_test = History.get_history_icon_name_from_message('error', 'event_type')
        self.assertEqual('error', under_test)

    def test_get_request_user_model(self):
        """Get User Request Model"""

        under_test = User.get_request_model('')

        self.assertTrue('endpoint' in under_test)
        self.assertEqual('user', under_test['endpoint'])
        self.assertTrue('params' in under_test)
        self.assertTrue('projection' in under_test)

    def test_get_user_role(self):
        """Get User Role"""

        # User case
        user_test = User()
        user_test.create(
            '_id',
            {'is_admin': False, 'can_submit_commands': False, 'back_role_super_admin': False},
            'name'
        )
        under_test = user_test.get_role()
        self.assertEqual('user', under_test)

        # Administrator case
        user_test = User()
        user_test.create(
            '_id',
            {'is_admin': True, 'can_submit_commands': False, 'back_role_super_admin': False},
            'name'
        )
        under_test = user_test.get_role()
        self.assertEqual('administrator', under_test)

        # Power case
        user_test = User()
        user_test.create(
            '_id',
            {'is_admin': False, 'can_submit_commands': True, 'back_role_super_admin': False},
            'name'
        )
        under_test = user_test.get_role()
        self.assertEqual('power', under_test)

    def test_get_request_host_model(self):
        """Get Host Request Model"""

        under_test = Host.get_request_model()

        self.assertTrue('endpoint' in under_test)
        self.assertEqual('host', under_test['endpoint'])
        self.assertTrue('params' in under_test)
        self.assertTrue('projection' in under_test)

    def test_get_request_service_model(self):
        """Get Service Request Model"""

        under_test = Service.get_request_model()

        self.assertTrue('endpoint' in under_test)
        self.assertEqual('service', under_test['endpoint'])
        self.assertTrue('params' in under_test)
        self.assertTrue('projection' in under_test)

    def test_get_request_daemon_model(self):
        """Get Daemon Request Model"""

        under_test = Daemon.get_request_model()

        self.assertTrue('endpoint' in under_test)
        self.assertEqual('alignakdaemon', under_test['endpoint'])
        self.assertTrue('params' in under_test)
        self.assertTrue('projection' in under_test)

    def test_get_daemons_names(self):
        """Get All Daemon Names"""

        daemon_names = [
            'poller',
            'receiver',
            'reactionner',
            'arbiter',
            'scheduler',
            'broker'
        ]

        self.assertEqual(daemon_names, Daemon.get_daemons_names())

    def test_get_request_event_model(self):
        """Get Event Request Model"""

        under_test = Event.get_request_model()

        self.assertTrue('endpoint' in under_test)
        self.assertEqual('history', under_test['endpoint'])
        self.assertTrue('params' in under_test)
        self.assertTrue('projection' in under_test)

    def test_get_request_livesynthesis_model(self):
        """Get LiveSynthesis Request Model"""

        under_test = LiveSynthesis.get_request_model()

        self.assertTrue('endpoint' in under_test)
        self.assertEqual('livesynthesis', under_test['endpoint'])
        self.assertTrue('params' in under_test)
        self.assertTrue('projection' in under_test)

    def get_request_realm_model(self):
        """get Realm Request Model"""

        under_test = Realm.get_request_model()

        self.assertTrue('endpoint' in under_test)
        self.assertEqual('realm', under_test['endpoint'])
        self.assertTrue('params' in under_test)
        self.assertTrue('projection' in under_test)
