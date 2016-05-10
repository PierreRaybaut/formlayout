# -*- coding: utf-8 -*-
#
# Copyright © 2009-2015 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see formlayout.py for details)

"""
formlayout
==========

Module for creating Qt form dialogs, layouts and widgets to edit various type 
of parameters, compatible with PyQt4, PyQt5 and PySide

Copyright © 2009-2015 Pierre Raybaut
This software is licensed under the terms of the MIT license
"""

from formlayout import __version__
LIBNAME = 'formlayout'

import setuptools  # analysis:ignore
from distutils.core import setup

setup(name = LIBNAME,
      version = __version__,
      description = 'Python module for creating Qt form dialogs and widgets',
      long_description = """\
With ``formlayout``, generating a form is very easy.

Here is a simple example (more are included in source package)::

    from formlayout import fedit
    datalist = [('Name', 'Paul'),
                ('Age', 30),
                ('Sex', [0, 'Male', 'Female']),
                ('Size', 12.1),
                ('Eyes', 'green'),
                ('Married', True),
                ]
    fedit(datalist, title="Describe yourself", comment="This is just an <b>example</b>.")

This shows the following dialog box:

.. image:: https://pythonhosted.org/formlayout/_images/simple.png
""",
      author = "Pierre Raybaut",
      author_email = 'pierre.raybaut@gmail.com',
      url = 'https://github.com/PierreRaybaut/%s' % LIBNAME,
      license = 'MIT',
      keywords = 'PyQt4 PyQt5 PySide GUI',
      platforms = ['any'],
      py_modules = ['formlayout'],
      package_data = {},
      classifiers = ['Development Status :: 5 - Production/Stable',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: MacOS',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: OS Independent',
                     'Operating System :: POSIX',
                     'Operating System :: Unix',
                     'Programming Language :: Python :: 2.6',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3',
        ],
    )
