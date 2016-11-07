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
