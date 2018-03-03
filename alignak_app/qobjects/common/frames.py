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
    Frames
    ++++++
    Frames manage global QFrames for Alignak-app
"""


from logging import getLogger

from PyQt5.Qt import Qt, QIcon, QPixmap, QFrame, QHBoxLayout, QPushButton, QLabel, QWidget
from PyQt5.Qt import QVBoxLayout

from alignak_app.utils.config import settings

from alignak_app.qobjects.common.widgets import center_widget

logger = getLogger(__name__)


class AppQFrame(QFrame):
    """
        Class who create a QFrame container for App QWidgets
    """

    def __init__(self, parent=None):
        super(AppQFrame, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        self.setStyleSheet(settings.css_style)
        self.child_widget = None
        self.offset = None

    def initialize(self, title):
        """
        Initialize the QFrame, with its "title"

        :param title: title of frame
        :type title: str
        """

        self.setWindowTitle(title)
        self.setObjectName('app_widget')

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        main_layout.addWidget(self.get_title_widget(title))

        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def get_title_widget(self, title):
        """
        Return the title QWidget for App windows

        :param title: title of frame
        :type title: str
        :return: a title QWidget
        :rtype: QWidget
        """

        title_widget = QWidget()
        title_widget.setFixedHeight(45)
        title_widget.setObjectName('logo')
        title_layout = QHBoxLayout()
        title_widget.setLayout(title_layout)

        logo_label = QLabel()
        logo_label.setObjectName('widget_title')
        logo_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        logo_label.setText('<h3>%s</h3>' % title)
        title_layout.addWidget(logo_label)
        title_layout.setAlignment(logo_label, Qt.AlignHCenter)

        minimize_btn = QPushButton()
        minimize_btn.setIcon(QIcon(settings.get_image('minimize')))
        minimize_btn.setFixedSize(22, 22)
        minimize_btn.setObjectName('app_widget')
        minimize_btn.clicked.connect(self.minimize)
        title_layout.addWidget(minimize_btn)

        maximize_btn = QPushButton()
        maximize_btn.setIcon(QIcon(settings.get_image('maximize')))
        maximize_btn.setFixedSize(22, 22)
        maximize_btn.setObjectName('app_widget')
        maximize_btn.clicked.connect(self.minimize_maximize)
        title_layout.addWidget(maximize_btn)

        close_btn = QPushButton()
        close_btn.setIcon(QIcon(settings.get_image('exit')))
        close_btn.setFixedSize(22, 22)
        close_btn.setObjectName('app_widget')
        close_btn.clicked.connect(self.close_widget)
        title_layout.addWidget(close_btn)

        return title_widget

    def minimize(self):  # pragma: no cover - not testable
        """
        Minimize QFrame

        """

        if self.windowState() == Qt.WindowMinimized:
            self.setWindowState(Qt.WindowNoState)
        else:
            self.setWindowState(Qt.WindowMinimized)

    def minimize_maximize(self):  # pragma: no cover - not testable
        """
        Minimize / Maximize QFrame

        """

        if self.windowState() == Qt.WindowMaximized:
            self.setWindowState(Qt.WindowNoState)
        else:
            self.setWindowState(Qt.WindowMaximized)

    def close_widget(self):
        """
        Close QFrame and child widget

        """

        self.child_widget.close()
        self.close()

    def show_widget(self):  # pragma: no cover - not testable
        """
        Show and center QFrame and child widget

        """

        center_widget(self)
        self.child_widget.show()
        self.show()
        QWidget.activateWindow(self)

    def add_widget(self, widget):  # pragma: no cover - not testable
        """
        Add the child QWidget of AppQWidget

        :param widget: QWidget to add
        :type widget: QWidget
        """

        self.child_widget = widget
        self.layout().addWidget(widget, 1)

    def mousePressEvent(self, event):  # pragma: no cover - not testable
        """ QWidget.mousePressEvent(QMouseEvent) """

        self.offset = event.pos()

    def mouseMoveEvent(self, event):  # pragma: no cover - not testable
        """ QWidget.mousePressEvent(QMouseEvent) """

        try:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)
        except AttributeError as e:
            logger.warning('Move Event %s: %s', self.objectName(), str(e))


def get_frame_separator(vertical=False):
    """
    Return a frame separator

    :param vertical: define if separator is vertical or horizontal
    :type vertical: bool
    :return: frame separator
    :rtype: QFrame
    """

    line = QFrame()
    if vertical:
        line.setObjectName('vseparator')
        line.setFrameShape(QFrame.VLine)
    else:
        line.setObjectName('hseparator')
        line.setFrameShape(QFrame.HLine)

    return line
