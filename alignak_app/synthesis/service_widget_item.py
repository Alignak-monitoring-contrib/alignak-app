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
        Inititalize QListWidgetItem

        :param service: Service item with its data
        :type service: alignak_app.models.item_model.ItemModel
        """

        self.aggregation = service.data['aggregation']
        self.define_state_name(service)

        if not service.data['aggregation']:
            service.data['aggregation'] = 'Global'

        self.setText(
            _('%s is %s') % (
                self.get_service_name(service).capitalize(),
                service.data['ls_state'],
            )
        )
        self.setToolTip(self.get_service_tooltip(service))

        if service.data['ls_acknowledged']:
            img = get_image_path('services_acknowledge')
        elif service.data['ls_downtimed']:
            img = get_image_path('services_downtime')
        else:
            img = get_image_path('services_%s' % service.data['ls_state'])
        self.setIcon(QIcon(img))

    def define_state_name(self, service):
        """
        Define the state name to display for service

        :param service: service dict data
        :type service: alignak_app.models.item_model.ItemModel
        """

        if service.data['ls_acknowledged'] and not service.data['ls_downtimed']:
            self.state = 'ACKNOWLEDGE'
        elif service.data['ls_downtimed']:
            self.state = 'DOWNTIME'
        else:
            self.state = service.data['ls_state']

    def get_service_tooltip(self, service):
        """
        Define and return service tooltip

        :param service: service dict data
        :type service: alignak_app.models.item_model.ItemModel
        :return: tooltip string
        :rtype: str
        """

        if service.data['ls_acknowledged'] and not service.data['ls_downtimed']:
            tooltip = _('%s is %s and acknowledged !') % (
                self.get_service_name(service).capitalize(),
                service.data['ls_state']
            )
        elif service.data['ls_downtimed'] and not service.data['ls_acknowledged']:
            tooltip = _('%s is %s and downtimed !') % (
                self.get_service_name(service).capitalize(),
                service.data['ls_state']
            )
        elif service.data['ls_acknowledged'] and service.data['ls_downtimed']:
            tooltip = _('%s is %s acknowledged. A downtimed is scheduled !') % (
                self.get_service_name(service).capitalize(),
                service.data['ls_state']
            )
        else:
            tooltip = _('%s is %s') % (
                self.get_service_name(service).capitalize(),
                service.data['ls_state']
            )

        return tooltip

    @staticmethod
    def get_service_name(service):
        """
        Return the service name

        :param service: service dict data
        :type service: alignak_app.models.item_model.ItemModel
        :return: service name
        :rtype: str
        """

        if service.data['display_name'] != '':
            service_name = service.data['display_name']
        elif service.data['alias'] != '':
            service_name = service.data['alias']
        else:
            service_name = service.name

        return service_name
