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

# Python 2

PIP_PY2="pip"
ARGS_PIP_PY2="--user"

CMD_TEST_PY2=~/.local/bin/nosetests
TEST_ARGS_PY2="-xv --nologcapture --with-coverage --cover-package=${LIB_NAME}"

# Python 3

PIP_PY3="pip3"
ARGS_PIP_PY3="--user"

CMD_TEST_PY3=~/.local/bin/nosetests-3.4
TEST_ARGS_PY3="-xv --nologcapture --with-coverage --cover-package=${LIB_NAME}"


# INFO ################################################################
#                                                                     #
# FUNCTIONS                                                           #
#                                                                     #
#######################################################################

function step_msg {
    echo -e "
---------------------> [ $1 ]..."
}

function go_to_dir {
    step_msg  "CD $WORKSPACE"
    cd "$WORKSPACE"
}

function uninstall_lib {
    # Uninstall library
    if [ "$1" -eq 2 ]; then
        sh -c "$PIP_PY2 uninstall -y $LIB_NAME"
    else
        sh -c "$PIP_PY3 uninstall -y $LIB_NAME"
    fi
}

function install_lib {
    # Install or upgrade library
    if [ ! -z "$2" ]; then
        flag="$2"
    else
        flag=""
    fi

    if [ "$1" -eq 2 ]; then
        sh -c "$PIP_PY2 install . $ARGS_PIP_PY2 $flag"
    else
        sh -c "$PIP_PY3 install . $ARGS_PIP_PY3 $flag"
    fi
}

function test_app {
    # Launch unit tests

    if [ $1 = "py2" ]; then
	    sh -c "$CMD_TEST_PY2 $TEST_ARGS_PY2 $TEST_FOLDER"
    else
        sh -c "$CMD_TEST_PY3 $TEST_ARGS_PY3 $TEST_FOLDER"
    fi
}

function choose_step {
    # Choose between the function.
    if [ "$2" = "upgrade" ]; then
        go_to_dir
        step_msg "UPGRADE"
        install_lib $1 "--$2"
    elif [ "$2" = "remove" ]; then
        step_msg "UNINSTALL"
        uninstall_lib $1
    elif [ "$2" = "test" ]; then
        step_msg  "RUN UNIT TESTS"
        test_app $1
    else
        go_to_dir
        step_msg "INSTALLATION"
        install_lib $1
    fi
}


# INFO ################################################################
#                                                                     #
# BEGINNING OF THE SCRIPT                                             #
#                                                                     #
#######################################################################

usage="$(basename "$0") [-h] [-p n] [-c command] -- script to test and install python libraries.

-h  show this help text.
-p  [2|3] choose between python 2 or 3. [2] is default !
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
    p)
        py=$OPTARG
        ;;
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

# Launch functions
if [ -z "$py" ]; then
    py=2
fi

step_msg "CONFIG"
echo "Python version : $py"
echo "Command : $cmd"

choose_step "$py" "$cmd"

if [ "$cmd" != "remove" -a "$cmd" != "test" ]; then
    step_msg "RUN COMMAND AFTER"
    sh -c "$CMD_AFTER"
fi
if [ "$cmd" = "start" ]; then
    step_msg  "LAUNCH $LIB_NAME"
    sh -c "$CMD_LIB"
fi
