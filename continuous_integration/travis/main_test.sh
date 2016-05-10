#!/usr/bin/env bash

set -ex

# Tell formlayout we're testing our widgets in Travis
export TEST_CI_WIDGETS=True

python formlayout.py

for f in examples/*/*.py; do
    python "$f"
    if [ $? -ne 0 ]; then
        exit 1
    fi
done
