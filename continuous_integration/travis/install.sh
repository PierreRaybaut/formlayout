#!/usr/bin/env bash

set -ex

PY_VERSION=$TRAVIS_PYTHON_VERSION

#==============================================================================
# Utility functions
#==============================================================================

install_conda()
{
  # Define the miniconda name to download
    if [ "$TRAVIS_OS_NAME" = "linux" ]; then
        MINICONDA_OS=$MINICONDA_LINUX;
    elif [ "$TRAVIS_OS_NAME" = "osx" ]; then
        MINICONDA_OS=$MINICONDA_OSX;
    fi

    wget "http://repo.continuum.io/miniconda/Miniconda3-$MINICONDA_VERSION-$MINICONDA_OS.sh" -O miniconda.sh;

    bash miniconda.sh -b -p "$HOME/miniconda";
    export PATH="$HOME/miniconda/bin:$PATH";
    hash -r;
    conda config --set always_yes yes --set changeps1 no;

    # Update conda
    conda update -q conda;

    conda create -q -n test-environment python=$PY_VERSION;
    source activate test-environment

    if [ "$USE_QT_API" = "PyQt5" ]; then
        conda install -c https://conda.anaconda.org/spyder-ide pyqt5
        export QT_API=pyqt5;
    elif [ "$USE_QT_API" = "PyQt4" ]; then
        conda install pyqt;
    elif [ "$USE_QT_API" = "PySide" ]; then
        conda install_pyside;
    fi
}


install_pyside()
{
    # Currently support Python 2.7 and 3.4
    # http://stackoverflow.com/questions/24489588/how-can-i-install-pyside-on-travis

    pip install -U setuptools;
    pip install -U pip;
    pip install --no-index --trusted-host $WHEELHOUSE_URI --find-links=http://$WHEELHOUSE_URI/ pyside;

    # Travis CI servers use virtualenvs, so we need to finish the install by the following
    POSTINSTALL=$(find ~/virtualenv/ -type f -name "pyside_postinstall.py";)
    python $POSTINSTALL -install;
}


install_arial_font()
{
    # The next line is to avoid an interactive prompt asking to accept
    # the EULA license
    echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | sudo debconf-set-selections;
    sudo apt-get install ttf-mscorefonts-installer;
}

#==============================================================================
# Main
#==============================================================================

# Arial is needed to run formlayout.py
install_arial_font;
install_conda;
