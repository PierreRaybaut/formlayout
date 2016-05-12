#!/usr/bin/env bash

set -ex

# Print basic testing info
pip --version

# Building universal wheel package
python setup.py sdist bdist_wheel --universal
  
# Building Python source package
python setup.py build sdist

