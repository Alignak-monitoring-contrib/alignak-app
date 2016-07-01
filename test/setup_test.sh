#!/usr/bin/env bash

set -e

THIS_PATH=$(dirname "$0")
BASE_PATH=$(dirname "$THIS_PATH")

cd $BASE_PATH

#pip install --upgrade pip

# install prog AND tests requirements :
pip3 install -r requirements.txt
pip2.7 install -r requirements2.7.txt
#pip install -e .
pip3 install --upgrade -r test/requirements.txt

#pyversion=$(python -c "import sys; print(''.join(map(str, sys.version_info[:2])))")
#if test -e "test/requirements.py${pyversion}.txt"
#then
#    pip install -r "test/requirements.py${pyversion}.txt"
#fi
