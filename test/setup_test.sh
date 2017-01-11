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

# install dependencies
echo ' --------- Update and Install packages ... --------- '
sudo apt-get update
sudo apt-get install -qq libegl1-mesa

echo '--------- Upgrade pip ... --------- '
pip install --upgrade pip

# install prog AND tests requirements :
echo '--------- Installing application requirements ... --------- '
pip install -r requirements.txt

echo '--------- Installing application in development mode ... --------- '
pip install -e .

echo '--------- Installing tests requirements ... --------- '
pip install --upgrade -r test/requirements.txt

PYVERSION=$(python -c "import sys; print(''.join(map(str, sys.version_info[:1])))")
if [[ "3" == "$PYVERSION" ]] ; then
    pip install PyQt5
else
    sudo apt-get install python-qt4
fi

echo '--------- Check and copy folder data to home... --------- '
mkdir -p ~/.local/alignak_app/images/
mkdir -p ~/.local/alignak_app/templates/
cp -R --verbose etc/images/* ~/.local/alignak_app/images/
cp -R --verbose etc/css/* ~/.local/alignak_app/css/
cp -R --verbose etc/templates/* ~/.local/alignak_app/templates/
cp --verbose test/etc/settings.cfg ~/.local/alignak_app/
