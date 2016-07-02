#!/usr/bin/env bash
#

set -e

THIS_PATH=$(dirname "$0")
BASE_PATH=$(dirname "$THIS_PATH")

cd $BASE_PATH

echo 'Upgrade pip ...'
pip install --upgrade pip

# install prog AND tests requirements :
echo 'Installing application requirements ...'
pip install -r requirements.txt
echo 'Installing application in development mode ...'
pip install -e .
echo 'Installing tests requirements ...'
pip install --upgrade -r test/requirements.txt
