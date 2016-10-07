#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016:
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
    Launch is launching Alignak-app.
"""

import os
import sys

from logging import getLogger
from alignak_app.application import AlignakApp as App


logger = getLogger(__name__)


def launch():
    """
        Check environment and launch Alignak-App.
    """

    # Actually, we must verify we are in DESKTOP_SESSION or not
    try:
        os.environ['DESKTOP_SESSION']
    except KeyError as e:
        logger.critical('You must be in desktop session to launch Alignak-App : ' + str(e))
        sys.exit()

    App().run()

if __name__ == "__main__":
    launch()
