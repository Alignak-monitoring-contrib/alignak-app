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

from alignak_app.core.utils import get_image_path, get_css
from alignak_app.core.backend import app_backend
from alignak_app.core.data_manager import data_manager
from alignak_app.user.password import PasswordDialog
from alignak_app.models.item_user import User
from alignak_app.widgets.app_widget import AppQWidget
from alignak_app.dock.events_widget import events_widget

from PyQt5.Qt import QIcon, QPixmap, Qt  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QLabel, QLineEdit, QDialog  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox  # pylint: disable=no-name-in-module

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
            'token': QLabel(),
            'notes': QLabel(),
            'host_notifications_enabled': QLabel(),
            'host_notification_period': QLabel(),
            'service_notification_enabled': QLabel(),
            'service_notification_period': QLabel(),
        }
        self.opt_labels = {
            'host': {},
            'service': {}
        }
        self.app_widget = None
        self.host_notif_state = None
        self.service_notif_state = None
        self.password_btn = None
        self.notes_btn = None
        self.notes_edit = None

    def initialize(self):
        """
        Initialize User QWidget

        """

        # Initialize AppQWidget
        self.app_widget = AppQWidget()
        self.app_widget.initialize(_('User View'))
        self.app_widget.add_widget(self)

        # first creation of QWidget
        self.create_widget()

    def create_widget(self):
        """
        Create or update the user QWidget. Separate function from initialize() for pyqtSignal

        """

        old_pos = None
        logger.debug("Delete old UserProfile")
        if self.app_widget:
            old_pos = self.app_widget.pos()

        if old_pos:
            self.app_widget.move(old_pos)

        if self.layout():
            # Clean layout
            for i in reversed(range(self.layout().count())):
                self.layout().itemAt(i).widget().deleteLater()
            layout = self.layout()
        else:
            layout = QVBoxLayout()
            self.setLayout(layout)

        layout.addWidget(self.get_main_user_widget())
        layout.addWidget(self.get_notes_widget())

        layout.addWidget(self.get_notifications_widget())

    def get_main_user_widget(self):
        """
        Create and return QWidget with main informations

        :return: main QWidget
        :rtype: QWidget
        """

        main_user_widget = QWidget()
        main_layout = QGridLayout()
        main_user_widget.setLayout(main_layout)

        main_title = QLabel(_('Main informations:'))
        main_title.setObjectName("usertitle")
        main_layout.addWidget(main_title, 0, 0, 1, 2)

        rights_title = QLabel(_('Rights:'))
        rights_title.setObjectName("usertitle")
        main_layout.addWidget(rights_title, 0, 2, 1, 2)

        main_layout.addWidget(self.get_information_widget(), 1, 0, 1, 2)
        main_layout.addWidget(self.get_rights_widget(), 1, 2, 1, 2)

        return main_user_widget

    def get_information_widget(self):
        """
        Return informations QWidget

        :return: information QWidget
        :rtype: QWidget
        """

        information_widget = QWidget()
        info_layout = QGridLayout()
        information_widget.setLayout(info_layout)

        realm_title = QLabel(_('Realm:'))
        realm_title.setObjectName("usersubtitle")
        info_layout.addWidget(realm_title, 0, 0, 1, 1)
        self.labels['realm'].setText(User.get_realm_name())
        info_layout.addWidget(self.labels['realm'], 0, 1, 1, 1)

        role_title = QLabel(_('Role:'))
        role_title.setObjectName("usersubtitle")
        info_layout.addWidget(role_title, 1, 0, 1, 1)
        self.labels['role'].setText(User.get_role().capitalize())
        info_layout.addWidget(self.labels['role'], 1, 1, 1, 1)

        mail_title = QLabel(_('Email:'))
        mail_title.setObjectName("usersubtitle")
        info_layout.addWidget(mail_title, 2, 0, 1, 1)
        self.labels['email'].setText(data_manager.database['user'].data['email'])
        info_layout.addWidget(self.labels['email'], 2, 1, 1, 1)

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

        admin_title = QLabel(_('Administrator:'))
        admin_title.setObjectName("usersubtitle")
        admin_title.setMinimumHeight(32)
        rights_layout.addWidget(admin_title, 1, 0, 1, 1)
        self.labels['is_admin'].setPixmap(
            self.get_enable_label_icon(data_manager.database['user'].data['is_admin'])
        )
        self.labels['is_admin'].setFixedSize(18, 18)
        self.labels['is_admin'].setScaledContents(True)
        rights_layout.addWidget(self.labels['is_admin'], 1, 1, 1, 1)

        command_title = QLabel(_('Commands:'))
        command_title.setObjectName("usersubtitle")
        command_title.setMinimumHeight(32)
        rights_layout.addWidget(command_title, 2, 0, 1, 1)
        self.labels['can_submit_commands'].setPixmap(
            self.get_enable_label_icon(data_manager.database['user'].data['can_submit_commands'])
        )
        self.labels['can_submit_commands'].setFixedSize(18, 18)
        self.labels['can_submit_commands'].setScaledContents(True)
        rights_layout.addWidget(self.labels['can_submit_commands'], 2, 1, 1, 1)

        password_title = QLabel(_('Password:'))
        password_title.setObjectName("usersubtitle")
        rights_layout.addWidget(password_title, 3, 0, 1, 1)
        self.password_btn = QPushButton()
        self.password_btn.setObjectName("password")
        self.password_btn.clicked.connect(self.edit_notes)
        self.password_btn.setIcon(QIcon(get_image_path('password')))
        self.password_btn.setFixedSize(32, 32)
        rights_layout.addWidget(self.password_btn, 3, 1, 1, 1)

        return rights_widget

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
        main_notes_title.setObjectName("usertitle")
        notes_layout.addWidget(main_notes_title, 0, 0, 1, 3)

        # Alias
        alias_title = QLabel(_('Alias:'))
        alias_title.setObjectName("usersubtitle")
        notes_layout.addWidget(alias_title, 1, 0, 1, 1)
        self.labels['alias'].setText(data_manager.database['user'].data['alias'])
        notes_layout.addWidget(self.labels['alias'], 1, 1, 1, 2)

        # Token only for administrators
        if data_manager.database['user'].data['is_admin']:
            token_title = QLabel(_('Token:'))
            token_title.setObjectName("usersubtitle")
            notes_layout.addWidget(token_title, 2, 0, 1, 2)

            self.labels['token'].setText(data_manager.database['user'].data['token'])
            self.labels['token'].setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.labels['token'].setCursor(Qt.IBeamCursor)
            notes_layout.addWidget(self.labels['token'], 2, 1, 1, 1)

        # Notes
        notes_title = QLabel(_('Notes:'))
        notes_title.setObjectName("usersubtitle")
        notes_layout.addWidget(notes_title, 3, 0, 1, 1)

        # Add and hide QLineEdit; Shown only when edited
        self.notes_edit = QLineEdit()
        self.notes_edit.hide()
        self.notes_edit.editingFinished.connect(self.patch_notes)
        self.notes_edit.setToolTip(_('Type enter to validate your notes.'))
        notes_layout.addWidget(self.notes_edit, 4, 1, 1, 1)

        # Create QLabel for notes
        self.labels['notes'].setText(data_manager.database['user'].data['notes'])
        notes_layout.addWidget(self.labels['notes'], 4, 1, 1, 1)

        # Edit button for notes
        self.notes_btn = QPushButton()
        self.notes_btn.setIcon(QIcon(get_image_path('edit')))
        self.notes_btn.setToolTip(_("Edit your notes."))
        self.notes_btn.setObjectName("notes")
        self.notes_btn.setFixedSize(32, 32)
        self.notes_btn.clicked.connect(self.edit_notes)

        notes_layout.addWidget(self.notes_btn, 4, 2, 1, 1)

        return notes_widget

    def edit_notes(self):
        """
        Hide and show QLabel for notes or PATCH password

        """

        btn = self.sender()

        if "notes" in btn.objectName():
            self.labels['notes'].hide()
            self.notes_edit.setText(self.labels['notes'].text())
            self.notes_edit.show()
            self.notes_edit.setFocus()
        elif "password" in btn.objectName():
            pass_dialog = PasswordDialog()
            pass_dialog.initialize()

            if pass_dialog.exec_() == QDialog.Accepted:
                new_password = pass_dialog.pass_edit.text()

                data = {'password': str(new_password)}
                headers = {'If-Match': data_manager.database['user'].data['_etag']}
                endpoint = '/'.join(['user', data_manager.database['user'].item_id])

                patched = app_backend.patch(endpoint, data, headers)

                if patched:
                    message = _("Your password has been updated !")
                    events_widget.add_event('OK', message)
                else:
                    events_widget.add_event(
                        'ERROR', _("Backend PATCH failed, please check your logs !")
                    )
        else:
            logger.error("Wrong sender in UserProfile.")

    def patch_notes(self):
        """
        Patch notes user when edition is finished

        """

        # Patch only if text have really changed
        if bool(self.notes_edit.text() != data_manager.database['user'].data['notes']):
            data = {'notes': str(self.notes_edit.text())}
            headers = {'If-Match': data_manager.database['user'].data['_etag']}
            endpoint = '/'.join(['user', data_manager.database['user'].item_id])

            patched = app_backend.patch(endpoint, data, headers)

            if patched:
                data_manager.database['user'].update_data('notes', self.notes_edit.text())
                message = _(
                    _("The notes for the %s have been edited.")
                ) % data_manager.database['user'].name
                events_widget.add_event('OK', message)
            else:
                events_widget.add_event('ERROR', _("Backend PATCH failed, please check your logs !"))

            # thread_manager.add_task('user')
            self.update_widget()
        else:
            self.labels['notes'].show()
            self.notes_edit.hide()

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
        notif_title.setObjectName("usertitle")
        host_notif_layout.addWidget(notif_title, 0, 0, 1, 2)

        state_title = QLabel(_("State:"))
        state_title.setObjectName("usersubtitle")
        host_notif_layout.addWidget(state_title, 1, 0, 1, 1)
        self.host_notif_state = QCheckBox()
        self.host_notif_state.setChecked(
            data_manager.database['user'].data['host_notifications_enabled']
        )
        self.host_notif_state.stateChanged.connect(self.enable_notifications)
        self.host_notif_state.setObjectName('hostactions')
        self.host_notif_state.setFixedSize(18, 18)
        host_notif_layout.addWidget(self.host_notif_state, 1, 1, 1, 1)

        enable_title = QLabel(_("Notification enabled:"))
        enable_title.setMinimumHeight(32)
        enable_title.setObjectName("usersubtitle")
        host_notif_layout.addWidget(enable_title, 2, 0, 1, 1)
        self.labels['host_notifications_enabled'].setPixmap(
            self.get_enable_label_icon(
                data_manager.database['user'].data['host_notifications_enabled']
            )
        )
        self.labels['host_notifications_enabled'].setFixedSize(18, 18)
        self.labels['host_notifications_enabled'].setScaledContents(True)
        host_notif_layout.addWidget(self.labels['host_notifications_enabled'], 2, 1, 1, 1)

        period_title = QLabel(_("Notification period:"))
        period_title.setObjectName("usersubtitle")
        host_notif_layout.addWidget(period_title, 3, 0, 1, 1)
        period = User.get_period_name(
            data_manager.database['user'].data['host_notification_period']
        )
        self.labels['host_notification_period'].setText(period.capitalize())
        host_notif_layout.addWidget(self.labels['host_notification_period'], 3, 1, 1, 1)

        option_title = QLabel(_("Options:"))
        option_title.setObjectName("usersubtitle")
        host_notif_layout.addWidget(option_title, 4, 0, 1, 2)
        host_notif_layout.setAlignment(option_title, Qt.AlignCenter)

        option_widget = self.get_options_widget(
            'host',
            data_manager.database['user'].data['host_notification_options']
        )
        host_notif_layout.addWidget(option_widget, 5, 0, 1, 2)

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
        notif_title.setObjectName("usertitle")
        service_notif_layout.addWidget(notif_title, 0, 0, 1, 2)

        state_title = QLabel(_("State:"))
        state_title.setObjectName("usersubtitle")
        service_notif_layout.addWidget(state_title, 1, 0, 1, 1)
        self.service_notif_state = QCheckBox()
        self.service_notif_state.setObjectName('serviceactions')
        self.service_notif_state.setChecked(
            data_manager.database['user'].data['service_notifications_enabled']
        )
        self.service_notif_state.stateChanged.connect(self.enable_notifications)
        self.service_notif_state.checkState()
        self.service_notif_state.setFixedSize(18, 18)
        service_notif_layout.addWidget(self.service_notif_state, 1, 1, 1, 1)

        enable_title = QLabel(_("Notification enabled:"))
        enable_title.setObjectName("usersubtitle")
        enable_title.setMinimumHeight(32)
        service_notif_layout.addWidget(enable_title, 2, 0, 1, 1)
        self.labels['service_notification_enabled'].setPixmap(
            self.get_enable_label_icon(
                data_manager.database['user'].data['service_notifications_enabled']
            )
        )
        self.labels['service_notification_enabled'].setFixedSize(18, 18)
        self.labels['service_notification_enabled'].setScaledContents(True)
        service_notif_layout.addWidget(self.labels['service_notification_enabled'], 2, 1, 1, 1)

        period_title = QLabel(_("Notification period:"))
        period_title.setObjectName("usersubtitle")
        service_notif_layout.addWidget(period_title, 3, 0, 1, 1)
        period = User.get_period_name(
            data_manager.database['user'].data['service_notification_period']
        )
        self.labels['service_notification_period'].setText(period.capitalize())
        service_notif_layout.addWidget(self.labels['service_notification_period'], 3, 1, 1, 1
        )

        option_title = QLabel(_("Options:"))
        option_title.setObjectName("usersubtitle")
        service_notif_layout.addWidget(option_title, 4, 0, 1, 2)
        service_notif_layout.setAlignment(option_title, Qt.AlignCenter)

        option_widget = self.get_options_widget(
            'service',
            data_manager.database['user'].data['service_notification_options']
        )
        service_notif_layout.addWidget(option_widget, 5, 0, 1, 2)

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
            # check_btn.checkState() is equal to 0 or 2
            notification_enabled = True if check_btn.checkState() else False
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
                events_widget.add_event('OK', message)
            else:
                events_widget.add_event('ERROR', _("Backend PATCH failed, please check your logs !"))

        self.update_widget()

    def get_options_widget(self, item_type, options):
        """
        Create and return QWidget with options and their icons

        :param item_type: define item type for options: host or service
        :type item_type: str
        :param options: list of notification options
        :type options: list
        :return: QWidget with options and icons
        :rtype: QWidget
        """

        items_options = {
            'host': ['d', 'u', 'r', 'f', 's', 'n'],
            'service': ['w', 'u', 'c', 'r', 'f', 's', 'n']
        }

        available_options = items_options[item_type]

        selected_options = {}
        for opt in available_options:
            selected_options[opt] = bool(opt in options)

        option_names = {
            'host': {
                'd': 'DOWN',
                'u': 'UNREACHABLE',
                'r': 'RECOVERY',
                'f': 'FLAPPING',
                's': 'DOWNTIME',
                'n': 'NONE'
            },
            'service': {
                'w': 'WARNING',
                'u': 'UNKNOWN',
                'c': 'CRITICAL',
                'r': 'RECOVERY',
                'f': 'FLAPPING',
                's': 'DOWNTIME',
                'n': 'NONE'
            }
        }

        line = 0
        options_widget = QWidget()
        options_layout = QGridLayout()
        options_widget.setLayout(options_layout)
        for opt in selected_options:
            # Name of Option
            option_label = QLabel(option_names[item_type][opt])
            object_name = 'user' + str(selected_options[opt])
            option_label.setObjectName(object_name)
            options_layout.addWidget(option_label, line, 0, 1, 1)
            # Corresponding icon
            self.opt_labels[item_type][opt] = QLabel()
            self.opt_labels[item_type][opt].setPixmap(
                self.get_enable_label_icon(selected_options[opt])
            )
            self.opt_labels[item_type][opt].setFixedSize(14, 14)
            self.opt_labels[item_type][opt].setScaledContents(True)
            options_layout.addWidget(self.opt_labels[item_type][opt], line, 1, 1, 1)
            line += 1

        return options_widget

    def update_widget(self):
        """
        Update UserQWidget

        """

        # Realm, Role, Email
        self.labels['realm'].setText(User.get_realm_name())
        self.labels['role'].setText(User.get_role().capitalize())
        self.labels['email'].setText(data_manager.database['user'].data['email'])

        # Admin, Commands
        self.labels['is_admin'].setPixmap(
            self.get_enable_label_icon(data_manager.database['user'].data['is_admin'])
        )
        self.labels['can_submit_commands'].setPixmap(
            self.get_enable_label_icon(data_manager.database['user'].data['can_submit_commands'])
        )

        # Alias, Notes, Token
        self.labels['alias'].setText(data_manager.database['user'].data['alias'])
        self.labels['notes'].setText(data_manager.database['user'].data['notes'])
        if data_manager.database['user'].data['is_admin']:
            self.labels['token'].setText(data_manager.database['user'].data['token'])

        # Notifications
        self.labels['host_notifications_enabled'].setPixmap(
            self.get_enable_label_icon(
                data_manager.database['user'].data['host_notifications_enabled']
            )
        )
        period = User.get_period_name(
            data_manager.database['user'].data['host_notification_period']
        )
        self.labels['host_notification_period'].setText(period.capitalize())

        self.labels['service_notification_enabled'].setPixmap(
            self.get_enable_label_icon(
                data_manager.database['user'].data['service_notifications_enabled']
            )
        )
        period = User.get_period_name(
            data_manager.database['user'].data['service_notification_period']
        )
        self.labels['service_notification_period'].setText(period.capitalize())

        items_options = {
            'host': ['d', 'u', 'r', 'f', 's', 'n'],
            'service': ['w', 'u', 'c', 'r', 'f', 's', 'n']
        }

        for item_type in self.opt_labels:
            if item_type == 'host':
                options = data_manager.database['user'].data['host_notification_options']
            else:
                options = data_manager.database['user'].data['service_notification_options']

            available_options = items_options[item_type]

            selected_options = {}
            for opt in available_options:
                selected_options[opt] = bool(opt in options)
                self.opt_labels[item_type][opt].setPixmap(
                    self.get_enable_label_icon(selected_options[opt])
                )

    @staticmethod
    def get_enable_label_icon(state):
        """
        Return red crosse or green check QPixmap in QLabel, depending state is True of False

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

        enable_pixmap = QPixmap(get_image_path(states[state]))

        return enable_pixmap


# Initialize user_widget object
user_widget = UserQWidget()
user_widget.initialize()
