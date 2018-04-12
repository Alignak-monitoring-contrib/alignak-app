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
    Customs
    +++++++
    Customs manage creation of QWidget to display custom variables of an host
"""


from logging import getLogger

from PyQt5.Qt import QWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, Qt, QVBoxLayout
from PyQt5.Qt import QStyle, QStyleOption, QPainter

from alignak_app.utils.config import settings

from alignak_app.qobjects.common.widgets import center_widget, get_logo_widget

logger = getLogger(__name__)


class CustomsQWidget(QWidget):
    """
        Class who create Customs Qwidget for host
    """

    def __init__(self, parent=None):
        super(CustomsQWidget, self).__init__(parent)
        self.setStyleSheet(settings.css_style)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName('dialog')
        self.setMinimumSize(420, 330)
        # Fields
        self.customs_table = QTableWidget()
        self.table_headers = ['Variable', 'Value']
        self.offset = None

    def initialize(self):
        """
        Initialize Customs QWidget

        """

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Title Window
        main_layout.addWidget(
            get_logo_widget(self, _('Custom variables'))
        )

        # Customs QWidget
        customs_widget = QWidget()
        customs_layout = QVBoxLayout(customs_widget)

        # Customs QTableWidget
        self.customs_table.setObjectName('history')
        self.customs_table.verticalHeader().hide()
        self.customs_table.setColumnCount(len(self.table_headers))
        self.customs_table.setColumnWidth(0, 200)
        self.customs_table.setColumnWidth(1, 200)
        self.customs_table.setSortingEnabled(True)
        self.customs_table.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)
        self.customs_table.setHorizontalHeaderLabels(self.table_headers)
        self.customs_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.customs_table.horizontalHeader().setStretchLastSection(True)
        self.customs_table.horizontalHeader().setMinimumHeight(30)
        customs_layout.addWidget(self.customs_table)

        main_layout.addWidget(customs_widget)

        center_widget(self)

    def update_customs(self, host_item):
        """
        Update customs QTableWidget with customs of host item

        :param host_item: Host item
        :type host_item: alignak_app.items.host.Host
        """

        logger.debug('Open Customs for %s', host_item.name)

        self.customs_table.clear()
        self.customs_table.setHorizontalHeaderLabels(self.table_headers)
        self.customs_table.setRowCount(len(host_item.data['customs']))

        row = 0
        for custom in host_item.data['customs']:
            title_item = QTableWidgetItem()
            title = ''
            if '_' in custom[:1]:
                title = custom[1:]
            title = title.replace('_', ' ').capitalize()
            title_item.setText(title)
            title_item.setToolTip(custom)
            self.customs_table.setItem(row, 0, title_item)

            data_item = QTableWidgetItem()
            data_item.setText(str(host_item.data['customs'][custom]))
            self.customs_table.setItem(row, 1, data_item)

            row += 1

    def paintEvent(self, _):  # pragma: no cover
        """Override to apply "background-color" property of QWidget"""

        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

    def mousePressEvent(self, event):  # pragma: no cover
        """ QWidget.mousePressEvent(QMouseEvent) """

        self.offset = event.pos()

    def mouseMoveEvent(self, event):  # pragma: no cover
        """ QWidget.mousePressEvent(QMouseEvent) """

        try:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)
        except AttributeError as e:
            logger.warning('Move Event %s: %s', self.objectName(), str(e))
