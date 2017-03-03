#!/bin/bash
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

# HELP ################################################################
#                                                                     #
# Change the VAR to adapt script to your library :)                   #
#                                                                     #
#######################################################################


# LIBRARY VARS ########################################################

LIB_NAME=alignak_app
LIB_ROOT="$HOME/.local/$LIB_NAME"

# Additional commands
CMD_AFTER="cp --verbose test/etc/settings.cfg $LIB_ROOT/settings.cfg"
CMD_LIB="~/.local/$LIB_NAME/bin/launch"

# Folders

WORKSPACE=$HOME/workspace/personnal-repos/alignak-app
TEST_FOLDER=test/test_*.py

# PYTHON VARS #########################################################

PIP="pip3"
ARGS_PIP="--user"

CMD_TEST=~/.local/bin/nosetests-3.4
TEST_ARGS="-xv --nologcapture --with-coverage --cover-package=${LIB_NAME}"


# INFO ################################################################
#                                                                     #
# FUNCTIONS                                                           #
#                                                                     #
#######################################################################

function step_msg {
    echo -e "
# $1 ################################################################
"
}

function go_to_dir {
    step_msg  "CD $WORKSPACE"
    cd "$WORKSPACE"
}

function uninstall_lib {
    # Uninstall library
    sh -c "$PIP uninstall -y $LIB_NAME"

}

function install_lib {
    # Install or upgrade library
    if [ ! -z "$1" ]; then
        upgrade="$1"
    else
        upgrade=""
    fi
    echo "------------> $upgrade"
    sh -c "$PIP install . $ARGS_PIP $upgrade"
}

function test_app {
    # Launch unit tests
    sh -c "$CMD_TEST $TEST_ARGS $TEST_FOLDER"
}

function choose_step {
    # Choose between the function.
    if [ "$1" = "upgrade" ]; then
        go_to_dir
        step_msg "UPGRADE"
        install_lib "--$1"
    elif [ "$1" = "remove" ]; then
        step_msg "UNINSTALL"
        uninstall_lib
    elif [ "$1" = "test" ]; then
        step_msg  "RUN UNIT TESTS"
        test_app
    else
        go_to_dir
        step_msg "INSTALLATION"
        install_lib
    fi
}


# INFO ################################################################
#                                                                     #
# BEGINNING OF THE SCRIPT                                             #
#                                                                     #
#######################################################################

usage="$(basename "$0") [-h] [-c command] -- script to test and install python libraries.

-h  show this help text.
-c  choose command to execute:
        - install : install library (default).
        - upgrade : upgrade library.
        - remove  : remove library.
        - test    : test library.
        - start   : install and start library."

# Get args

while getopts 'h:p:c:' opt;
do
    case "$opt" in
    c)
        cmd="$OPTARG"
        if [[ "$cmd" =~ ^(install|upgrade|remove|test|start)$ ]]; then
            continue
        else
            printf "Illegal option: -%s\n" "$OPTARG" >&2
            echo "$usage" >&2
            exit 1
        fi
        ;;
    h)
        echo "$usage"
        exit
        ;;
    \?)
        printf "Illegal option: -%s\n" "$OPTARG" >&2
        echo "$usage" >&2
        exit 1
        ;;
    esac
done


step_msg "CONFIG"
echo "Command : $cmd"

choose_step "$cmd"

if [ "$cmd" != "remove" -a "$cmd" != "test" ]; then
    step_msg "RUN COMMAND AFTER"
    sh -c "$CMD_AFTER"
fi
if [ "$cmd" = "start" ]; then
    step_msg  "LAUNCH $LIB_NAME"
    sh -c "$CMD_LIB"
fi
