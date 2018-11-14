# -*- coding: utf-8 -*-
"""
formlayout
==========

Module creating Qt form dialogs/layouts to edit various type of parameters


formlayout License Agreement (MIT License)
------------------------------------------

Copyright (c) 2009-2015 Pierre Raybaut

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

from __future__ import print_function

__version__ = '2.0.0alpha'
__license__ = __doc__

DEBUG_FORMLAYOUT = False

import os
import sys
import datetime

STDERR = sys.stderr


# ---+- PyQt-PySide compatibility -+----
_modname = os.environ.setdefault('QT_API', 'pyqt')
assert _modname in ('pyqt', 'pyqt5', 'pyside', 'pyside2')

if os.environ['QT_API'].startswith('pyqt'):
    try:
        if os.environ['QT_API'] == 'pyqt5':
            import PyQt5  # analysis:ignore
        else:
            import PyQt4  # analysis:ignore
    except ImportError:
        # Switching to PySide
        os.environ['QT_API'] = _modname = 'pyside'
        try:
            import PySide  # analysis:ignore
        except ImportError:
            # Switching to PySide2
            os.environ['QT_API'] = _modname = 'pyside2'
            try:
                import PySide2  # analysis:ignore
            except ImportError:
                raise ImportError("formlayout requires PyQt4, PyQt5, PySide or PySide2")

if os.environ['QT_API'] == 'pyqt':
    try:
        from PyQt4.QtGui import QFormLayout
    except ImportError:
        raise ImportError("formlayout requires PyQt4, PyQt5, PySide or PySide2")
    from PyQt4.QtGui import *  # analysis:ignore
    from PyQt4.QtCore import *  # analysis:ignore
    from PyQt4.QtCore import pyqtSlot as Slot
    from PyQt4.QtCore import pyqtProperty as Property
    QT_LIB = 'PyQt4'

if os.environ['QT_API'] == 'pyqt5':
    from PyQt5.QtWidgets import *  # analysis:ignore
    from PyQt5.QtGui import *  # analysis:ignore
    from PyQt5.QtCore import *  # analysis:ignore
    from PyQt5.QtCore import pyqtSignal as Signal  # analysis:ignore
    from PyQt5.QtCore import pyqtSlot as Slot  # analysis:ignore
    from PyQt5.QtCore import pyqtProperty as Property  # analysis:ignore
    SIGNAL = None  # analysis:ignore
    QT_LIB = 'PyQt5'

if os.environ['QT_API'] == 'pyside':
    from PySide.QtGui import *  # analysis:ignore
    from PySide.QtCore import *  # analysis:ignore
    QT_LIB = 'PySide'
    
if os.environ['QT_API'] == 'pyside2':
    from PySide2.QtGui import *  # analysis:ignore
    from PySide2.QtCore import *  # analysis:ignore
    from PySide2.QtWidgets import *  # analysis:ignore
    QT_LIB = 'PySide2'


# ---+- Python 2-3 compatibility -+----
PY2 = sys.version[0] == '2'

if PY2:
    # Python 2
    import codecs
    def u(obj):
        """Make unicode object"""
        return codecs.unicode_escape_decode(obj)[0]
else:
    # Python 3
    def u(obj):
        """Return string as it is"""
        return obj

def is_text_string(obj):
    """Return True if `obj` is a text string, False if it is anything else,
    like binary data (Python 3) or QString (Python 2, PyQt API #1)"""
    if PY2:
        # Python 2
        return isinstance(obj, basestring)
    else:
        # Python 3
        return isinstance(obj, str)

def is_binary_string(obj):
    """Return True if `obj` is a binary string, False if it is anything else"""
    if PY2:
        # Python 2
        return isinstance(obj, str)
    else:
        # Python 3
        return isinstance(obj, bytes)

def is_string(obj):
    """Return True if `obj` is a text or binary Python string object,
    False if it is anything else, like a QString (Python 2, PyQt API #1)"""
    return is_text_string(obj) or is_binary_string(obj)

def to_text_string(obj, encoding=None):
    """Convert `obj` to (unicode) text string"""
    if PY2:
        # Python 2
        if encoding is None:
            return unicode(obj)
        else:
            return unicode(obj, encoding)
    else:
        # Python 3
        if encoding is None:
            return str(obj)
        elif isinstance(obj, str):
            # In case this function is not used properly, this could happen
            return obj
        else:
            return str(obj, encoding)


class ColorButton(QPushButton):
    """
    Color choosing push button
    """
    __pyqtSignals__ = ("colorChanged(QColor)",)
    if SIGNAL is None:
        colorChanged = Signal("QColor")
    
    def __init__(self, parent=None, colorChanged_slot=None):
        QPushButton.__init__(self, parent)
        self.setFixedSize(20, 20)
        self.setIconSize(QSize(12, 12))
        
        if colorChanged_slot:
            if SIGNAL is None:
                self.colorChanged.connect(colorChanged_slot)
            else:
                self.connect(self, SIGNAL("colorChanged(QColor)"),
                             colorChanged_slot)
        
        if SIGNAL is None:
            self.clicked.connect(self.choose_color)
        else:
            self.connect(self, SIGNAL("clicked()"), self.choose_color)
        self._color = QColor()
    
    def choose_color(self):
        color = QColorDialog.getColor(self._color, self.parentWidget())
        if color.isValid():
            self.set_color(color)
    
    def get_color(self):
        return self._color
    
    @Slot(QColor)
    def set_color(self, color):
        if color != self._color:
            self._color = color
            if SIGNAL is None:
                self.colorChanged.emit(self._color)
            else:
                self.emit(SIGNAL("colorChanged(QColor)"), self._color)
            pixmap = QPixmap(self.iconSize())
            pixmap.fill(color)
            self.setIcon(QIcon(pixmap))
    
    color = Property("QColor", get_color, set_color)


def text_to_qcolor(text):
    """
    Create a QColor from specified string
    Avoid warning from Qt when an invalid QColor is instantiated
    """
    color = QColor()
    if not is_string(text): # testing for QString (PyQt API#1)
        text = str(text)
    if not is_text_string(text):
        return color
    if text.startswith('#') and len(text)==7:
        correct = '#0123456789abcdef'
        for char in text:
            if char.lower() not in correct:
                return color
    elif text not in list(QColor.colorNames()):
        return color
    color.setNamedColor(text)
    return color


class ColorLayout(QHBoxLayout):
    """Color-specialized QLineEdit layout"""
    def __init__(self, color, parent=None):
        QHBoxLayout.__init__(self)
        assert isinstance(color, QColor)
        self.lineedit = QLineEdit(color.name(), parent)
        if SIGNAL is None:
            self.lineedit.textChanged.connect(self.update_color)
        else:
            self.connect(self.lineedit, SIGNAL("textChanged(QString)"),
                         self.update_color)
        self.addWidget(self.lineedit)
        self.colorbtn = ColorButton(parent, self.update_text)
        self.colorbtn.color = color
        
        self.addWidget(self.colorbtn)

    def update_color(self, text):
        color = text_to_qcolor(text)
        if color.isValid():
            self.colorbtn.color = color

    def update_text(self, color):
        self.lineedit.setText(color.name())
        
    def text(self):
        return self.lineedit.text()

    def setStyleSheet(self, style):
        self.lineedit.setStyleSheet(style)
        self.colorbtn.setStyleSheet(style)


class FileLayout(QHBoxLayout):
    """File-specialized QLineEdit layout"""
    def __init__(self, value, parent=None):
        QHBoxLayout.__init__(self)
        self.value = value
        self.lineedit = QLineEdit('', parent)
        self.addWidget(self.lineedit)
        self.filebtn = QPushButton('Browse')
        self.filebtn.clicked.connect(self.getfile)
        self.addWidget(self.filebtn)

    def getfile(self):
        if self.value.startswith('file'):
            name = QFileDialog.getOpenFileName(None, 'Select file',
                                               filter=self.value[5:])
            if QT_LIB == 'PyQt5':
                name, _filter = name
        elif self.value == 'dir':
            name = QFileDialog.getExistingDirectory(None, 'Select directory')
        if name:
            self.lineedit.setText(name)

    def text(self):
        return self.lineedit.text()

    def setStyleSheet(self, style):
        self.lineedit.setStyleSheet(style)


class SliderLayout(QHBoxLayout):
    """QSlider with QLabel"""
    def __init__(self, value, parent=None):
        QHBoxLayout.__init__(self)
        index = value.find('@')
        if index != -1:
            value, default = value[:index], int(value[index+1:])
        else:
            default = False
        parsed = value.split(':')
        self.slider = QSlider(Qt.Horizontal)
        if parsed[-1] == '':
            self.slider.setTickPosition(2)
            parsed.pop(-1)
        if len(parsed) == 2:
            self.slider.setMaximum(int(parsed[1]))
        elif len(parsed) == 3:
            self.slider.setMinimum(int(parsed[1]))
            self.slider.setMaximum(int(parsed[2]))
        if default:
            self.slider.setValue(default)  # always set value in last
        if SIGNAL is None:
            self.slider.valueChanged.connect(self.update)
        else:
            self.connect(self.slider, SIGNAL("valueChanged(int)"), self.update)
        self.cpt = QLabel(str(self.value()))
        self.addWidget(self.slider)
        self.addWidget(self.cpt)

    def update(self):
        self.cpt.setText(str(self.value()))

    def value(self):
        return self.slider.value()

    def setStyleSheet(self, style):
        self.slider.setStyleSheet(style)
        self.cpt.setStyleSheet(style)


class RadioLayout(QVBoxLayout):
    """Radio buttons layout with QButtonGroup"""
    def __init__(self, buttons, index, parent=None):
        QVBoxLayout.__init__(self)
        self.setSpacing(0)
        self.group = QButtonGroup()
        for i, button in enumerate(buttons):
            btn = QRadioButton(button)
            if i == index:
                btn.setChecked(True)
            self.addWidget(btn)
            self.group.addButton(btn, i)

    def currentIndex(self):
        return self.group.checkedId()

    def setStyleSheet(self, style):
        for btn in self.group.buttons():
            btn.setStyleSheet(style)


class CheckLayout(QVBoxLayout):
    """Check boxes layout with QButtonGroup"""
    def __init__(self, boxes, checks, parent=None):
        QVBoxLayout.__init__(self)
        self.setSpacing(0)
        self.group = QButtonGroup()
        self.group.setExclusive(False)
        for i, (box, check) in enumerate(zip(boxes, checks)):
            cbx = QCheckBox(box)
            cbx.setChecked(eval(check))
            self.addWidget(cbx)
            self.group.addButton(cbx, i)

    def values(self):
        return [cbx.isChecked() for cbx in self.group.buttons()]

    def setStyleSheet(self, style):
        for cbx in self.group.buttons():
            cbx.setStyleSheet(style)


class PushLayout(QHBoxLayout):
    """Push buttons horizontal layout"""
    def __init__(self, buttons, parent=None):
        QHBoxLayout.__init__(self)
        self.result = parent.result
        self.dialog = parent.get_dialog()
        for button in buttons:
            label, callback = button
            self.btn = QPushButton(label)
            if SIGNAL is None:
                self.btn.clicked.connect(self.call(callback))
            else:
                self.connect(self.btn, SIGNAL("clicked()"), self.call(callback))
            self.addWidget(self.btn)

    def call(self, callback):
        return lambda: self.apply(callback)

    def apply(self, callback):
        if self.result == 'XML':
            app = ET.Element('App')
            app.attrib['title'] = self.dialog.title
            child = ET.fromstring(self.dialog.formwidget.get())
            app.append(child)
            callback(ET.tostring(app),
                     self.dialog.formwidget.get_widgets())
        else:
            callback(self.dialog.formwidget.get(),
                     self.dialog.formwidget.get_widgets())


class CountLayout(QHBoxLayout):
    """Field with a QSpinBox"""
    def __init__(self, field, parent=None):
        QHBoxLayout.__init__(self)
        self.field = field
        self.count = QSpinBox()
        self.count.setFixedWidth(45)
        self.addWidget(self.field)
        self.addWidget(self.count)

    def text(self):
        return self.field.text()

    def currentIndex(self):
        return self.field.currentIndex()

    def n(self):
        return self.count.value()

    def setStyleSheet(self, style):
        self.field.setStyleSheet(style)
        self.count.setStyleSheet(style)


def font_is_installed(font):
    """Check if font is installed"""
    return [fam for fam in QFontDatabase().families()
            if to_text_string(fam) == font]

def tuple_to_qfont(tup):
    """
    Create a QFont from tuple:
        (family [string], size [int], italic [bool], bold [bool])
    """
    if not isinstance(tup, tuple) or len(tup) != 4 \
       or not is_text_string(tup[0]) \
       or not isinstance(tup[1], int) \
       or not isinstance(tup[2], bool) \
       or not isinstance(tup[3], bool):
        return None
    font = QFont()
    family, size, italic, bold = tup
    font.setFamily(family)
    font.setPointSize(size)
    font.setItalic(italic)
    font.setBold(bold)
    return font

def qfont_to_tuple(font):
    return (to_text_string(font.family()), int(font.pointSize()),
            font.italic(), font.bold())

class FontLayout(QGridLayout):
    """Font selection"""
    def __init__(self, value, parent=None):
        QGridLayout.__init__(self)
        if not font_is_installed(value[0]):
            print("Warning: Font `%s` is not installed" % value[0],
                  file=sys.stderr)
        font = tuple_to_qfont(value)
        assert font is not None
        
        # Font family
        self.family = QFontComboBox(parent)
        self.family.setCurrentFont(font)
        self.addWidget(self.family, 0, 0, 1, -1)
        
        # Font size
        self.size = QComboBox(parent)
        self.size.setEditable(True)
        sizelist = list(range(6, 12)) + list(range(12, 30, 2)) + [36, 48, 72]
        size = font.pointSize()
        if size not in sizelist:
            sizelist.append(size)
            sizelist.sort()
        self.size.addItems([str(s) for s in sizelist])
        self.size.setCurrentIndex(sizelist.index(size))
        self.addWidget(self.size, 1, 0)
        
        # Italic or not
        self.italic = QCheckBox(self.tr("Italic"), parent)
        self.italic.setChecked(font.italic())
        self.addWidget(self.italic, 1, 1)
        
        # Bold or not
        self.bold = QCheckBox(self.tr("Bold"), parent)
        self.bold.setChecked(font.bold())
        self.addWidget(self.bold, 1, 2)
        
    def get_font(self):
        font = self.family.currentFont()
        font.setItalic(self.italic.isChecked())
        font.setBold(self.bold.isChecked())
        font.setPointSize(int(self.size.currentText()))
        return qfont_to_tuple(font)

    def setStyleSheet(self, style):
        self.family.setStyleSheet(style)
        self.size.setStyleSheet(style)
        self.italic.setStyleSheet(style)
        self.bold.setStyleSheet(style)


def is_float_valid(edit):
    text = edit.text()
    state = edit.validator().validate(text, 0)[0]
    return state == QDoubleValidator.Acceptable

def is_required_valid(edit, widget_color):
    required_color = "background-color:rgb(255, 175, 90);"
    if widget_color:
        widget_color = "background-color:" + widget_color + ";"
    else:
        widget_color = ""
    if isinstance(edit, (QLineEdit, FileLayout)):
        if edit.text():
            edit.setStyleSheet(widget_color)
            return True
        else:
            edit.setStyleSheet(required_color)
    elif isinstance(edit, (QComboBox, RadioLayout)):
        if edit.currentIndex() != -1:
            edit.setStyleSheet(widget_color)
            return True
        else:
            edit.setStyleSheet(required_color)
    elif isinstance(edit, QTextEdit):
        if edit.toPlainText():
            edit.setStyleSheet(widget_color)
            return True
        else:
            edit.setStyleSheet(required_color)
    return False

class FormWidget(QWidget):
    def __init__(self, data, comment="", parent=None):
        QWidget.__init__(self, parent)
        from copy import deepcopy
        self.data = deepcopy(data)
        self.result = parent.result
        self.type = parent.type
        self.widget_color = parent.widget_color
        self.widgets = []
        self.formlayout = QFormLayout(self)
        if comment:
            self.formlayout.addRow(QLabel(comment))
            self.formlayout.addRow(QLabel(" "))
        if DEBUG_FORMLAYOUT:
            print("\n"+("*"*80))
            print("DATA:", self.data)
            print("*"*80)
            print("COMMENT:", comment)
            print("*"*80)
            
    def get_dialog(self):
        """Return FormDialog instance"""
        dialog = self.parent()
        while not isinstance(dialog, QDialog):
            dialog = dialog.parent()
        return dialog

    def setup(self):
        for label, value in self.data:
            if DEBUG_FORMLAYOUT:
                print("value:", value)
            if label is None and value is None:
                # Separator: (None, None)
                separator = QFrame()
                separator.setFrameShape(QFrame.HLine)
                separator.setFrameShadow(QFrame.Sunken)
                self.formlayout.addRow(separator)
                self.widgets.append(None)
                continue
            if label is None:
                if isinstance(value, (list, tuple)):
                    field = PushLayout(value, self)
                    self.formlayout.addRow(field)
                else:
                    img_fmt = tuple(['.'+str(bytes(ext.data() if QT_LIB == "PySide" or QT_LIB == "PySide2" else ext).decode()) 
                                    for ext in QImageReader.supportedImageFormats()])
                    if value.endswith(img_fmt):
                        # Image
                        pixmap = QPixmap(value)
                        lab = QLabel()
                        lab.setPixmap(pixmap)
                        self.formlayout.addRow(lab)
                    else:
                        # Comment
                        self.formlayout.addRow(QLabel(value))
                self.widgets.append(None)
                continue
            if tuple_to_qfont(value) is not None:
                field = FontLayout(value, self)
            elif text_to_qcolor(value).isValid():
                field = ColorLayout(QColor(value), self)
            elif is_text_string(value):
                if value in ['file', 'dir'] or value.startswith('file:'):
                    field = FileLayout(value, self)
                elif value == 'slider' or value.startswith('slider:') \
                                       or value.startswith('slider@'):
                    field = SliderLayout(value, self)
                elif value == 'password':
                    field = QLineEdit(self)
                    field.setEchoMode(QLineEdit.Password)
                elif value in ['calendar', 'calendarM'] \
                           or value.startswith(('calendar:', 'calendarM:')) \
                           or value.startswith(('calendar@', 'calendarM@')):
                    index = value.find('@')
                    if index != -1:
                        value, date = value[:index], value[index+1:]
                    else:
                        date = False
                    field = QCalendarWidget(self)
                    field.setVerticalHeaderFormat(field.NoVerticalHeader)
                    parsed = value.split(':')
                    if parsed[-1] == '':
                        field.setGridVisible(True)
                        parsed.pop(-1)
                    if parsed[0] == 'calendarM':
                        field.setFirstDayOfWeek(Qt.Monday)
                    if len(parsed) == 2:
                        field.setMaximumDate(datetime.date(*eval(parsed[1])))
                    elif len(parsed) == 3:
                        field.setMinimumDate(datetime.date(*eval(parsed[1])))
                        field.setMaximumDate(datetime.date(*eval(parsed[2])))
                    if date:
                        field.setSelectedDate(datetime.date(*eval(date)))
                elif '\n' in value:
                    if value == '\n':
                        value = ''
                    for linesep in (os.linesep, '\n'):
                        if linesep in value:
                            value = value.replace(linesep, u("\u2029"))
                    field = QTextEdit(value, self)
                else:
                    field = QLineEdit(value, self)
            elif isinstance(value, (list, tuple)) and is_text_string(value[0])\
                                                 and value[0].startswith('0b'):
                field = CheckLayout(value[1:], value[0][2:], self)
            elif isinstance(value, (list, tuple)):
                save_value = value
                value = list(value)  # always needed to protect self.data
                selindex = value.pop(0)
                if isinstance(selindex, int):
                    selindex = selindex - 1
                if isinstance(value[0], (list, tuple)):
                    keys = [ key for key, _val in value ]
                    value = [ val for _key, val in value ]
                else:
                    keys = value
                if selindex in value:
                    selindex = value.index(selindex)
                elif selindex in keys:
                    selindex = keys.index(selindex)
                elif not isinstance(selindex, int):
                    print("Warning: '%s' index is invalid (label: "\
                          "%s, value: %s)" % (selindex, label, value),
                          file=STDERR)
                    selindex = -1
                if isinstance(save_value, list):
                    field = QComboBox(self)
                    field.addItems(value)
                    field.setCurrentIndex(selindex)
                elif isinstance(save_value, tuple):
                    field = RadioLayout(value, selindex, self)
            elif isinstance(value, bool):
                field = QCheckBox(self)
                field.setChecked(value)
            elif isinstance(value, float):
                field = QLineEdit(QLocale().toString(value), self)
                field.setValidator(QDoubleValidator(field))
                dialog = self.get_dialog()
                dialog.register_float_field(field)
                if SIGNAL is None:
                    field.textChanged.connect(dialog.float_valid)
                else:
                    self.connect(field, SIGNAL('textChanged(QString)'),
                                 dialog.float_valid)
            elif isinstance(value, int):
                field = QSpinBox(self)
                field.setRange(-1e9, 1e9)
                field.setValue(value)
            elif isinstance(value, datetime.datetime):
                field = QDateTimeEdit(self)
                field.setDateTime(value)
            elif isinstance(value, datetime.date):
                field = QDateEdit(self)
                field.setDate(value)
            elif isinstance(value, datetime.time):
                field = QTimeEdit(self)
                field.setTime(value)
            else:
                field = QLineEdit(repr(value), self)

            # Eventually catching the 'countfield' feature and processing it
            if label.startswith('n '):
                label = label[2:]
                if isinstance(field, QLineEdit) and is_text_string(value) or\
                   isinstance(field, QComboBox):
                    field = CountLayout(field)
                else:
                    print("Warning: '%s' doesn't support 'nfield' feature"\
                          % label, file=STDERR)

            # Eventually extracting tooltip from label and processing it
            index = label.find('::')
            if index != -1:
                label, tooltip = label[:index], label[index+2:]
                field.setToolTip(tooltip)

            # Eventually catching the 'required' feature and processing it
            if label.endswith(' *'):
                label = label[:-1] + '<font color="red">*</font>'
                if isinstance(field, (QLineEdit, QTextEdit, QComboBox,
                                      FileLayout, RadioLayout)):
                    dialog = self.get_dialog()
                    dialog.register_required_field(field)
                else:
                    print("Warning: '%s' doesn't support 'required' feature"\
                          % type(field), file=STDERR)
                if isinstance(field, QLineEdit):
                    if SIGNAL is None:
                        field.textChanged.connect(dialog.required_valid)
                    else:
                        self.connect(field, SIGNAL('textChanged(QString)'),
                                     dialog.required_valid)
                elif isinstance(field, QTextEdit):
                    if SIGNAL is None:
                        field.textChanged.connect(dialog.required_valid)
                    else:
                        self.connect(field, SIGNAL('textChanged()'),
                                     dialog.required_valid)
                elif isinstance(field, QComboBox):
                    if SIGNAL is None:
                        field.currentIndexChanged.connect(\
                            dialog.required_valid)
                    else:
                        self.connect(field,
                                     SIGNAL('currentIndexChanged(QString)'),
                                     dialog.required_valid)
                elif isinstance(field, FileLayout):
                    if SIGNAL is None:
                        field.lineedit.textChanged.connect(\
                            dialog.required_valid)
                    else:
                        self.connect(field.lineedit,
                                     SIGNAL('textChanged(QString)'),
                                     dialog.required_valid)
                elif isinstance(field, RadioLayout):
                    if SIGNAL is None:
                        field.group.buttonClicked.connect(\
                            dialog.required_valid)
                    else:
                        self.connect(field.group, SIGNAL('buttonClicked(int)'),
                                     dialog.required_valid)

            # Eventually setting the widget_color
            if self.widget_color:
                style = "background-color:" + self.widget_color + ";"
                field.setStyleSheet(style)

            if self.type == 'form':
                self.formlayout.addRow(label, field)
            elif self.type == 'questions':
                self.formlayout.addRow(QLabel(label))
                self.formlayout.addRow(field)
            self.widgets.append(field)
            
    def get(self):
        valuelist = []
        for index, (label, value) in enumerate(self.data):
            field = self.widgets[index]
            if label is None:
                # Separator / Comment
                continue
            if label.startswith('n '):
                label = label[2:]
            if tuple_to_qfont(value) is not None:
                value = field.get_font()
            elif is_text_string(value):
                if isinstance(field, QTextEdit):
                    value = to_text_string(field.toPlainText()
                                           ).replace(u("\u2029"), os.linesep)
                elif isinstance(field, SliderLayout):
                    value = field.value()
                elif isinstance(field, QCalendarWidget):
                    value = field.selectedDate()
                    try:
                        value = value.toPyDate()  # PyQt
                    except AttributeError:
                        value = value.toPython()  # PySide
                else:
                    value = to_text_string(field.text())
            elif isinstance(field, CheckLayout):
                value = field.values()
            elif isinstance(value, (list, tuple)):
                index = int(field.currentIndex())
                if isinstance(value[0], int):
                    # Return an int index, if initialization was an int
                    value = index + 1
                else:
                    value = value[index+1]
                    if isinstance(value, (list, tuple)):
                        value = value[0]
            elif isinstance(value, bool):
                value = field.checkState() == Qt.Checked
            elif isinstance(value, float):
                value = float(QLocale().toDouble(field.text())[0])
            elif isinstance(value, int):
                value = int(field.value())
            elif isinstance(value, datetime.datetime):
                value = field.dateTime()
                try:
                    value = value.toPyDateTime()  # PyQt
                except AttributeError:
                    value = value.toPython()  # PySide
            elif isinstance(value, datetime.date):
                value = field.date()
                try:
                    value = value.toPyDate()  # PyQt
                except AttributeError:
                    value = value.toPython()  # PySide
            elif isinstance(value, datetime.time):
                value = field.time()
                try:
                    value = value.toPyTime()  # PyQt
                except AttributeError:
                    value = value.toPython()  # PySide
            else:
                value = eval(str(field.text()))
            if isinstance(field, CountLayout):
                value = (value, field.n())
            valuelist.append((label, value))
        if self.result == 'list':
            return [value for label, value in valuelist]
        elif self.result in ['dict', 'OrderedDict', 'JSON']:
            if self.result == 'dict':
                dic = {}
            else:
                dic = OrderedDict()
            for label, value in valuelist:
                if label in dic.keys():
                    print("Warning: '%s' is duplicate and '%s' doesn't "\
                          "handle it, you should use 'list' or 'XML' instead"\
                          % (label, self.result), file=STDERR)
                if isinstance(value, (datetime.date, datetime.time,
                              datetime.datetime)) and self.result == 'JSON':
                    dic[label] = value.isoformat()
                else:
                    dic[label] = value
            if self.result == 'JSON':
                return json.dumps(dic)
            else:
                return dic
        elif self.result == 'XML':
            form = ET.Element('Form')
            for label, value in valuelist:
                tooltip = ''
                index = label.find('::')
                if index != -1:
                    label, tooltip = label[:index], label[index+2:]
                required = 'false'
                if label.endswith(' *'):
                    label = label[:-2]
                    required = 'true'
                child = ET.SubElement(form, label)
                if isinstance(value, tuple):
                    child.text = to_text_string(value[0])
                    child.attrib['amount'] = to_text_string(value[1])
                else:
                    if isinstance(value, datetime.datetime):
                        child.text = value.isoformat()
                    else:
                        child.text = to_text_string(value)
                child.attrib['tooltip'] = tooltip
                child.attrib['required'] = required
            return ET.tostring(form)

    def get_widgets(self):
        return self.widgets


class FormComboWidget(QWidget):
    def __init__(self, datalist, comment="", parent=None):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.combobox = QComboBox()
        layout.addWidget(self.combobox)
        
        self.stackwidget = QStackedWidget(self)
        layout.addWidget(self.stackwidget)
        if SIGNAL is None:
            self.combobox.currentIndexChanged.connect(
                                            self.stackwidget.setCurrentIndex)
        else:
            self.connect(self.combobox, SIGNAL("currentIndexChanged(int)"),
                         self.stackwidget, SLOT("setCurrentIndex(int)"))

        self.result = parent.result 
        self.widget_color = parent.widget_color
        if self.widget_color:
            style = "background-color:" + self.widget_color + ";"
            self.combobox.setStyleSheet(style)
        self.type = parent.type
        self.widgetlist = []
        for data, title, comment in datalist:
            self.combobox.addItem(title)
            widget = FormWidget(data, comment=comment, parent=self)
            self.stackwidget.addWidget(widget)
            self.widgetlist.append((title, widget))
            
    def setup(self):
        for title, widget in self.widgetlist:
            widget.setup()

    def get(self):
        if self.result == 'list':
            return [widget.get() for title, widget in self.widgetlist]
        elif self.result in ['dict', 'OrderedDict', 'JSON']:
            if self.result == 'dict':
                dic = {}
            else:
                dic = OrderedDict()
            for title, widget in self.widgetlist:
                if self.result == 'JSON':
                    dic[title] = json.loads(widget.get(),
                                            object_pairs_hook=OrderedDict)
                else:
                    dic[title] = widget.get()
            if self.result == 'JSON':
                return json.dumps(dic)
            else:
                return dic
        elif self.result == 'XML':
            combos = ET.Element('Combos')
            for title, widget in self.widgetlist:
                combo = ET.SubElement(combos, 'Combo')
                combo.attrib['title'] = title
                child = ET.fromstring(widget.get())
                combo.append(child)
            return ET.tostring(combos)

    def get_widgets(self):
        widgets = []
        for title, widget in self.widgetlist:
            widgets.extend(widget.get_widgets())
        return widgets


class FormTabWidget(QWidget):
    def __init__(self, datalist, comment="", parent=None):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout()
        self.tabwidget = QTabWidget()
        layout.addWidget(self.tabwidget)
        self.setLayout(layout)
        self.result = parent.result
        self.widget_color = parent.widget_color
        self.type = parent.type
        self.widgetlist = []
        for data, title, comment in datalist:
            if len(data[0])==3:
                widget = FormComboWidget(data, comment=comment, parent=self)
            else:
                widget = FormWidget(data, comment=comment, parent=self)
            index = self.tabwidget.addTab(widget, title)
            self.tabwidget.setTabToolTip(index, comment)
            self.widgetlist.append((title, widget))
            
    def setup(self):
        for title, widget in self.widgetlist:
            widget.setup()
            
    def get(self):
        if self.result == 'list':
            return [widget.get() for title, widget in self.widgetlist]
        elif self.result in ['dict', 'OrderedDict', 'JSON']:
            if self.result == 'dict':
                dic = {}
            else:
                dic = OrderedDict()
            for title, widget in self.widgetlist:
                if self.result == 'JSON':
                    dic[title] = json.loads(widget.get(),
                                            object_pairs_hook=OrderedDict)
                else:
                    dic[title] = widget.get()
            if self.result == 'JSON':
                return json.dumps(dic)
            else:
                return dic
        elif self.result == 'XML':
            tabs = ET.Element('Tabs')
            for title, widget in self.widgetlist:
                tab = ET.SubElement(tabs, 'Tab')
                tab.attrib['title'] = title
                child = ET.fromstring(widget.get())
                tab.append(child)
            return ET.tostring(tabs)

    def get_widgets(self):
        widgets = []
        for title, widget in self.widgetlist:
            widgets.extend(widget.get_widgets())
        return widgets


class FormDialog(QDialog):
    """Form Dialog"""
    def __init__(self, data, title="", comment="", icon=None, parent=None,
                 apply=None, ok=None, cancel=None, result=None, outfile=None,
                 type=None, scrollbar=None, background_color=None,
                 widget_color=None):
        QDialog.__init__(self, parent)
        
        # Destroying the C++ object right after closing the dialog box,
        # otherwise it may be garbage-collected in another QThread
        # (e.g. the editor's analysis thread in Spyder), thus leading to
        # a segmentation fault on UNIX or an application crash on Windows
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.type = type
        self.title = title
        self.ok = ok
        self.cancel = cancel
        self.apply_ = None
        self.apply_callback = None
        if callable(apply):
            self.apply_callback = apply
        elif isinstance(apply, (list, tuple)):
            self.apply_, self.apply_callback = apply
        elif apply is not None:
            raise AssertionError("`apply` argument must be either a function "\
                                 "or tuple ('Apply label', apply_callback)")
        self.outfile = outfile
        self.result = result
        if self.result in ['OrderedDict', 'JSON']:
            global OrderedDict
            from collections import OrderedDict
            if self.result == 'JSON':
                global json
                import json
        elif self.result == 'XML':
            global ET
            import xml.etree.ElementTree as ET

        self.widget_color = widget_color
        if background_color:
            style = "FormDialog {background-color:" + background_color + ";}"
            self.setStyleSheet(style)

        # Form
        if isinstance(data[0][0], (list, tuple)):
            self.formwidget = FormTabWidget(data, comment=comment,
                                            parent=self)
        elif len(data[0])==3:
            self.formwidget = FormComboWidget(data, comment=comment,
                                              parent=self)
        else:
            self.formwidget = FormWidget(data, comment=comment, 
                                         parent=self)
        layout = QVBoxLayout()

        if scrollbar == True:
            scroll = QScrollArea(parent=self)
            scroll.setWidgetResizable(True)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll.setWidget(self.formwidget)
            layout.addWidget(scroll)
        else:
            layout.addWidget(self.formwidget)

        self.float_fields = []
        self.required_fields = []
        self.formwidget.setup()
        
        # Button box
        self.bbox = bbox = QDialogButtonBox()
        if self.ok == True:
            bbox.addButton(QDialogButtonBox.Ok)
        elif self.ok:
            ok_btn = QPushButton(self.ok)
            bbox.addButton(ok_btn, QDialogButtonBox.AcceptRole)
        if self.cancel == True:
            bbox.addButton(QDialogButtonBox.Cancel)
        elif self.cancel:
            cancel_btn = QPushButton(self.cancel)
            bbox.addButton(cancel_btn, QDialogButtonBox.RejectRole)

        if self.apply_callback is not None:
            if self.apply_:
                apply_btn = QPushButton(self.apply_)
                bbox.addButton(apply_btn, QDialogButtonBox.ApplyRole)
            else:
                apply_btn = bbox.addButton(QDialogButtonBox.Apply)
            if SIGNAL is None:
                apply_btn.clicked.connect(self.apply)
            else:
                self.connect(apply_btn, SIGNAL("clicked()"), self.apply)
        if SIGNAL is None:
            if self.ok:
                bbox.accepted.connect(self.accept)
            if self.cancel:
                bbox.rejected.connect(self.reject)
        else:
            if self.ok:
                self.connect(bbox, SIGNAL("accepted()"), SLOT("accept()"))
            if self.cancel:
                self.connect(bbox, SIGNAL("rejected()"), SLOT("reject()"))
        layout.addWidget(bbox)
        self.required_valid()

        self.setLayout(layout)
        
        self.setWindowTitle(self.title)
        if not isinstance(icon, QIcon):
            icon = QWidget().style().standardIcon(QStyle.SP_MessageBoxQuestion)
        self.setWindowIcon(icon)
        
    def register_float_field(self, field):
        self.float_fields.append(field)

    def register_required_field(self, field):
        self.required_fields.append(field)

    def float_valid(self):
        valid = True
        for field in self.float_fields:
            if not is_float_valid(field):
                valid = False
        self.update_buttons(valid)

    def required_valid(self):
        valid = True
        for field in self.required_fields:
            if not is_required_valid(field, self.widget_color):
                valid = False
        self.update_buttons(valid)

    def update_buttons(self, valid):
        for btn in self.bbox.buttons():
            btn_role = self.bbox.buttonRole(btn)
            if btn_role in (QDialogButtonBox.AcceptRole,
                            QDialogButtonBox.ApplyRole):
                btn.setEnabled(valid)
        
    def accept(self):
        if self.result == 'XML':
            app = ET.Element('App')
            app.attrib['title'] = self.title
            child = ET.fromstring(self.formwidget.get())
            app.append(child)
            self.data = ET.tostring(app)
        else:
            self.data = self.formwidget.get()
        QDialog.accept(self)
        
    def reject(self):
        self.data = None
        QDialog.reject(self)
        
    def apply(self):
        if self.result == 'XML':
            app = ET.Element('App')
            app.attrib['title'] = self.title
            child = ET.fromstring(self.formwidget.get())
            app.append(child)
            self.apply_callback(ET.tostring(app),
                                self.formwidget.get_widgets())
        else:
            self.apply_callback(self.formwidget.get(),
                                self.formwidget.get_widgets())
        
    def get(self):
        """Return form result"""
        # It is import to avoid accessing Qt C++ object as it has probably
        # already been destroyed, due to the Qt.WA_DeleteOnClose attribute
        if self.outfile:
            if self.result in ['list', 'dict', 'OrderedDict']:
                fd = open(self.outfile + '.py', 'w')
                fd.write(str(self.data))
            elif self.result == 'JSON':
                fd = open(self.outfile + '.json', 'w')
                data = json.loads(self.data, object_pairs_hook=OrderedDict)
                json.dump(data, fd)
            elif self.result == 'XML':
                fd = open(self.outfile + '.xml', 'w')
                root = ET.fromstring(self.data)
                tree = ET.ElementTree(root)
                tree.write(fd, encoding='UTF-8')
            fd.close()
        else:
            return self.data


def fedit(data, title="", comment="", icon=None, parent=None, apply=None,
          ok=True, cancel=True, result='list', outfile=None, type='form',
          scrollbar=False, background_color=None, widget_color=None):
    """
    Create form dialog and return result
    (if Cancel button is pressed, return None)

    :param tuple data: datalist, datagroup (see below)
    :param str title: form title
    :param str comment: header comment
    :param QIcon icon: dialog box icon
    :param QWidget parent: parent widget
    :param str ok: customized ok button label
    :param str cancel: customized cancel button label
    :param tuple apply: (label, function) customized button label and callback
    :param function apply: function taking two arguments (result, widgets)
    :param str result: result serialization ('list', 'dict', 'OrderedDict',
                                             'JSON' or 'XML')
    :param str outfile: write result to the file outfile.[py|json|xml]
    :param str type: layout type ('form' or 'questions')
    :param bool scrollbar: vertical scrollbar
    :param str background_color: color of the background
    :param str widget_color: color of the widgets

    :return: Serialized result (data type depends on `result` parameter)
    
    datalist: list/tuple of (field_name, field_value)
    datagroup: list/tuple of (datalist *or* datagroup, title, comment)
    
    Tips:
      * one field for each member of a datalist
      * one tab for each member of a top-level datagroup
      * one page (of a multipage widget, each page can be selected with a 
        combo box) for each member of a datagroup inside a datagroup
       
    Supported types for field_value:
      - int, float, str, unicode, bool
      - colors: in Qt-compatible text form, i.e. in hex format or name (red,...)
                (automatically detected from a string)
      - list/tuple:
          * the first element will be the selected index (or value)
          * the other elements can be couples (key, value) or only values
    """
    # Create a QApplication instance if no instance currently exists
    # (e.g. if the module is used directly from the interpreter)
    test_travis = os.environ.get('TEST_CI_WIDGETS', None)
    if test_travis is not None:
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        timer = QTimer(app)
        timer.timeout.connect(app.quit)
        timer.start(1000)
    elif QApplication.startingUp():
        _app = QApplication([])
        translator_qt = QTranslator()
        translator_qt.load('qt_' + QLocale.system().name(),
                       QLibraryInfo.location(QLibraryInfo.TranslationsPath))
        _app.installTranslator(translator_qt)

    serial = ['list', 'dict', 'OrderedDict', 'JSON', 'XML']
    if result not in serial:
        print("Warning: '%s' not in %s, default to list" %
              (result, ', '.join(serial)), file=sys.stderr)
        result = 'list'

    layouts = ['form', 'questions']
    if type not in layouts:
        print("Warning: '%s' not in %s, default to form" %
              (type, ', '.join(layouts)), file=sys.stderr)
        type = 'form'

    dialog = FormDialog(data, title, comment, icon, parent, apply, ok, cancel,
                        result, outfile, type, scrollbar, background_color,
                        widget_color)
    if dialog.exec_():
        return dialog.get()


if __name__ == "__main__":

    def create_datalist_example():
        return [('str', 'this is a string'),
                ('str', """this is a 
                MULTILINE
                string"""),
                ('list', [0, '1', '3', '4']),
                ('list2', ['--', ('none', 'None'), ('--', 'Dashed'),
                           ('-.', 'DashDot'), ('-', 'Solid'),
                           ('steps', 'Steps'), (':', 'Dotted')]),
                ('float', 1.2),
                (None, 'Other:'),
                ('int', 12),
                ('font', ('Arial', 10, False, True)),
                ('color', '#123409'),
                ('bool', True),
                ('date', datetime.date(2010, 10, 10)),
                ('datetime', datetime.datetime(2010, 10, 10)),
                ]
        
    def create_datagroup_example():
        datalist = create_datalist_example()
        return ((datalist, "Category 1", "Category 1 comment"),
                (datalist, "Category 2", "Category 2 comment"),
                (datalist, "Category 3", "Category 3 comment"))
    
    #--------- datalist example
    datalist = create_datalist_example()
    def apply_test(data):
        print("data:", data)
    print("result:", fedit(datalist, title="Example",
                           comment="This is just an <b>example</b>.",
                           apply=apply_test))
    
    #--------- datagroup example
    datagroup = create_datagroup_example()
    print("result:", fedit(datagroup, "Global title"))
    
    #--------- datagroup inside a datagroup example
    datalist = create_datalist_example()
    datagroup = create_datagroup_example()
    print("result:", fedit(((datagroup, "Title 1", "Tab 1 comment"),
                            (datalist, "Title 2", "Tab 2 comment"),
                            (datalist, "Title 3", "Tab 3 comment")),
                            "Global title"))
