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
    Actions display QDialog's for actions : Acknowledge and Downtime
"""


from logging import getLogger

from alignak_app.core.utils import get_image_path, get_css


try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QDialog, QWidget  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QPushButton, QLabel  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QGridLayout, QHBoxLayout  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QVBoxLayout, QTextEdit  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QIcon, QPixmap, QCheckBox, Qt  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QDialog, QWidget  # pylint: disable=import-error
    from PyQt4.Qt import QPushButton, QLabel  # pylint: disable=import-error
    from PyQt4.Qt import QGridLayout, QHBoxLayout  # pylint: disable=import-error
    from PyQt4.Qt import QVBoxLayout, QTextEdit  # pylint: disable=import-error
    from PyQt4.Qt import QIcon, QPixmap, QCheckBox, Qt  # pylint: disable=import-error


logger = getLogger(__name__)


def get_logo_widget(widget):
    """
    Return the logo QWidget

    :return: logo QWidget
    :rtype: QWidget
    """

    logo_widget = QWidget()
    logo_widget.setFixedHeight(45)
    logo_widget.setObjectName('title')
    logo_layout = QHBoxLayout()
    logo_widget.setLayout(logo_layout)

    logo_label = QLabel()
    logo_label.setPixmap(QPixmap(get_image_path('alignak')))
    logo_label.setFixedSize(121, 35)
    logo_label.setScaledContents(True)

    logo_layout.addWidget(logo_label, 0)

    minimize_btn = QPushButton()
    minimize_btn.setIcon(QIcon(get_image_path('minimize')))
    minimize_btn.setFixedSize(24, 24)
    minimize_btn.setObjectName('app_widget')
    minimize_btn.clicked.connect(widget.showMinimized)
    logo_layout.addStretch(widget.width())
    logo_layout.addWidget(minimize_btn, 1)

    maximize_btn = QPushButton()
    maximize_btn.setIcon(QIcon(get_image_path('maximize')))
    maximize_btn.setFixedSize(24, 24)
    maximize_btn.setObjectName('app_widget')
    maximize_btn.clicked.connect(widget.showMaximized)
    logo_layout.addWidget(maximize_btn, 2)

    close_btn = QPushButton()
    close_btn.setIcon(QIcon(get_image_path('exit')))
    close_btn.setObjectName('app_widget')
    close_btn.setFixedSize(24, 24)
    close_btn.clicked.connect(widget.close)
    logo_layout.addWidget(close_btn, 3)

    return logo_widget


class Acknowledge(QDialog):
    """
        Class who create Acknowledge QDialog for hosts/services
    """

    def __init__(self, parent=None):
        super(Acknowledge, self).__init__(parent)
        self.setWindowTitle('Login to Alignak')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(get_css())
        self.setWindowIcon(QIcon(get_image_path('icon')))
        self.setMinimumSize(360, 460)
        # Fields
        self.sticky = True
        self.notify = False
        self.ack_comment_edit = None

    def initialize(self, item_type, item_name, comment):
        """
        Initialize Acknowledge QDialog

        :param item_type: type of item to acknowledge : host | service
        :type item_type: str
        :param item_name: name of the item to acknowledge
        :type item_name: str
        :param comment: the default comment of action
        :type comment: str
        """

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(get_logo_widget(self))

        ack_widget = QWidget()
        ack_widget.setObjectName('login')
        ack_layout = QGridLayout(ack_widget)

        ack_title = QLabel('<h2>Request an acknowledge</h2>')
        ack_layout.addWidget(ack_title, 0, 0, 1, 2)

        host_label = QLabel('<h2>%s: %s</h2>' % (item_type.capitalize(), item_name))
        ack_layout.addWidget(host_label, 1, 0, 1, 1)

        sticky_label = QLabel('Acknowledge is sticky:')
        sticky_label.setObjectName('actions')
        ack_layout.addWidget(sticky_label, 2, 0, 1, 1)

        sticky_checkbox = QCheckBox()
        sticky_checkbox.setObjectName('actions')
        sticky_checkbox.setChecked(self.sticky)
        sticky_checkbox.setFixedSize(18, 18)
        ack_layout.addWidget(sticky_checkbox, 2, 1, 1, 1)

        sticky_info = QLabel(
            '<i>If checked, '
            'the acknowledge will remain until the element returns to an "OK" state.</i>'
        )
        sticky_info.setWordWrap(True)
        ack_layout.addWidget(sticky_info, 3, 0, 1, 2)

        notify_label = QLabel('Acknowledge notifies:')
        notify_label.setObjectName('actions')
        ack_layout.addWidget(notify_label, 4, 0, 1, 1)

        notify_checkbox = QCheckBox()
        notify_checkbox.setObjectName('actions')
        notify_checkbox.setChecked(self.notify)
        notify_checkbox.setFixedSize(18, 18)
        ack_layout.addWidget(notify_checkbox, 4, 1, 1, 1)

        notify_info = QLabel(
            '<i>If checked, a notification will be sent out to the concerned contacts.'
        )
        notify_info.setWordWrap(True)
        ack_layout.addWidget(notify_info, 5, 0, 1, 2)

        ack_comment = QLabel('Acknowledge comment:')
        ack_comment.setObjectName('actions')
        ack_layout.addWidget(ack_comment, 6, 0, 1, 1)

        self.ack_comment_edit = QTextEdit()
        self.ack_comment_edit.setText(comment)
        self.ack_comment_edit.setMaximumHeight(60)
        ack_layout.addWidget(self.ack_comment_edit, 7, 0, 1, 2)

        # Login button
        login_button = QPushButton('REQUEST ACKNOWLEDGE', self)
        login_button.clicked.connect(self.accept)
        login_button.setObjectName('valid')
        login_button.setMinimumHeight(30)
        login_button.setDefault(True)
        ack_layout.addWidget(login_button, 8, 0, 1, 2)

        main_layout.addWidget(ack_widget)

    def mousePressEvent(self, event):
        """ QWidget.mousePressEvent(QMouseEvent) """

        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        """ QWidget.mousePressEvent(QMouseEvent) """

        try:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)
        except AttributeError as e:
            logger.warning('Move Event %s: %s', self.objectName(), str(e))


if __name__ == '__main__':  # pylint: disable-all
    from PyQt5.QtWidgets import QApplication
    from alignak_app.core.utils import init_config
    import sys

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    init_config()
    ack_dialog = Acknowledge()
    ack_dialog.initialize('host', 'pi2', 'Acknowledge requested by App')

    if ack_dialog.exec_() == ack_dialog.Accepted:
        print('Ok')
    else:
        print('Out')

    sys.exit(app.exec_())
