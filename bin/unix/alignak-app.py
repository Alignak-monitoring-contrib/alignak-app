#!/usr/bin/env python
# -*- codinf: utf-8 -*-

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
    Launch Alignak-app
"""

import sys
import os

from alignak_app.app import AlignakApp

from PyQt5.QtWidgets import QApplication


if 'win32' not in sys.platform:
    if 'SSH_CONNECTION' in os.environ:
        if os.name == 'posix':
            FAIL = '\033[91m'
            ENDC = '\033[0m'
        else:
            FAIL = '# ! #\n'
            ENDC = '\n# ! #'
        sys.exit(
            '%sAlignak-app can not be launched during an SSH connection '
            'and requires an X server to be displayed.%s' % (FAIL, ENDC)
        )

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

alignak_app = AlignakApp(app)
alignak_app.start()

sys.exit(app.exec_())
