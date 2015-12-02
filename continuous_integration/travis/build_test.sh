#!/usr/bin/env bash

set -ex

# Print basic testing info
pip --version

# Moving to where our code is
cd $REP_CLONE

# Checkout the right branch
if [ $TRAVIS_PULL_REQUEST != "false" ] ; then
    git checkout travis_pr_$TRAVIS_PULL_REQUEST
else
    git checkout master
fi

python setup.py bdist_wheel --universal
