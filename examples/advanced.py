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

import datetime
# for normal usage
from formlayout import fedit
# for programming usage
from formlayout import QLineEdit

def create_datalist_example():
    test = [('str *', 'this is a string'),
            ('str_m *', """this is a 
             MULTILINE
             string"""),
            ('file *', 'file'),
            ('list *', [0, '1', '3', '4']),
            ('tuple *', (0, '1', '3', '4')),
            ('list2', ['--', ('none', 'None'), ('--', 'Dashed'),
                       ('-.', 'DashDot'), ('-', 'Solid'),
                       ('steps', 'Steps'), (':', 'Dotted')]),
            ('float', 1.2),
            (None, [('fi&rst', first_function), ('s&econd', second_function)]),
            (None, 'Other:'),
            ('slider to 30 at 20 with ticks', 'slider:30:@20'),
            ('slider from -100 to 50 at -10', 'slider:-100:50@-10'),
            ('int', 12),
            ('font', ('Arial', 10, False, True)),
            ('color', '#123409'),
            ('bool', True),
            ('date', datetime.date(2010, 10, 10)),
            ('time', datetime.time(12, 30)),
            ('datetime', datetime.datetime(2010, 10, 10)),
            ]
    return test
    
def create_combogroup_example():
    datalist = create_datalist_example()
    return [(datalist, "Category 1", "Category 1 comment"),
            (datalist, "Category 2", "Category 2 comment"),
            (datalist, "Category 3", "Category 3 comment")]

def create_tabgroup_example():
    datalist = create_datalist_example()
    return ((datalist, "Title 1", "Title 1 comment"),
            (datalist, "Title 2", "Title 2 comment"),
            (datalist, "Title 3", "Title 3 comment"))

def apply_function(result, widgets):
    print('result:', result)
    print('widgets:', widgets)
    for widget in widgets:
        if isinstance(widget, QLineEdit) and not widget.validator():
            widget.setText(widget.text() + ' Apply !')

def first_function(result, widgets):
    print('first')
    print('result:', result)
    print('widgets:', widgets)
    for widget in widgets:
        if isinstance(widget, QLineEdit) and not widget.validator():
            widget.setText(widget.text() + ' First !')

def second_function(result, widgets):
    print('second')
    print('result:', result)
    print('widgets:', widgets)
    for widget in widgets:
        if isinstance(widget, QLineEdit) and not widget.validator():
            widget.setText(widget.text() + ' Second !')

#--------- datalist example
datalist = create_datalist_example()
print("result:", fedit(datalist, title="Example",
                       comment="This is just an <b>example</b>.",
                       apply=('Custom &Apply button', apply_function),
                       ok='Custom &OK button',
                       cancel='Custom &Cancel button',
                       result='dict',
                       type='questions',
                       scrollbar=True))

#--------- datagroup examples
datagroup = create_combogroup_example()
print("result:", fedit(datagroup, "Global title", result='JSON'))

datagroup = create_tabgroup_example()
print("result:", fedit(datagroup, "Global title", result='JSON'))

#--------- datagroup inside a datagroup examples
datalist = create_datalist_example()
datagroup = create_tabgroup_example()
print("result:", fedit([(datagroup, "Category 1", "Category 1 comment"),
                        (datalist, "Category 2", "Category 2 comment"),
                        (datalist, "Category 3", "Category 3 comment")],
                        "Global title", result='XML'))

datalist = create_datalist_example()
datagroup = create_combogroup_example()
print("result:", fedit(((datagroup, "Title 1", "Tab 1 comment"),
                        (datalist, "Title 2", "Tab 2 comment"),
                        (datalist, "Title 3", "Tab 3 comment")),
                        "Global title", result='XML'))

datalist = create_datalist_example()
datagroup = create_combogroup_example()
print("result:", fedit([(datagroup, "Category 1", "Category 1 comment"),
                        (datalist, "Category 2", "Category 2 comment"),
                        (datalist, "Category 3", "Category 3 comment")],
                        "Global title", result='XML'))

datalist = create_datalist_example()
datagroup = create_tabgroup_example()
print("result:", fedit(((datagroup, "Title 1", "Tab 1 comment"),
                        (datalist, "Title 2", "Tab 2 comment"),
                        (datalist, "Title 3", "Tab 3 comment")),
                        "Global title", result='XML'))

datalist = create_datalist_example()
datagroup = create_tabgroup_example()
print("result:", fedit((([(datagroup, "Category 1", "Category 1 comment"),
                          (datalist, "Category 2", "Category 2 comment"),
                          (datalist, "Category 3", "Category 3 comment")],
                          "Three", "Three levels"),
                        (datagroup, "Two", "Two levels"),
                        (datalist, "One", "One level")),
                        "Global title", result='XML'))
