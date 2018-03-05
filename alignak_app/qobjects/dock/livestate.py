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
    Livestate
    +++++++++
    Livestate manage creation fo QWidget to resume number of:

     * Number of hosts monitored and in problem
     * Number of services monitored and in problem
     * Number of item monitored and in problems
"""

from logging import getLogger

from PyQt5.Qt import QLabel, QTimer
from PyQt5.Qt import QWidget, QVBoxLayout, QHBoxLayout, Qt, QStyleOption, QPainter, QStyle

from alignak_app.backend.datamanager import data_manager
from alignak_app.utils.config import settings

from alignak_app.qobjects.common.labels import get_icon_item

logger = getLogger(__name__)


class LivestateQWidget(QWidget):
    """
        Class who display items livestate: hosts, services and number of problems
    """

    def __init__(self):
        super(LivestateQWidget, self).__init__()
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

        update_livestate = int(settings.get_config('Alignak-app', 'update_livestate')) * 1000
        self.timer.setInterval(update_livestate)
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

        problem_label = QLabel('%d' % problem_nb)
        problem_label.setObjectName('ok')
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
        Update QLabels of QWidget

        """

        items_and_problems = data_manager.get_items_and_problems()

        for item_type in self.labels:
            if items_and_problems[item_type]['problem'] < 1:
                self.labels[item_type]['problem'].setObjectName('ok')
            else:
                self.labels[item_type]['problem'].setObjectName('ko')

            self.labels[item_type]['problem'].style().unpolish(self.labels[item_type]['problem'])
            self.labels[item_type]['problem'].style().polish(self.labels[item_type]['problem'])
            self.labels[item_type]['problem'].update()

            self.labels[item_type]['problem'].setText(
                '%s' % str(items_and_problems[item_type]['problem'])
            )
            self.labels[item_type]['icon'].setPixmap(
                get_icon_item(item_type, items_and_problems[item_type]['problem'])
            )
            self.labels[item_type]['total'].setText(
                '%s' % str(items_and_problems[item_type]['total'])
            )

    def paintEvent(self, _):
        """Override paintEvent to paint background"""

        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
