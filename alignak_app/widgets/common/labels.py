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
    Common QLabel manage creation of QLabels or QPixmaps
"""

from PyQt5.Qt import QPixmap

from alignak_app.core.config import get_image


def get_icon_item(item_type, problem_nb):
    """
    Return QPixmap with the corresponding image

    :param item_type: type of item: host, service or problem
    :type item_type: str
    :param problem_nb: problem number
    :type problem_nb: int
    :return: QPixmap with corresponding image
    :rtype: QPixmap
    """

    if problem_nb > 0:
        if item_type == 'host':
            icon_type = 'hosts_down'
        elif item_type == 'service':
            icon_type = 'services_critical'
        else:
            icon_type = 'problem'
    else:
        if item_type == 'host':
            icon_type = 'hosts_up'
        elif item_type == 'service':
            icon_type = 'services_ok'
        else:
            icon_type = 'problem_ok'
    icon = QPixmap(get_image(icon_type))

    return icon


def get_enable_label_icon(state):
    """
    Return red crosse or green check QPixmap, depending state is True of False

    :param state: state True of False
    :type state: bool
    :return: corresponding QPixmap
    :rtype: QPixmap
    """

    states = {
        True: 'checked',
        False: 'error'
    }

    # Should never happen
    if not isinstance(state, bool):
        state = False

    enable_pixmap = QPixmap(get_image(states[state]))

    return enable_pixmap
