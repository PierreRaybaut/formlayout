#!/usr/bin/env bash

set -ex

# Print basic testing info
pip --version

cd $HOME/builds/PierreRaybaut/formlayout

# Checkout the right branch
if [ $TRAVIS_PULL_REQUEST != "false" ] ; then
    git checkout travis_pr_$TRAVIS_PULL_REQUEST
else
    git checkout master
fi

python setup.py sdist bdist_wheel --universal
python setup.py build sdist
