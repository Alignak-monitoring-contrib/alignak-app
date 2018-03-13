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
    Widgets
    +++++++
    Widgets manage global QWidgets
"""

import sys

from PyQt5.Qt import QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QIcon, QLabel, QDialog
from PyQt5.Qt import QStyleOption, QStyle, QPainter, Qt, QApplication

from alignak_app.utils.config import settings


class LogoQWidget(QWidget):
    """
        Class who manage creation of Logo QWidget
    """

    def __init__(self):
        super(LogoQWidget, self).__init__()
        self.setFixedHeight(45)
        self.setObjectName('app_widget')
        self.setStyleSheet(settings.css_style)
        self.child_widget = None
        self.old_state = None

    def initialize(self, child_widget, title, exitapp):
        """
        Initialize QWidget

        :param child_widget: widget child of LogoQWidget, needed for action button and layout
        :type child_widget: QWidget
        :param title: title of widget
        :type title: str
        :param exitapp: define if close button close application or just child QWidget
        :type exitapp: bool
        """

        self.child_widget = child_widget

        logo_layout = QHBoxLayout()
        self.setLayout(logo_layout)

        logo_label = QLabel()
        logo_label.setObjectName('widget_title')
        logo_label.setText('<h3>%s</h3>' % title)
        logo_layout.addWidget(logo_label, 0)

        minimize_btn = QPushButton()
        minimize_btn.setIcon(QIcon(settings.get_image('minimize')))
        minimize_btn.setFixedSize(24, 24)
        minimize_btn.setObjectName('app_widget')
        minimize_btn.clicked.connect(self.minimize)
        logo_layout.addStretch(child_widget.width())
        logo_layout.addWidget(minimize_btn, 1)

        maximize_btn = QPushButton()
        maximize_btn.setIcon(QIcon(settings.get_image('maximize')))
        maximize_btn.setFixedSize(24, 24)
        maximize_btn.setObjectName('app_widget')
        maximize_btn.clicked.connect(self.minimize_maximize)
        logo_layout.addWidget(maximize_btn, 2)

        close_btn = QPushButton()
        close_btn.setIcon(QIcon(settings.get_image('exit')))
        close_btn.setObjectName('app_widget')
        close_btn.setFixedSize(24, 24)
        if exitapp:
            close_btn.clicked.connect(sys.exit)
        else:
            close_btn.clicked.connect(child_widget.close)
        logo_layout.addWidget(close_btn, 3)

    def paintEvent(self, _):  # pragma: no cover
        """Override to apply "background-color" property of QWidget"""

        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

    def minimize(self):  # pragma: no cover - not testable
        """
        Minimize QWidget

        """

        if self.child_widget.windowState() == Qt.WindowMinimized:
            self.child_widget.setWindowState(Qt.WindowNoState)
        else:
            self.old_state = self.child_widget.windowState()
            self.child_widget.setWindowState(Qt.WindowMinimized)

    def minimize_maximize(self):  # pragma: no cover - not testable
        """
        Minimize / Maximize QWidget

        """

        if self.child_widget.windowState() == Qt.WindowMaximized:
            if self.old_state:
                self.child_widget.setWindowState(self.old_state)
            else:
                self.child_widget.setWindowState(Qt.WindowNoState)
        else:
            self.old_state = self.child_widget.windowState()
            self.child_widget.setWindowState(Qt.WindowMaximized)


def get_logo_widget(child_widget, title, exitapp=False):
    """
    Return LogoQWidget with alignak logo

    :param child_widget: widget child of LogoQWidget, needed for action button and layout
    :type child_widget: QWidget
    :param title: title of widget
    :type title: str
    :param exitapp: define if close button close application or just child QWidget
    :type exitapp: bool
    :return: Logo QWidget with buttons and child QWidget
    :rtype: QWidget
    """

    logo_widget = LogoQWidget()
    logo_widget.initialize(child_widget, title, exitapp)

    return logo_widget


class MessageQDialog(QDialog):
    """
        Class who create a Message QDialog to display texts in Alignak-app
    """

    def __init__(self, parent=None):
        super(MessageQDialog, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(settings.css_style)
        self.setWindowIcon(QIcon(settings.get_image('icon')))
        self.setFixedSize(500, 200)
        self.setObjectName('dialog')

    def initialize(self, widgettitle, dialog, title, text):
        """
        Initialize QDialog for PasswordDialog

        :param widgettitle: title of the QDialog
        :type widgettitle: str
        :param dialog: type of dialog ('notes' or 'error')
        :type dialog: str
        :param title: title of text to display
        :type title: str
        :param text: text to display
        :type text: str
        """

        center_widget(self)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        main_layout.addWidget(get_logo_widget(self, widgettitle))
        main_layout.addWidget(self.get_message_widget(dialog, title, text))

    def get_message_widget(self, dialog, title, text):
        """
        Return colored message QWidget

        :param dialog: type of dialog ('notes' or 'error')
        :type dialog: str
        :param title: title of text to display
        :type title: str
        :param text: text to display
        :type text: str
        :return: message QWidget
        :rtype: QWidget
        """

        # Token QWidget
        token_widget = QWidget()
        token_widget.setObjectName('dialog')
        token_layout = QVBoxLayout()
        token_widget.setLayout(token_layout)

        token_title = QLabel(title)
        token_title.setObjectName('itemtitle')
        token_layout.addWidget(token_title)
        token_layout.setAlignment(token_title, Qt.AlignCenter)

        token_label = QLabel(text)
        token_label.setObjectName(dialog)
        token_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        token_label.setWordWrap(True)
        token_layout.addWidget(token_label)

        # Login button
        accept_btn = QPushButton('OK', self)
        accept_btn.clicked.connect(self.accept)
        accept_btn.setObjectName('ok')
        accept_btn.setMinimumHeight(30)
        token_layout.addWidget(accept_btn)

        return token_widget


def center_widget(widget):
    """
    Center QWidget

    :param widget: widget to center
    :type widget: QWidget
    """

    screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
    center = QApplication.desktop().screenGeometry(screen).center()
    widget.move(center.x() - (widget.width() / 2), center.y() - (widget.height() / 2))
