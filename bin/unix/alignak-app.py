#!/usr/bin/env python
# -*- codinf: utf-8 -*-

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
    Launch Alignak-app
"""

import sys
import os

from alignak_app.app import AlignakApp

from PyQt5.QtWidgets import QApplication, QMessageBox

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

if 'win32' not in sys.platform:
    try:
        os.environ['DESKTOP_SESSION']
    except KeyError as e:
        print(
            'You must be in [DESKTOP_SESSION] to launch Alignak-App !\n'
            'Try to launch without ssh connection or set your [DESKTOP_SESSION] variable.'
        )
        QMessageBox.critical(
            None,
            'No DESKTOP_SESSION found',
            'You must be in [DESKTOP_SESSION] to launch Alignak-App !\n'
            'Try to launch without ssh connection or set your [DESKTOP_SESSION] variable.'
        )
        sys.exit()

alignak_app = AlignakApp(app)
alignak_app.start()

sys.exit(app.exec_())
