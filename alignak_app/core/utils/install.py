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
    Settings manage configurations of Alignak-app
"""

import os
import sys
import subprocess

from logging import getLogger

logger = getLogger(__name__)


def create_user_app_dir(cfg_file):
    """
    Create a user folder for App configuration file and log

    :param cfg_file: file to copy if user has no rights
    :type cfg_file: str
    :return: return original file if user ha right, else the new file created
    :rtype: str
    """

    if not os.access(cfg_file, os.W_OK):
        # Create Folder for user if does not exist
        user_app_dir = '%s/.local/alignak_app' % os.environ['HOME']
        if not os.path.exists(user_app_dir):
            try:
                os.makedirs(user_app_dir)
            except (PermissionError, FileExistsError) as e:
                print(e)
                sys.exit('Can\'t create App directory for user in [%s] !' % user_app_dir)

        dest_file = os.path.join(user_app_dir, os.path.split(cfg_file)[1])
        # If file does not exist, App create it
        if not os.path.isfile(dest_file):
            creation = subprocess.run(
                ['cp', cfg_file, dest_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            try:
                assert creation.returncode == 0
            except AssertionError:
                print("Copy of user configuration file: ", creation.stdout.decode('UTF-8'))

        return dest_file
    else:
        # If the file exists, App add a sample file
        if not os.path.isfile(cfg_file + '.sample'):
            creation = subprocess.run(
                ['cp', cfg_file, cfg_file + '.sample'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            try:
                assert creation.returncode == 0
            except AssertionError:
                print("User folder creation: ", creation.stdout.decode('UTF-8'))

        return cfg_file
