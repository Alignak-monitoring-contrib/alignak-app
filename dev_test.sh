#!/bin/bash
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

# HELP ################################################################
#                                                                     #
# Change the VAR to adapt script to your lib                          #
#                                                                     #
#######################################################################


# SCRIPT VARS #########################################################

# Library

LIB_NAME=alignak_app
LIB_ROOT=$HOME/.local/$LIB_NAME

CMD_BEFORE="cp test/etc/settings.cfg $LIB_ROOT/settings.cfg"
CMD_LIB="~/.local/$LIB_NAME/bin/launch"

# Folders

WORKSPACE=$HOME/workspace/repos/alignak-app
TEST_FOLDER="test/test_*.py"

# Python 2

PY2=false
TEST_PY2=$PY2

CMD_TEST_PY2=~/.local/bin/nosetests
TEST_ARGS_PY2="-xv --nologcapture --with-coverage --cover-package=$LIB_NAME"

# Python 3

PY3=false
TEST_PY2=$PY3

CMD_TEST_PY3=~/.local/bin/nosetests-3.4
TEST_ARGS_PY3="-xv --nologcapture --with-coverage --cover-package=$LIB_NAME"


# FUNCTIONS ############################################################


function install_app {
    echo "---------------- Install $LIB_NAME -----------------"
    if [ $1 = "py2" ]; then
        echo "------------------ for Python 2 ---------------------"
        pip install . --user --upgrade
    else
        echo "------------------ for Python 3 ---------------------"
        pip3 install . --user --upgrade
    fi
}

function reinstall_app {
    echo "-------------- Uninstall $LIB_NAME -----------------"
    if [ $1 = "py2" ]; then
        pip uninstall -y $LIB_NAME
    else
        pip3 uninstall -y $LIB_NAME
    fi
    install_app $1
}

function test_app {
    echo "-------------- Test $LIB_NAME -----------------"
    if [ $1 = "py2" ]; then
	$CMD_TEST_PY2 $TEST_ARGS_PY2 $TEST_FOLDER
    else
        $CMD_TEST_PY3 $TEST_ARGS_PY3 $TEST_FOLDER
    fi
}


# BEGIN ################################################################

echo "------------- Go to $WORKSPACE ---------------"
cd $WORKSPACE

install_app $1

$CMD_BEFORE

test_app $1

$CMD_LIB
