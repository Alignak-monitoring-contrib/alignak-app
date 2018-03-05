#!/usr/bin/env bash

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

set -e

THIS_PATH=$(dirname "$0")
BASE_PATH=$(dirname "$THIS_PATH")

cd $BASE_PATH

echo '--------- Upgrade pip ... --------- '
pip install --upgrade pip

echo '--------- Installing application requirements ... --------- '
pip install -r requirements.txt

echo '--------- Installing application in development mode ... --------- '
pip install -e .

echo '--------- Installing tests requirements ... --------- '
pip install --upgrade -r test/requirements.txt

echo '--------- Check and copy folder data to home... --------- '
mkdir -p ~/.local/alignak_app/images/
mkdir -p ~/.local/alignak_app/css/
mkdir -p ~/.local/alignak_app/bin/
mkdir -p ~/.local/alignak_app/bin-samples/
cp -R --verbose etc/images/* ~/.local/alignak_app/images/
cp -R --verbose etc/css/* ~/.local/alignak_app/css/
cp -R --verbose test/etc/* ~/.local/alignak_app/
cp --verbose bin/unix/alignak-app.py ~/.local/alignak_app/bin/
cp --verbose bin/unix/alignak-app.sample.sh ~/.local/alignak_app/bin-samples/
cp --verbose bin/unix/alignak-app-auto.sample.sh ~/.local/alignak_app/bin-samples/
