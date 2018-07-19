# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'comdialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_COMDialog(object):
    def setupUi(self, COMDialog):
        COMDialog.setObjectName(_fromUtf8("COMDialog"))
        COMDialog.resize(367, 176)
        self.verticalLayout = QtGui.QVBoxLayout(COMDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formScreen = QtGui.QFormLayout()
        self.formScreen.setObjectName(_fromUtf8("formScreen"))
        self.labelCOMName = QtGui.QLabel(COMDialog)
        self.labelCOMName.setObjectName(_fromUtf8("labelCOMName"))
        self.formScreen.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelCOMName)
        self.leCOMName = QtGui.QLineEdit(COMDialog)
        self.leCOMName.setObjectName(_fromUtf8("leCOMName"))
        self.formScreen.setWidget(0, QtGui.QFormLayout.FieldRole, self.leCOMName)
        self.labelCOMLink = QtGui.QLabel(COMDialog)
        self.labelCOMLink.setObjectName(_fromUtf8("labelCOMLink"))
        self.formScreen.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelCOMLink)
        self.cbCOMLink = QtGui.QComboBox(COMDialog)
        self.cbCOMLink.setObjectName(_fromUtf8("cbCOMLink"))
        self.formScreen.setWidget(1, QtGui.QFormLayout.FieldRole, self.cbCOMLink)
        self.labelCOMSignal = QtGui.QLabel(COMDialog)
        self.labelCOMSignal.setObjectName(_fromUtf8("labelCOMSignal"))
        self.formScreen.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelCOMSignal)
        self.leCOMSignal = QtGui.QLineEdit(COMDialog)
        self.leCOMSignal.setMaxLength(1)
        self.leCOMSignal.setObjectName(_fromUtf8("leCOMSignal"))
        self.formScreen.setWidget(2, QtGui.QFormLayout.FieldRole, self.leCOMSignal)
        self.labelCOMRules = QtGui.QLabel(COMDialog)
        self.labelCOMRules.setObjectName(_fromUtf8("labelCOMRules"))
        self.formScreen.setWidget(4, QtGui.QFormLayout.LabelRole, self.labelCOMRules)
        self.cbCOMRules = QtGui.QComboBox(COMDialog)
        self.cbCOMRules.setObjectName(_fromUtf8("cbCOMRules"))
        self.formScreen.setWidget(4, QtGui.QFormLayout.FieldRole, self.cbCOMRules)
        self.labelCOMBaudRate = QtGui.QLabel(COMDialog)
        self.labelCOMBaudRate.setObjectName(_fromUtf8("labelCOMBaudRate"))
        self.formScreen.setWidget(3, QtGui.QFormLayout.LabelRole, self.labelCOMBaudRate)
        self.leCOMBaudRate = QtGui.QLineEdit(COMDialog)
        self.leCOMBaudRate.setMaxLength(5)
        self.leCOMBaudRate.setObjectName(_fromUtf8("leCOMBaudRate"))
        self.formScreen.setWidget(3, QtGui.QFormLayout.FieldRole, self.leCOMBaudRate)
        self.verticalLayout.addLayout(self.formScreen)
        self.bbScreen = QtGui.QDialogButtonBox(COMDialog)
        self.bbScreen.setOrientation(QtCore.Qt.Horizontal)
        self.bbScreen.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbScreen.setObjectName(_fromUtf8("bbScreen"))
        self.verticalLayout.addWidget(self.bbScreen)

        self.retranslateUi(COMDialog)
        QtCore.QObject.connect(self.bbScreen, QtCore.SIGNAL(_fromUtf8("accepted()")), COMDialog.accept)
        QtCore.QObject.connect(self.bbScreen, QtCore.SIGNAL(_fromUtf8("rejected()")), COMDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(COMDialog)

    def retranslateUi(self, COMDialog):
        COMDialog.setWindowTitle(_translate("COMDialog", "Dialog", None))
        self.labelCOMName.setText(_translate("COMDialog", "TextLabel", None))
        self.labelCOMLink.setText(_translate("COMDialog", "TextLabel", None))
        self.labelCOMSignal.setText(_translate("COMDialog", "TextLabel", None))
        self.labelCOMRules.setText(_translate("COMDialog", "TextLabel", None))
        self.labelCOMBaudRate.setText(_translate("COMDialog", "TextLabel", None))

