# -*- coding: utf-8 -*-
#
# Copyright © 2009 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see formlayout.py for details)

"""
Tree examples
"""

from formlayout import fedit

datalist = [('dict:', {"Name": "QuickForm",
                       "Authors":
                         {"french" : [u"Pièrre", u"Flôrent"],
                          "english" : [
                              {"Brit" : ["John", "Andrew"]},
                              {"US"   : [
                                         "Tim",
                                         {"William" : ["Will","Bill"]}
                                        ]
                              }
                           ]
                         },
                       "Python": ["2", "3"]
                       }),
            (None, 'JSON tree:'),
            (None, u'Treè vîew_Node content.json'),
            (None, 'XML tree:'),
            (None, u'Treè vîew.xml')
            ]

print('result:', fedit(datalist, title='Tree examples', type='questions'))
