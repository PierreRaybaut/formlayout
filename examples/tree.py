# -*- coding: utf-8 -*-
#
# Copyright © 2009 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see formlayout.py for details)

"""
Tree examples
"""

from formlayout import fedit

datalist = [(None, 'JSON tree:'),
            (None, u'Treè vîew.json'),
            (None, 'XML tree:'),
            (None, u'Treè vîew.xml')
            ]

print("result:", fedit(datalist, title="Tree examples"))
