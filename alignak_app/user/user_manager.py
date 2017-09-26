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
    UserManager manage QWidget who display User Profile.
"""

from logging import getLogger

from alignak_app.user.user_profile import UserProfile

logger = getLogger(__name__)


class UserManager(object):
    """
        User manage the UserProfile QWidget creation
    """

    def __init__(self, app_backend):
        self.app_backend = app_backend
        self.user_widget = None

    def create_user_profile(self):
        """
        Create the USerProfile QWidget. Store old informations if needed.

        """

        logger.info("Create UserProfile")

        old_pos = None
        if self.user_widget:  # pragma: no cover
            logger.debug("Delete old UserProfile")
            if self.user_widget.app_widget:
                old_pos = self.user_widget.app_widget.pos()
            self.user_widget.deleteLater()
            self.user_widget = None

        self.user_widget = UserProfile(self.app_backend)
        self.user_widget.initialize()

        if old_pos:
            self.user_widget.app_widget.move(old_pos)

        self.user_widget.update_profile.connect(self.user_widget.create_widget)

    def show_user_widget(self):
        """
        Destroy and create the UserProfile, then show it

        """

        self.create_user_profile()
        self.user_widget.app_widget.show()
