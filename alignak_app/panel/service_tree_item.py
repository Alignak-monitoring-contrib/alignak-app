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
    Service QTreeWidgetItem subclass to store Service item data
"""

from logging import getLogger

from alignak_app.core.utils import get_image_path
from alignak_app.models.item_model import get_icon_item

from PyQt5.Qt import QIcon, QTreeWidgetItem  # pylint: disable=no-name-in-module

logger = getLogger(__name__)


class ServicesTreeItem(QTreeWidgetItem):  # pylint: disable=too-few-public-methods
    """
        Class who create QTreeWidgetItem with service data
    """

    def __init__(self, parent=None):
        super(ServicesTreeItem, self).__init__(parent)
        self.service_item = None
        self.service_id = None

    def initialize(self, service_item):
        """
        Initialize the QTreeWidgetItem

        :param service_item: service item with its data
        :type service_item: alignak_app.models.item_service.Service
        """

        self.service_item = service_item
        self.service_id = service_item.item_id
        self.setText(0, self.service_item.name)

        icon_name = get_icon_item(
            'service',
            service_item.data['ls_state'],
            service_item.data['ls_acknowledged'],
            service_item.data['ls_downtimed']
        )

        self.setIcon(0, QIcon(get_image_path(icon_name)))
