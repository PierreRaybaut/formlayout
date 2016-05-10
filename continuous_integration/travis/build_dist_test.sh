#!/usr/bin/env bash

set -ex

# Print basic testing info
pip --version

cd $HOME/build/PierreRaybaut/formlayout

# Is the following really necessary?
## Checkout the right branch
#if [ $TRAVIS_PULL_REQUEST != "false" ] ; then
#    git checkout travis_pr_$TRAVIS_PULL_REQUEST
#else
#    git checkout master
#fi

# Wheel build is causing a segfault when using PyQt4!?
## Building universal wheel package
# python setup.py sdist bdist_wheel --universal

# Building Python source package
python setup.py build sdist
