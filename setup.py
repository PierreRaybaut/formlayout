# -*- coding: utf-8 -*-
#
# Copyright © 2009-2015 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see formlayout.py for details)

"""
formlayout
==========

Python module providing the most easy way to create Qt form dialogs and widgets
(compatible with Python 2, Python 3, PyQt4, PyQt5 and PySide).

Copyright © 2009-2016 Pierre Raybaut
This software is licensed under the terms of the MIT license
"""

from formlayout import __version__
LIBNAME = 'formlayout'

import setuptools  # analysis:ignore
from distutils.core import setup

CLASSIFIERS = []
if 'beta' in version or 'b' in version:
    CLASSIFIERS += ['Development Status :: 4 - Beta']
elif 'alpha' in version or 'a' in version or version.startswith('0.'):
    CLASSIFIERS += ['Development Status :: 3 - Alpha']
else:
    CLASSIFIERS += ['Development Status :: 5 - Production/Stable']

setup(name = LIBNAME,
      version = __version__,
      description = 'The most easy way to create Qt form dialogs and widgets with Python',
      long_description = """\
.. image:: https://pythonhosted.org/formlayout/_images/advanced1.png
.. image:: https://pythonhosted.org/formlayout/_images/advanced2.png
.. image:: https://pythonhosted.org/formlayout/_images/advanced3.png

With ``formlayout``, generating a form is very easy:
  * To show a dialog box, just call the ``fedit`` function.
  * To set-up the form dialog, simply use lists to pass parameters (field names, default values, ...).
  * To embedd ``formlayout`` in your own library, just copy the ``formlayout`` autoconsistent single script (*zero dependency*, except Qt itself).

Here is a simple example (more are included in source package)::

    from formlayout import fedit
    datalist = [('Name', 'Paul'),
                (None, None),
                (None, 'Information:'),
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
      classifiers=CLASSIFIERS + [
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Widget Sets',
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
