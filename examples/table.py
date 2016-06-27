# -*- coding: utf-8 -*-
#
# Copyright © 2009 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see formlayout.py for details)

"""
Table examples
"""

from formlayout import fedit

datalist = [('list of lists:', [[u'Pièrre', 35, 'Paris'],
                                [u'Flôrent', 34, 'Paris'],
                                [u'Loïc', 36, 'Paris']]),
            ('tuple marks header:', [('Name', 'Age', 'City'),
                                     [u'Pièrre', 35, 'Paris'],
                                     [u'Flôrent', 34, 'Paris'],
                                     [u'Loïc', 36, 'Paris']]),
            (None, 'No header CSV:'),
            (None, 'table.csv'),
            (None, 'Numered headers CSV:'),
            (None, '#table.csv'),
            (None, 'Horizontal header CSV:'),
            (None, '_table.csv'),
            (None, 'Vertical header CSV:'),
            (None, '|tablev.csv'),
            (None, 'Both headers CSV:'),
            (None, '/tablehv.csv'),
            ]

print('result:', fedit(datalist, title='Table examples',
                       type='questions', scrollbar=True))
