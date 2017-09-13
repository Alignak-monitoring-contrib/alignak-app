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
    Service widget item is a QListWidgetItem who display service in HostSynthesis
"""


from logging import getLogger

from alignak_app.core.utils import get_image_path

from PyQt5.Qt import QListWidgetItem, QIcon  # pylint: disable=no-name-in-module


logger = getLogger(__name__)


class ServiceListWidgetItem(QListWidgetItem):
    """
        Class who create the QListWidgetItem dedicated to services
    """

    def __init__(self, parent=None):
        super(ServiceListWidgetItem, self).__init__(parent)
        self.aggregation = ''
        self.state = ''

    def initialize(self, service):
        """
        TODO
        :return:
        """

        self.aggregation = service['aggregation']
        self.define_state_name(service)

        if not service['aggregation']:
            service['aggregation'] = 'Global'

        self.setText(
            '%s is %s' % (
                self.get_service_name(service).capitalize(),
                service['ls_state'],
            )
        )
        self.setToolTip(self.get_service_tooltip(service))

        if service['ls_acknowledged']:
            img = get_image_path('services_acknowledge')
        elif service['ls_downtimed']:
            img = get_image_path('services_downtime')
        else:
            img = get_image_path('services_%s' % service['ls_state'])
        self.setIcon(QIcon(img))

    def define_state_name(self, service):
        """
        TODO
        :param service:
        :return:
        """

        if service['ls_acknowledged'] and not service['ls_downtimed']:
            self.state = 'ACKNOWLEDGE'
        elif service['ls_downtimed']:
            self.state = 'DOWNTIME'
        else:
            self.state = service['ls_state']

    def get_service_tooltip(self, service):
        """
        TODO
        :param service:
        :return:
        """

        if service['ls_acknowledged'] and not service['ls_downtimed']:
            tooltip = '%s is %s and acknowledged !' % (
                self.get_service_name(service).capitalize(),
                service['ls_state']
            )
        elif service['ls_downtimed'] and not service['ls_acknowledged']:
            tooltip = '%s is %s and downtimed !' % (
                self.get_service_name(service).capitalize(),
                service['ls_state']
            )
        elif service['ls_acknowledged'] and service['ls_downtimed']:
            tooltip = '%s is %s acknowledged. A downtimed is scheduled !' % (
                self.get_service_name(service).capitalize(),
                service['ls_state']
            )
        else:
            tooltip = '%s is %s' % (
                self.get_service_name(service).capitalize(),
                service['ls_state']
            )

        return tooltip

    @staticmethod
    def get_service_name(service):
        """

        :param service:
        :return:
        """

        if service['display_name'] != '':
            service_name = service['display_name']
        elif service['alias'] != '':
            service_name = service['alias']
        else:
            service_name = service['name']

        return service_name
