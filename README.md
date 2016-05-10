# formlayout
Python module for creating Qt form dialogs and widgets

See [documentation](http://pythonhosted.org/formlayout/) for more details 
(mostly examples) on the library and [changelog](CHANGELOG.md) for recent 
history of changes.

## Overview

Graphical user interface (GUI) libraries are usually designed to address issues 
that are far more complex than a simple dialog box. As a consequence, generating 
simple GUI like form layouts or dialogs is generally not as easy as it should be: 
the feature-line count ratio is very low for the most simple dialog boxes. 
That's where ``formlayout`` can be useful, by providing a simplistic API (a 
single function ``fedit`` taking lists as parameters) for creating simple form 
layouts.

## Example

With ``formlayout``, generating a form is very easy.
Here is a simple example (more are included in source package):

```python
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
```

<img src="https://pythonhosted.org/formlayout/_images/simple.png">


