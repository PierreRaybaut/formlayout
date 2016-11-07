=======
Widgets
=======

Separator
=========

The label and the value must be ``None``.

label: ``None``
value: ``None``

.. image:: /images/separator.png

Text
====

The label must be ``None`` and the value can be any string.

label: ``None``
value: ``Some text``

.. image:: /images/text.png

The text can be formatted.

label: ``None``
value: ``Some <b><font color="red">red bold</font></b> text``

.. image:: /images/text_red_bold.png

Push button
===========

The label must be ``None`` and the value a list or a tuple of binomials.
The first element is the button label, the second is the callback function.

label: ``None``
value: ``[('Push !', push_function)]``

.. image:: /images/push_button.png

The ``&`` char can be used to specify a keyboard shortcut.

label: ``None``
value: ``[('fi&rst', first_function), ('s&econd', second_function)]``

.. image:: /images/push_button_multiple.png

Line edit
=========

Empty line edit
---------------

The value must be an empty string.

label: ``'Name'``
value: ``''``

.. image:: /images/line_edit_empty.png

Line edit with default content
------------------------------

The value can be any string excluding reserved strings.

label: ``'Name'``
value: ``'Florent'``

.. image:: /images/line_edit_default.png
 
Line edit for password
----------------------

The value must be the string ``password``.

label: ``'Password'``
value: ``'password'``

Before typing:

.. image:: /images/line_edit_password_before.png

After typing:

.. image:: /images/line_edit_password_after.png

Text edit
=========

Empty text edit
---------------

The value must be the string ``\n``.

label: ``'Motivation'``
value: ``'\n'``

.. image:: /images/text_edit_empty.png

Text edit with default content
------------------------------

The value can be any string with at least one ``\n`` inside.

label: ``'Name'``
value: ``'This is why\n'``

.. image:: /images/text_edit_default.png

Checkbox
========

Single checkbox
---------------

The value must be ``True`` or ``False``.

label: ``'False'``
value: ``False``

.. image:: /images/checkbox_false.png

label: ``'True'``
value: ``True``

.. image:: /images/checkbox_true.png

Multiple checkbox
-----------------

The value must be a list or a tuple of strings whose the first element is a bit string.

label: ``'Fruits'``
value: ``['0b101', 'Apple', 'Orange', 'Banana']``

.. image:: /images/checkbox_multiple.png

Radio buttons
=============

The value must be a tuple of strings whose the first element is an integer.

Empty radio buttons
-------------------

The index must be ``0``.

label: ``'Fruit'``
value: ``(0, 'Apple', 'Orange', 'Banana')``

.. image:: /images/radio_buttons_empty.png

Radio buttons with default choice
---------------------------------

The index must be the one of the chosen item.

label: ``'Fruit'``
value: ``(2, 'Apple', 'Orange', 'Banana')``

.. image:: /images/radio_buttons_default.png

Combobox
========

The value must be a list of strings whose the first element is an integer.

Empty combobox
--------------

The index must be ``0``.

label: ``'Fruit'``
value: ``[0, 'Apple', 'Orange', 'Banana']``

.. image:: /images/combobox_empty.png

Combobox with default choice
----------------------------

The index must be the one of the chosen item.

label: ``'Fruit'``
value: ``[2, 'Apple', 'Orange', 'Banana']``

.. image:: /images/combobox_default.png
