#!/usr/bin/env bash

set -ex

# Tell Spyder we're testing our widgets in Travis
export TEST_CI_WIDGETS=True

# Checkout the right branch
cd $REP_CLONE

python simple.py
python formlayout.py
