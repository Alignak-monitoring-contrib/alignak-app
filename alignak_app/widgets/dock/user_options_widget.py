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
    TODO
"""

from logging import getLogger

from PyQt5.Qt import QGridLayout, QLabel, QWidget  # pylint: disable=no-name-in-module

from alignak_app.widgets.common.common_labels import get_enable_label_icon

logger = getLogger(__name__)


class UserOptionsQWidget(QWidget):
    """
        TODO
    """

    def __init__(self, parent=None):
        super(UserOptionsQWidget, self).__init__(parent)
        self.options_labels = {
            'host': {
                'd': QLabel(),
                'u': QLabel(),
                'r': QLabel(),
                'f': QLabel(),
                's': QLabel(),
                'n': QLabel()
            },
            'service': {
                'w': QLabel(),
                'u': QLabel(),
                'c': QLabel(),
                'r': QLabel(),
                'f': QLabel(),
                's': QLabel(),
                'n': QLabel()
            }
        }
        self.titles_labels = {
            'host': {
                'd': QLabel('DOWN'),
                'u': QLabel('UNREACHABLE'),
                'r': QLabel('RECOVERY'),
                'f': QLabel('FLAPPING'),
                's': QLabel('DOWNTIME'),
                'n': QLabel('NONE')
            },
            'service': {
                'w': QLabel('WARNING'),
                'u': QLabel('UNKNOWN'),
                'c': QLabel('CRITICAL'),
                'r': QLabel('RECOVERY'),
                'f': QLabel('FLAPPING'),
                's': QLabel('DOWNTIME'),
                'n': QLabel('NONE')
            }
        }

    def initialize(self, item_type, options):
        """
        Create QWidget with options and their icons

        :param item_type: define item type for options: host or service
        :type item_type: str
        :param options: list of notification options
        :type options: list
        :return: QWidget with options and icons
        :rtype: QWidget
        """

        selected_options = self.get_selected_options(item_type, options)

        line = 0
        layout = QGridLayout()
        self.setLayout(layout)
        for opt in selected_options:
            # Title
            layout.addWidget(self.titles_labels[item_type][opt], line, 0, 1, 1)
            # Icon
            self.options_labels[item_type][opt].setPixmap(
                get_enable_label_icon(selected_options[opt])
            )
            self.options_labels[item_type][opt].setFixedSize(14, 14)
            self.options_labels[item_type][opt].setScaledContents(True)
            layout.addWidget(self.options_labels[item_type][opt], line, 1, 1, 1)
            line += 1

    @staticmethod
    def get_selected_options(item_type, options):
        """
        TODO
        :return:
        """

        items_options = {
            'host': ['d', 'u', 'r', 'f', 's', 'n'],
            'service': ['w', 'u', 'c', 'r', 'f', 's', 'n']
        }

        available_options = items_options[item_type]

        selected_options = {}
        for opt in available_options:
            selected_options[opt] = bool(opt in options)

        return selected_options
