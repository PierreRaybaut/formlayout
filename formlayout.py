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
assert _modname in ('pyqt', 'pyqt5', 'pyside')

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
            raise ImportError("formlayout requires PyQt4, PyQt5 or PySide")

if os.environ['QT_API'] == 'pyqt':
    try:
        from PyQt4.QtGui import QFormLayout
    except ImportError:
        raise ImportError("formlayout requires PyQt4, PyQt5 or PySide")
    from PyQt4.QtGui import *  # analysis:ignore
    from PyQt4.QtCore import *  # analysis:ignore
    from PyQt4.QtCore import pyqtSlot as Slot
    from PyQt4.QtCore import pyqtProperty as Property

if os.environ['QT_API'] == 'pyqt5':
    from PyQt5.QtWidgets import *  # analysis:ignore
    from PyQt5.QtGui import *  # analysis:ignore
    from PyQt5.QtCore import *  # analysis:ignore
    from PyQt5.QtCore import pyqtSignal as Signal  # analysis:ignore
    from PyQt5.QtCore import pyqtSlot as Slot  # analysis:ignore
    from PyQt5.QtCore import pyqtProperty as Property  # analysis:ignore
    SIGNAL = None  # analysis:ignore

if os.environ['QT_API'] == 'pyside':
    from PySide.QtGui import *  # analysis:ignore
    from PySide.QtCore import *  # analysis:ignore


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
    
    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)
        self.setFixedSize(20, 20)
        self.setIconSize(QSize(12, 12))
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
        self.colorbtn = ColorButton(parent)
        self.colorbtn.color = color
        if SIGNAL is None:
            self.colorbtn.colorChanged.connect(self.update_text)
        else:
            self.connect(self.colorbtn, SIGNAL("colorChanged(QColor)"),
                         self.update_text)
        self.addWidget(self.colorbtn)

    def update_color(self, text):
        color = text_to_qcolor(text)
        if color.isValid():
            self.colorbtn.color = color

    def update_text(self, color):
        self.lineedit.setText(color.name())
        
    def text(self):
        return self.lineedit.text()


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
        elif self.value == 'dir':
            name = QFileDialog.getExistingDirectory(None, 'Select directory')
        self.lineedit.setText(name)

    def text(self):
        return self.lineedit.text()


class RadioLayout(QVBoxLayout):
    """Radio buttons layout with QButtonGroup"""
    def __init__(self, buttons, index, parent=None):
        QVBoxLayout.__init__(self)
        self.group = QButtonGroup()
        for i, button in enumerate(buttons):
            self.btn = QRadioButton(button)
            if i == index:
                self.btn.setChecked(True)
            self.addWidget(self.btn)
            self.group.addButton(self.btn, i)

    def currentIndex(self):
        return self.group.id(self.group.checkedButton())


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
       or not font_is_installed(tup[0]) \
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


def is_edit_valid(edit):
    text = edit.text()
    state = edit.validator().validate(text, 0)[0]
    return state == QDoubleValidator.Acceptable

class FormWidget(QWidget):
    def __init__(self, data, comment="", parent=None):
        QWidget.__init__(self, parent)
        from copy import deepcopy
        self.data = deepcopy(data)
        self.result = parent.result
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
                img_fmt = tuple(['.'+str(bytes(ext).decode()) for ext 
                                 in QImageReader.supportedImageFormats()])
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
                elif value == 'password':
                    field = QLineEdit(self)
                    field.setEchoMode(QLineEdit.Password)
                elif '\n' in value:
                    for linesep in (os.linesep, '\n'):
                        if linesep in value:
                            value = value.replace(linesep, u("\u2029"))
                    field = QTextEdit(value, self)
                else:
                    field = QLineEdit(value, self)
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
                field.setCheckState(Qt.Checked if value else Qt.Unchecked)
            elif isinstance(value, float):
                field = QLineEdit(QLocale().toString(value), self)
                field.setValidator(QDoubleValidator(field))
                dialog = self.get_dialog()
                dialog.register_float_field(field)
                if SIGNAL is None:
                    field.textChanged.connect(
                                 lambda text: dialog.update_buttons())
                else:
                    self.connect(field, SIGNAL('textChanged(QString)'),
                                 lambda text: dialog.update_buttons())
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
            else:
                field = QLineEdit(repr(value), self)
            
            # Eventually extracting tooltip from label and processing it
            index = label.find('::')
            if index != -1:
                label, tooltip = label[:index], label[index+2:]
                field.setToolTip(tooltip)

            self.formlayout.addRow(label, field)
            self.widgets.append(field)
            
    def get(self):
        valuelist = []
        for index, (label, value) in enumerate(self.data):
            field = self.widgets[index]
            if label is None:
                # Separator / Comment
                continue
            elif tuple_to_qfont(value) is not None:
                value = field.get_font()
            elif is_text_string(value):
                if isinstance(field, QTextEdit):
                    value = to_text_string(field.toPlainText()
                                           ).replace(u("\u2029"), os.linesep)
                else:
                    value = to_text_string(field.text())
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
            else:
                value = eval(str(field.text()))
            valuelist.append((label, value))
        if self.result == 'list':
            return [value for label, value in valuelist]
        elif self.result in ['dict', 'OrderedDict', 'JSON']:
            if self.result == 'dict':
                dic = {}
            else:
                dic = OrderedDict()
            for label, value in valuelist:
                dic[label] = value
            if self.result == 'JSON':
                return json.dumps(dic)
            else:
                return dic


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
                    dic[title] = json.loads(widget.get())
                else:
                    dic[title] = widget.get()
            if self.result == 'JSON':
                return json.dumps(dic)
            else:
                return dic


class FormTabWidget(QWidget):
    def __init__(self, datalist, comment="", parent=None):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout()
        self.tabwidget = QTabWidget()
        layout.addWidget(self.tabwidget)
        self.setLayout(layout)
        self.result = parent.result
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
                    dic[title] = json.loads(widget.get())
                else:
                    dic[title] = widget.get()
            if self.result == 'JSON':
                return json.dumps(dic)
            else:
                return dic


class FormDialog(QDialog):
    """Form Dialog"""
    def __init__(self, data, title="", comment="",
                 icon=None, parent=None, apply=None, ok=None, cancel=None, result=None):
        QDialog.__init__(self, parent)
        
        # Destroying the C++ object right after closing the dialog box,
        # otherwise it may be garbage-collected in another QThread
        # (e.g. the editor's analysis thread in Spyder), thus leading to
        # a segmentation fault on UNIX or an application crash on Windows
        self.setAttribute(Qt.WA_DeleteOnClose)

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
        self.result = result
        if self.result in ['OrderedDict', 'JSON']:
            global OrderedDict
            from collections import OrderedDict
            if self.result == 'JSON':
                global json
                import json

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
        layout.addWidget(self.formwidget)
        
        self.float_fields = []
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

        self.setLayout(layout)
        
        self.setWindowTitle(title)
        if not isinstance(icon, QIcon):
            icon = QWidget().style().standardIcon(QStyle.SP_MessageBoxQuestion)
        self.setWindowIcon(icon)
        
    def register_float_field(self, field):
        self.float_fields.append(field)
    
    def update_buttons(self):
        valid = True
        for field in self.float_fields:
            if not is_edit_valid(field):
                valid = False
        for btn_type in (QDialogButtonBox.Ok, QDialogButtonBox.Apply):
            btn = self.bbox.button(btn_type)
            if btn is not None:
                btn.setEnabled(valid)
        
    def accept(self):
        self.data = self.formwidget.get()
        QDialog.accept(self)
        
    def reject(self):
        self.data = None
        QDialog.reject(self)
        
    def apply(self):
        self.apply_callback(self.formwidget.get())
        
    def get(self):
        """Return form result"""
        # It is import to avoid accessing Qt C++ object as it has probably
        # already been destroyed, due to the Qt.WA_DeleteOnClose attribute
        return self.data


def fedit(data, title="", comment="", icon=None, parent=None, apply=None,
          ok=True, cancel=True, result='list'):
    """
    Create form dialog and return result
    (if Cancel button is pressed, return None)
    
    data: datalist, datagroup
    title: string
    comment: string
    icon: QIcon instance
    parent: parent QWidget
    apply: apply callback (function or tuple (label, function))
    ok: customized ok button label
    cancel: customized cancel button label
    result: result serialization ('list', 'dict', 'OrderedDict' and 'JSON')
    
    datalist: list/tuple of (field_name, field_value)
    datagroup: list/tuple of (datalist *or* datagroup, title, comment)
    
    -> one field for each member of a datalist
    -> one tab for each member of a top-level datagroup
    -> one page (of a multipage widget, each page can be selected with a combo
       box) for each member of a datagroup inside a datagroup
       
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

    dialog = FormDialog(data, title, comment, icon, parent, apply, ok, cancel, result)
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
