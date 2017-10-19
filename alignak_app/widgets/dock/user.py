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
    User manage QWidget who display User Profile.
"""

from logging import getLogger

from alignak_app.core.backend import app_backend
from alignak_app.core.data_manager import data_manager
from alignak_app.core.utils import get_image_path, get_css
from alignak_app.widgets.common.frames import AppQFrame, get_frame_separator
from alignak_app.widgets.common.labels import get_enable_label_icon
from alignak_app.widgets.dock.events import send_event
from alignak_app.widgets.dialogs.user_options import show_options_dialog
from alignak_app.widgets.dialogs.token import TokenQDialog
from alignak_app.widgets.dialogs.password import PasswordQDialog
from alignak_app.widgets.dialogs.user_notes import UserNotesQDialog

from PyQt5.Qt import QGridLayout, QVBoxLayout, QLineEdit  # pylint: disable=no-name-in-module
from PyQt5.Qt import QIcon, Qt, QHBoxLayout, QLabel, QWidget  # pylint: disable=no-name-in-module
from PyQt5.Qt import QPushButton, QCheckBox  # pylint: disable=no-name-in-module

logger = getLogger(__name__)


class UserQWidget(QWidget):
    """
        Class who create QWidget for User Profile.
    """

    def __init__(self, parent=None):
        super(UserQWidget, self).__init__(parent)
        self.setStyleSheet(get_css())
        # Fields
        self.labels = {
            'realm': QLabel(),
            'role': QLabel(),
            'email': QLabel(),
            'is_admin': QLabel(),
            'can_submit_commands': QLabel(),
            'alias': QLabel(),
            'notes': QLabel(),
            'host_notifications_enabled': QLabel(),
            'host_notification_period': QLabel(),
            'service_notifications_enabled': QLabel(),
            'service_notification_period': QLabel(),
        }
        self.app_widget = None
        self.host_notif_state = None
        self.service_notif_state = None
        self.password_btn = None
        self.token_btn = QPushButton()
        self.notes_btn = None

    def initialize(self):
        """
        Initialize User QWidget

        """

        # Initialize AppQWidget
        self.app_widget = AppQFrame()
        self.app_widget.initialize(_('User View'))
        self.app_widget.add_widget(self)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.get_main_informations_widget())
        layout.addWidget(self.get_notifications_widget())

    def get_main_informations_widget(self):
        """
        Create and return informations QWidget

        :return: informations QWidget
        :rtype: QWidget
        """

        informations_widget = QWidget()
        informations_layout = QHBoxLayout()
        informations_widget.setLayout(informations_layout)

        informations_layout.addWidget(self.get_informations_widget())
        informations_layout.addWidget(self.get_notes_widget())

        return informations_widget

    def get_informations_widget(self):
        """
        Create and return QWidget with main informations

        :return: main QWidget
        :rtype: QWidget
        """

        main_user_widget = QWidget()
        main_layout = QGridLayout()
        main_user_widget.setLayout(main_layout)

        main_title = QLabel(_('User informations:'))
        main_title.setObjectName("title")
        main_layout.addWidget(main_title, 0, 0, 1, 4)
        main_layout.addWidget(get_frame_separator(), 1, 0, 1, 4)

        main_layout.addWidget(self.get_identity_widget(), 2, 0, 1, 2)
        main_layout.addWidget(self.get_rights_widget(), 2, 2, 1, 2)

        return main_user_widget

    def get_identity_widget(self):
        """
        Return informations QWidget

        :return: information QWidget
        :rtype: QWidget
        """

        information_widget = QWidget()
        info_layout = QGridLayout()
        information_widget.setLayout(info_layout)

        # Realm
        realm_title = QLabel(_('<h5>Realm:</h5>'))
        realm_title.setObjectName("subtitle")
        info_layout.addWidget(realm_title, 0, 0, 1, 1)
        info_layout.addWidget(self.labels['realm'], 0, 1, 1, 1)

        # Role
        role_title = QLabel(_('<h5>Role:</h5>'))
        role_title.setObjectName("subtitle")
        info_layout.addWidget(role_title, 1, 0, 1, 1)
        info_layout.addWidget(self.labels['role'], 1, 1, 1, 1)

        # Mail
        mail_title = QLabel(_('<h5>Email:</h5>'))
        mail_title.setObjectName("subtitle")
        info_layout.addWidget(mail_title, 2, 0, 1, 1)
        info_layout.addWidget(self.labels['email'], 2, 1, 1, 1)

        # Alias
        alias_title = QLabel(_('<h5>Alias:</h5>'))
        alias_title.setObjectName("subtitle")
        info_layout.addWidget(alias_title, 3, 0, 1, 1)
        info_layout.addWidget(self.labels['alias'], 3, 1, 1, 1)

        return information_widget

    def get_rights_widget(self):
        """
        Create and return Rights QWidget

        :return: rights QWidget
        :rtype: QWidget
        """

        rights_widget = QWidget()
        rights_layout = QGridLayout()
        rights_widget.setLayout(rights_layout)

        # Is Admin
        admin_title = QLabel(_('<h5>Administrator:</h5>'))
        admin_title.setObjectName("subtitle")
        admin_title.setMinimumHeight(32)
        rights_layout.addWidget(admin_title, 1, 0, 1, 1)
        self.labels['is_admin'].setFixedSize(14, 14)
        self.labels['is_admin'].setScaledContents(True)
        rights_layout.addWidget(self.labels['is_admin'], 1, 1, 1, 1)

        # Can submit commands
        command_title = QLabel(_('<h5>Commands:</h5>'))
        command_title.setObjectName("subtitle")
        command_title.setMinimumHeight(32)
        rights_layout.addWidget(command_title, 2, 0, 1, 1)
        self.labels['can_submit_commands'].setFixedSize(14, 14)
        self.labels['can_submit_commands'].setScaledContents(True)
        rights_layout.addWidget(self.labels['can_submit_commands'], 2, 1, 1, 1)

        # Password
        password_title = QLabel(_('<h5>Password:</h5>'))
        password_title.setObjectName("subtitle")
        rights_layout.addWidget(password_title, 3, 0, 1, 1)
        self.password_btn = QPushButton()
        self.password_btn.setObjectName("password")
        self.password_btn.clicked.connect(self.patch_data)
        self.password_btn.setIcon(QIcon(get_image_path('password')))
        self.password_btn.setToolTip(_('Change my password'))
        self.password_btn.setFixedSize(32, 32)
        rights_layout.addWidget(self.password_btn, 3, 1, 1, 1)

        # Token visible only for administrators
        token_title = QLabel(_('<h5>Token:</h5>'))
        token_title.setObjectName("subtitle")
        rights_layout.addWidget(token_title, 4, 0, 1, 2)

        self.token_btn.setIcon(QIcon(get_image_path('token')))
        self.token_btn.setFixedSize(32, 32)
        self.token_btn.clicked.connect(self.show_token_dialog)
        rights_layout.addWidget(self.token_btn, 4, 1, 1, 1)

        return rights_widget

    @staticmethod
    def show_token_dialog():
        """
        Show TokenQDialog

        """

        token_dialog = TokenQDialog()
        token_dialog.initialize()

        token_dialog.exec_()

    def get_notes_widget(self):
        """
        Create and return Notes QWidget

        :return: notes QWidget
        :rtype: QWidget
        """

        notes_widget = QWidget()
        notes_layout = QGridLayout()
        notes_widget.setLayout(notes_layout)

        main_notes_title = QLabel(_('Notes:'))
        main_notes_title.setObjectName("title")
        notes_layout.addWidget(main_notes_title, 0, 0, 1, 1)
        notes_layout.addWidget(get_frame_separator(), 1, 0, 1, 4)

        # Notes button
        self.notes_btn = QPushButton()
        self.notes_btn.setIcon(QIcon(get_image_path('edit')))
        self.notes_btn.setToolTip(_("Edit your notes."))
        self.notes_btn.setObjectName("notes")
        self.notes_btn.setFixedSize(32, 32)
        self.notes_btn.clicked.connect(self.patch_data)
        notes_layout.addWidget(self.notes_btn, 2, 3, 1, 1)

        # Create QLabel for notes
        self.labels['notes'].setText(data_manager.database['user'].data['notes'])
        self.labels['notes'].setWordWrap(True)
        self.labels['notes'].setObjectName('notes')
        notes_layout.addWidget(self.labels['notes'], 3, 0, 1, 4)

        notes_layout.setAlignment(Qt.AlignTop)

        return notes_widget

    def patch_data(self):
        """
        Hide and show QLabel for notes or PATCH password

        """

        btn = self.sender()

        if "notes" in btn.objectName():
            notes_dialog = UserNotesQDialog()
            notes_dialog.initialize(data_manager.database['user'].data['notes'])
            if notes_dialog.exec_() == UserNotesQDialog.Accepted:
                data = {'notes': str(notes_dialog.notes_edit.toPlainText())}
                headers = {'If-Match': data_manager.database['user'].data['_etag']}
                endpoint = '/'.join(['user', data_manager.database['user'].item_id])

                patched = app_backend.patch(endpoint, data, headers)

                if patched:
                    data_manager.database['user'].update_data(
                        'notes', notes_dialog.notes_edit.toPlainText()
                    )
                    self.labels['notes'].setText(notes_dialog.notes_edit.toPlainText())
                    message = _(
                        _("Your notes have been edited.")
                    )
                    send_event('INFO', message)
                else:
                    send_event(
                        'ERROR',
                        _("Backend PATCH failed, please check your logs !")
                    )
        elif "password" in btn.objectName():
            pass_dialog = PasswordQDialog()
            pass_dialog.initialize()

            if pass_dialog.exec_() == PasswordQDialog.Accepted:
                new_password = pass_dialog.pass_edit.text()

                data = {'password': str(new_password)}
                headers = {'If-Match': data_manager.database['user'].data['_etag']}
                endpoint = '/'.join(['user', data_manager.database['user'].item_id])

                patched = app_backend.patch(endpoint, data, headers)

                if patched:
                    message = _("Your password has been updated !")
                    send_event('OK', message)
                else:
                    send_event(
                        'ERROR', _("Backend PATCH failed, please check your logs !")
                    )
        else:
            logger.error("Wrong sender in UserProfile.")

    def get_notifications_widget(self):
        """
        Create and return notification QWidget for hosts and services

        :return: notifications QWidget
        :rtype: QWidget
        """

        notification_widget = QWidget()
        notification_layout = QGridLayout()
        notification_widget.setLayout(notification_layout)

        host_notif_widget = self.get_hosts_notif_widget()
        notification_layout.addWidget(host_notif_widget, 0, 0, 1, 1)
        notification_layout.setAlignment(host_notif_widget, Qt.AlignTop)

        services_notif_widget = self.get_services_notif_widget()
        notification_layout.addWidget(services_notif_widget, 0, 1, 1, 1)
        notification_layout.setAlignment(services_notif_widget, Qt.AlignTop)

        return notification_widget

    def get_hosts_notif_widget(self):
        """
        Create and return notification QWidget for hosts

        :return: hosts notification QWidget
        :rtype: QWidget
        """

        host_notif_widget = QWidget()
        host_notif_layout = QGridLayout()
        host_notif_widget.setLayout(host_notif_layout)

        notif_title = QLabel(_("Hosts notifications configurations"))
        notif_title.setObjectName("title")
        host_notif_layout.addWidget(notif_title, 0, 0, 1, 2)
        host_notif_layout.addWidget(get_frame_separator(), 1, 0, 1, 2)

        state_title = QLabel(_("<h5>Notification enabled:</h5>"))
        state_title.setObjectName("subtitle")
        host_notif_layout.addWidget(state_title, 2, 0, 1, 1)
        self.host_notif_state = QCheckBox()
        self.host_notif_state.setChecked(
            data_manager.database['user'].data['host_notifications_enabled']
        )
        self.host_notif_state.stateChanged.connect(self.enable_notifications)
        self.host_notif_state.setObjectName('hostactions')
        self.host_notif_state.setFixedSize(18, 18)
        host_notif_layout.addWidget(self.host_notif_state, 2, 1, 1, 1)

        period_title = QLabel(_("<h5>Notification period:</h5>"))
        period_title.setObjectName("subtitle")
        host_notif_layout.addWidget(period_title, 3, 0, 1, 1)
        self.labels['host_notification_period'].setText(
            app_backend.get_period_name(
                data_manager.database['user'].data['host_notification_period']
            )
        )
        host_notif_layout.addWidget(self.labels['host_notification_period'], 3, 1, 1, 1)

        option_btn = QPushButton()
        option_btn.setIcon(QIcon(get_image_path('options')))
        option_btn.setFixedSize(64, 32)
        option_btn.clicked.connect(lambda: show_options_dialog(
            'host',
            data_manager.database['user'].data['host_notification_options']
        ))

        host_notif_layout.addWidget(option_btn, 4, 0, 1, 2)
        host_notif_layout.setAlignment(option_btn, Qt.AlignCenter)

        return host_notif_widget

    def get_services_notif_widget(self):
        """
        Create and return notification QWidget for services

        :return: services notification QWidget
        :rtype: QWidget
        """

        service_notif_widget = QWidget()
        service_notif_layout = QGridLayout()
        service_notif_widget.setLayout(service_notif_layout)

        notif_title = QLabel(_("Services notifications configurations"))
        notif_title.setObjectName("title")
        service_notif_layout.addWidget(notif_title, 0, 0, 1, 2)
        service_notif_layout.addWidget(get_frame_separator(), 1, 0, 1, 2)

        state_title = QLabel(_("<h5>Notification enabled:</h5>"))
        state_title.setObjectName("subtitle")
        service_notif_layout.addWidget(state_title, 2, 0, 1, 1)
        self.service_notif_state = QCheckBox()
        self.service_notif_state.setObjectName('serviceactions')
        self.service_notif_state.setChecked(
            data_manager.database['user'].data['service_notifications_enabled']
        )
        self.service_notif_state.stateChanged.connect(self.enable_notifications)
        self.service_notif_state.setFixedSize(18, 18)
        service_notif_layout.addWidget(self.service_notif_state, 2, 1, 1, 1)

        period_title = QLabel(_("<h5>Notification period:</h5>"))
        period_title.setObjectName("subtitle")
        service_notif_layout.addWidget(period_title, 3, 0, 1, 1)
        self.labels['service_notification_period'].setText(
            app_backend.get_period_name(
                data_manager.database['user'].data['service_notification_period']
            )
        )
        service_notif_layout.addWidget(self.labels['service_notification_period'], 3, 1, 1, 1)

        option_btn = QPushButton()
        option_btn.setIcon(QIcon(get_image_path('options')))
        option_btn.setFixedSize(64, 32)
        option_btn.clicked.connect(lambda: show_options_dialog(
            'service',
            data_manager.database['user'].data['service_notification_options']
        ))

        service_notif_layout.addWidget(option_btn, 4, 0, 1, 2)
        service_notif_layout.setAlignment(option_btn, Qt.AlignCenter)

        return service_notif_widget

    def enable_notifications(self):  # pragma: no cover
        """
        Enable notification for the wanted type: hosts or services

        """

        check_btn = self.sender()

        notification_type = ''
        if 'hostactions' in check_btn.objectName():
            notification_type = 'host_notifications_enabled'
        elif 'serviceactions' in check_btn.objectName():
            notification_type = 'service_notifications_enabled'
        else:
            logger.error('Wrong caller %s', self.sender().objectName())

        if notification_type:
            # btn.checkState() equal to 0 or 2
            notification_enabled = bool(check_btn.checkState())

            data = {notification_type: notification_enabled}
            headers = {'If-Match': data_manager.database['user'].data['_etag']}
            endpoint = '/'.join(['user', data_manager.database['user'].item_id])

            patched = app_backend.patch(endpoint, data, headers)

            if patched:
                data_manager.database['user'].update_data(notification_type, notification_enabled)
                enabled = 'enabled' if notification_enabled else 'disabled'
                message = _("Notifications for %ss are %s") % (
                    check_btn.objectName().replace('actions', ''),
                    enabled
                )
                send_event('INFO', message)
            else:
                send_event(
                    'ERROR',
                    _("Backend PATCH failed, please check your logs !")
                )

    def update_widget(self):
        """
        Update UserQWidget

        """

        # Realm, Role, Email
        self.labels['realm'].setText(
            app_backend.get_realm_name(data_manager.database['user'].data['_realm'])
        )
        self.labels['role'].setText(data_manager.database['user'].get_role().capitalize())
        self.labels['email'].setText(data_manager.database['user'].data['email'])

        # Admin, Commands
        self.labels['is_admin'].setPixmap(
            get_enable_label_icon(data_manager.database['user'].data['is_admin'])
        )
        self.labels['can_submit_commands'].setPixmap(
            get_enable_label_icon(data_manager.database['user'].data['can_submit_commands'])
        )

        # Alias, Notes, Token
        self.labels['alias'].setText(data_manager.database['user'].data['alias'])

        if data_manager.database['user'].data['is_admin']:
            self.token_btn.setEnabled(True)
            self.token_btn.setToolTip(_('See my token'))
        else:
            self.token_btn.setEnabled(False)
            self.token_btn.setToolTip(_('Token is only available for Administrators !'))