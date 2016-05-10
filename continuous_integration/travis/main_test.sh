#!/usr/bin/env bash

set -ex

# Tell formlayout we're testing our widgets in Travis
export TEST_CI_WIDGETS=True

python formlayout.py
python ./examples/simple.py
python ./examples/advanced.py
