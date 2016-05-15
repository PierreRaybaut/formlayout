# -*- coding: utf-8 -*-
#
# Copyright © 2009 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see formlayout.py for details)

"""
Simple formlayout example

Please take a look at formlayout.py for more examples
(at the end of the script, after the 'if __name__ == "__main__":' line)
"""

from formlayout import fedit

datalist = [('Name', 'Paul'),
            (None, 'Qt.jpg'),
            (None, None),
            (None, 'Information:'),
            ('Password', 'password'),
            ('Age', 30),
            ('Sex', [0, 'Male', 'Female']),
            ('Size', 12.1),
            ('Eyes', 'green'),
            ('Married', True),
            ]

print("result:", fedit(datalist, title="Describe yourself",
                       comment="This is just an <b>example</b>."))
