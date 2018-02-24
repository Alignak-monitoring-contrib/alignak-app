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

"""
    QActions Factory
    ++++++++++++++++
    QAction Factory manage creation of QActions for TrayIcon.
"""

from logging import getLogger

from PyQt5.Qt import QAction, QIcon

from alignak_app.utils.config import settings

logger = getLogger(__name__)


class QActionFactory(object):
    """
        Create QActions with its icon and content
    """

    def __init__(self):
        self.actions = {}

    def create(self, name, content, parent):
        """
        Create QAction

        """

        q_action = QAction(
            QIcon(settings.get_image(name)),
            content,
            parent
        )

        self.actions[name] = q_action

    def get_action(self, name):
        """
        Return QAction

        :param name: name of the QAction
        :type name: str
        :return: wanted QAction
        :rtype: QAction
        """

        try:
            return self.actions[name]
        except KeyError as e:
            logger.error('Bad value for QAction : %s', e)
