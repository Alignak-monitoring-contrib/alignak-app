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
    Action_FActory build actions for TrayIcon.
"""

from logging import getLogger

from alignak_app.utils import get_image_path

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QAction  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QLabel # pylint: disable=no-name-in-module
    from PyQt5.QtGui import QIcon  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QAction  # pylint: disable=import-error
    from PyQt4.Qt import QLabel # pylint: disable=import-error
    from PyQt4.QtGui import QIcon  # pylint: disable=import-error


logger = getLogger(__name__)


class ActionFactory(object):
    """
        Create Action for
    """

    @staticmethod
    def create(icon, content, parent):
        """

        :return:
        """

        action = QAction(
            QIcon(get_image_path(icon)),
            content,
            parent
        )

        return action
