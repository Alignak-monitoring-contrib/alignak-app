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

"""
    Action_Factory build actions for TrayIcon.
"""

from logging import getLogger

from alignak_app.core.utils import get_image_path

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QAction  # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QIcon  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QAction  # pylint: disable=import-error
    from PyQt4.QtGui import QIcon  # pylint: disable=import-error


logger = getLogger(__name__)


class ActionFactory(object):
    """
        Create QAction with his icon and content
    """

    def __init__(self):
        self.actions = {}

    def create(self, name, content, parent):
        """
        Create QAction

        """

        q_action = QAction(
            QIcon(get_image_path(name)),
            content,
            parent
        )

        if 'acknowledged' in name and 'Hosts' in content:
            name = 'hosts_' + name
        if 'downtime' in name and 'Hosts' in content:
            name = 'hosts_' + name
        if 'acknowledged' in name and 'Services' in content:
            name = 'services_' + name
        if 'downtime' in name and 'Services' in content:
            name = 'services_' + name
        self.add_action(name, q_action)

    def add_action(self, name, q_action):
        """
        Add action in actions dict for acces thereafter

        :param name: name of QAction
        :type name: str
        :param q_action: QAction associated to name
        :type q_action: QAction
        """

        self.actions[name] = q_action

    def get(self, name):
        """
        Return QAction

        :param name: name of the QAction
        :type name: str
        """
        try:
            return self.actions[name]
        except KeyError as e:
            logger.error('Bad value for QAction : ' + str(e))
