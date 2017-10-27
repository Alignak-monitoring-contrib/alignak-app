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
    Application logs
"""

import os
from logging import DEBUG
from logging import Formatter
from logging import getLogger
from logging.handlers import TimedRotatingFileHandler

from alignak_app.core.utils.config import get_app_workdir, get_app_config


# Application Logger
def create_logger():  # pragma: no cover
    """
    Create the logger for Alignak-App

    """

    root_logger = getLogger()

    stdout_handler = None

    if root_logger.handlers:
        stdout_handler = root_logger.handlers[0]

    # Define path and file for "file_handler"
    path = get_app_workdir()
    filename = '%s.log' % get_app_config('Log', 'filename')

    if not os.path.isdir(path):
        # noinspection PyBroadException
        try:  # pragma: no cover - not testable
            os.makedirs(path)
        except Exception:
            print('Can\'t create log file in [%s], App will log in current directory !' % path)
            path = '.'

    if not os.access(path, os.W_OK):
        print('Access denied for [%s], App will log in current directory !' % path)
        path = '.'

    formatter = Formatter('[%(asctime)s]> %(name)-12s : [%(levelname)s] %(message)s')

    # Create "file_handler"
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(path, filename),
        when="D",
        interval=1,
        backupCount=6
    )

    file_handler.setLevel(DEBUG)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)

    # Remove stdout handler to ensure logs are only in filehandler
    root_logger.removeHandler(stdout_handler)

    return root_logger
