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
    Common QFrames manage creation of QFrames for Alignak-app
"""


from logging import getLogger

from PyQt5.Qt import QVBoxLayout
from PyQt5.Qt import Qt, QIcon, QPixmap, QFrame, QHBoxLayout, QPushButton, QLabel, QWidget

from alignak_app.core.utils.config import get_image, get_app_config, app_css
from alignak_app.pyqt.common.widgets import center_widget

logger = getLogger(__name__)


class AppQFrame(QFrame):
    """
        Class who create a QFrame container for App QWidgets
    """

    def __init__(self, parent=None):
        super(AppQFrame, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(get_image('icon')))
        self.setStyleSheet(app_css)
        self.offset = None

    def initialize(self, title, logo=False):
        """
        Initialize the QFrame, with its "title"

        :param title: title of frame
        :type title: str
        :param logo: Display logo or title
        :type logo: bool
        """

        self.setWindowTitle(title)
        self.setObjectName('app_widget')

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        main_layout.addWidget(self.get_logo_widget(title, logo))

        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def get_logo_widget(self, title, logo):
        """
        Return the logo QWidget

        :param title: title of frame
        :type title: str
        :param logo: Display logo or title
        :type logo: bool
        :return: logo QWidget
        :rtype: QWidget
        """

        logo_widget = QWidget()
        logo_widget.setFixedHeight(45)
        logo_widget.setObjectName('logo')
        logo_layout = QHBoxLayout()
        logo_widget.setLayout(logo_layout)

        logo_label = QLabel()
        logo_label.setObjectName('widget_title')
        logo_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        if logo:
            logo_label.setPixmap(QPixmap(get_image('alignak')))
            logo_label.setFixedSize(120, 30)
            logo_label.setScaledContents(True)

            logo_layout.addWidget(logo_label)
        else:
            logo_label.setText('<h3>%s</h3>' % title)

        logo_layout.addWidget(logo_label)
        logo_layout.setAlignment(logo_label, Qt.AlignHCenter)

        minimize_btn = QPushButton()
        minimize_btn.setIcon(QIcon(get_image('minimize')))
        minimize_btn.setFixedSize(22, 22)
        minimize_btn.setObjectName('app_widget')
        minimize_btn.clicked.connect(self.minimize)
        logo_layout.addWidget(minimize_btn)

        maximize_btn = QPushButton()
        maximize_btn.setIcon(QIcon(get_image('maximize')))
        maximize_btn.setFixedSize(22, 22)
        maximize_btn.setObjectName('app_widget')
        maximize_btn.clicked.connect(self.minimize_maximize)
        logo_layout.addWidget(maximize_btn)

        close_btn = QPushButton()
        close_btn.setIcon(QIcon(get_image('exit')))
        close_btn.setFixedSize(22, 22)
        close_btn.setObjectName('app_widget')
        close_btn.clicked.connect(self.close)
        logo_layout.addWidget(close_btn)

        return logo_widget

    def minimize(self):  # pragma: no cover - not testable
        """
        Minimize QWidget

        """

        if self.windowState() == Qt.WindowMinimized:
            self.setWindowState(Qt.WindowNoState)
        else:
            self.setWindowState(Qt.WindowMinimized)

    def minimize_maximize(self):  # pragma: no cover - not testable
        """
        Minimize / Maximize QWidget

        """

        if self.windowState() == Qt.WindowMaximized:
            self.setWindowState(Qt.WindowNoState)
        else:
            self.setWindowState(Qt.WindowMaximized)

    def show_widget(self):  # pragma: no cover - not testable
        """
        Show and center AppQWidget

        """

        center_widget(self)
        self.show()
        QWidget.activateWindow(self)

    def add_widget(self, widget):  # pragma: no cover - not testable
        """
        Add the main QWidget of AppQWidget

        :param widget: QWidget to add
        :type widget: QWidget
        """

        self.layout().addWidget(widget, 2)

    def mousePressEvent(self, event):  # pragma: no cover - not testable
        """ QWidget.mousePressEvent(QMouseEvent) """

        sticky = False

        if 'Dashboard' in self.windowTitle():
            sticky = bool(get_app_config('Dashboard', 'sticky', boolean=True))

        if not sticky:
            self.offset = event.pos()
        else:
            pass

    def mouseMoveEvent(self, event):  # pragma: no cover - not testable
        """ QWidget.mousePressEvent(QMouseEvent) """

        sticky = False

        if 'Dashboard' in self.windowTitle():
            sticky = bool(get_app_config('Dashboard', 'sticky', boolean=True))

        if not sticky:
            try:
                x = event.globalX()
                y = event.globalY()
                x_w = self.offset.x()
                y_w = self.offset.y()
                self.move(x - x_w, y - y_w)
            except AttributeError as e:
                logger.warning('Move Event %s: %s', self.objectName(), str(e))
        else:
            pass


def get_frame_separator():
    """
    Return a frame separator

    :return: frame separator
    :rtype: QFrame
    """

    line = QFrame()
    line.setObjectName('separator')
    line.setFrameShape(QFrame.HLine)

    return line
