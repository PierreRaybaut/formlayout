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

# Somehow, building the package is segfaulting when using PyQt4.
# Here is the corresponding Travis log:
#   [...]
#   Writing formlayout-2.0.0a0/setup.cfg
#   creating dist
#   Creating tar archive
#   ./continuous_integration/travis/build_dist_test.sh: line 23:  4944 Segmentation fault      (core dumped) python setup.py build sdist
if [ "$USE_QT_API" = "PyQt5" ]; then
  # Building universal wheel package
  python setup.py sdist bdist_wheel --universal
  
  # Building Python source package
  python setup.py build sdist
fi
