#!/usr/bin/env bash

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

set -e

THIS_PATH=$(dirname "$0")
BASE_PATH=$(dirname "$THIS_PATH")

cd $BASE_PATH

echo '--------- Upgrade pip ... --------- '
pip install --upgrade pip

# install prog AND tests requirements :
echo '--------- Installing application requirements ... --------- '
pip install -r requirements.txt
echo '--------- Locate missing library ... --------- '
sudo updatedb
locate xcb
echo $PATH
PATH=$PATH:~/virtualenv/python3.5.2/lib/python3.5/site-packages/PyQt5/Qt/plugins/platforms/
echo '--------- Installing application in development mode ... --------- '
pip install -e .
echo '--------- Installing tests requirements ... --------- '
pip install --upgrade -r test/requirements.txt
