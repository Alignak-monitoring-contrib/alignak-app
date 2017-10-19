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
    Livestate QWidget manage resume of hosts, services and problems
"""

from alignak_app.core.utils import get_css
from alignak_app.core.data_manager import data_manager
from alignak_app.widgets.common.common_labels import get_icon_item

from PyQt5.Qt import QWidget, QVBoxLayout, QHBoxLayout, Qt  # pylint: disable=no-name-in-module
from PyQt5.Qt import QLabel, QTimer  # pylint: disable=no-name-in-module


class LivestateQWidget(QWidget):
    """
        Class who display items livestate: hosts, services and number of problems
    """

    def __init__(self):
        super(LivestateQWidget, self).__init__()
        self.setStyleSheet(get_css())
        # Fields
        self.labels = {
            'host': None,
            'service': None,
            'problem': None
        }
        self.timer = QTimer()

    def initialize(self):
        """
        Initialize QWidget

        """

        layout = QHBoxLayout()
        self.setLayout(layout)

        item_types = ['host', 'service', 'problem']

        for item_type in item_types:
            item_widget = self.get_item_type_widget(item_type, 0, 0)
            layout.addWidget(item_widget)

        self.update_labels()

        self.timer.setInterval(15000)
        self.timer.start()
        self.timer.timeout.connect(self.update_labels)

    def get_item_type_widget(self, item_type, problem_nb, total_nb):
        """
        Create and return QWidget with backend data

        :param item_type: type of item: host, service, problem
        :type item_type: str
        :param problem_nb: number of problems for item type
        :type problem_nb: int
        :param total_nb: total number of item type
        :type total_nb: int
        :return: widget with its data
        :rtype: QWidget
        """

        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        widget.setObjectName('livestate')

        problem_label = QLabel('%d' % problem_nb)
        problem_label.setObjectName('ko')
        problem_label.setToolTip(
            _('Number of unhandled %s problems') % (
                item_type if 'problem' not in item_type else ''
            )
        )
        layout.addWidget(problem_label)
        layout.setAlignment(problem_label, Qt.AlignCenter)

        icon_label = QLabel()
        icon_label.setFixedSize(64, 64)
        icon_label.setScaledContents(True)
        icon_label.setObjectName('livestate')
        layout.addWidget(icon_label)
        layout.setAlignment(icon_label, Qt.AlignCenter)

        total_label = QLabel('%d' % total_nb)
        total_label.setObjectName('total')
        total_label.setToolTip(
            _('Number of monitored %s') % (
                item_type if 'problem' not in item_type else 'items'
            )
        )
        layout.addWidget(total_label)
        layout.setAlignment(total_label, Qt.AlignCenter)

        self.labels[item_type] = {
            'problem': problem_label,
            'icon': icon_label,
            'total': total_label
        }

        return widget

    def update_labels(self):
        """
        Update Qlabels of widget

        """

        items_and_problems = data_manager.get_items_and_problems()

        for item_type in self.labels:
            self.labels[item_type]['problem'].setText(
                '%s' % str(items_and_problems[item_type]['problem'])
            )
            self.labels[item_type]['icon'].setPixmap(
                get_icon_item(item_type, items_and_problems[item_type]['problem'])
            )
            self.labels[item_type]['total'].setText(
                '%s' % str(items_and_problems[item_type]['total'])
            )
