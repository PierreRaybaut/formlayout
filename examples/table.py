# -*- coding: utf-8 -*-
#
# Copyright © 2009 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see formlayout.py for details)

"""
Table examples
"""

from formlayout import fedit

datalist = [(None, 'No header:'),
            (None, 'table.csv'),
            (None, 'Numered headers:'),
            (None, '#table.csv'),
            (None, 'Horizontal header:'),
            (None, '_table.csv'),
            (None, 'Vertical header:'),
            (None, '|tablev.csv'),
            (None, 'Both headers:'),
            (None, '/tablehv.csv'),
            ]

print("result:", fedit(datalist, title="Table examples"))
