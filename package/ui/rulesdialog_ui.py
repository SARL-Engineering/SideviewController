# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rulesdialog.ui'
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

class Ui_rulesDialog(object):
    def setupUi(self, rulesDialog):
        rulesDialog.setObjectName(_fromUtf8("rulesDialog"))
        rulesDialog.resize(367, 150)
        self.verticalLayout = QtGui.QVBoxLayout(rulesDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formScreen = QtGui.QFormLayout()
        self.formScreen.setObjectName(_fromUtf8("formScreen"))
        self.labelRuleNum = QtGui.QLabel(rulesDialog)
        self.labelRuleNum.setObjectName(_fromUtf8("labelRuleNum"))
        self.formScreen.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelRuleNum)
        self.leRuleNum = QtGui.QLineEdit(rulesDialog)
        self.leRuleNum.setReadOnly(True)
        self.leRuleNum.setObjectName(_fromUtf8("leRuleNum"))
        self.formScreen.setWidget(0, QtGui.QFormLayout.FieldRole, self.leRuleNum)
        self.rbRuleAt = QtGui.QRadioButton(rulesDialog)
        self.rbRuleAt.setObjectName(_fromUtf8("rbRuleAt"))
        self.formScreen.setWidget(1, QtGui.QFormLayout.LabelRole, self.rbRuleAt)
        self.rbRuleEvery = QtGui.QRadioButton(rulesDialog)
        self.rbRuleEvery.setObjectName(_fromUtf8("rbRuleEvery"))
        self.formScreen.setWidget(2, QtGui.QFormLayout.LabelRole, self.rbRuleEvery)
        self.teRuleAt = QtGui.QTimeEdit(rulesDialog)
        self.teRuleAt.setObjectName(_fromUtf8("teRuleAt"))
        self.formScreen.setWidget(1, QtGui.QFormLayout.FieldRole, self.teRuleAt)
        self.teRuleEvery = QtGui.QTimeEdit(rulesDialog)
        self.teRuleEvery.setObjectName(_fromUtf8("teRuleEvery"))
        self.formScreen.setWidget(2, QtGui.QFormLayout.FieldRole, self.teRuleEvery)
        self.verticalLayout.addLayout(self.formScreen)
        self.pbRuleRemove = QtGui.QPushButton(rulesDialog)
        self.pbRuleRemove.setObjectName(_fromUtf8("pbRuleRemove"))
        self.verticalLayout.addWidget(self.pbRuleRemove)
        self.bbScreen = QtGui.QDialogButtonBox(rulesDialog)
        self.bbScreen.setOrientation(QtCore.Qt.Horizontal)
        self.bbScreen.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbScreen.setObjectName(_fromUtf8("bbScreen"))
        self.verticalLayout.addWidget(self.bbScreen)

        self.retranslateUi(rulesDialog)
        QtCore.QObject.connect(self.bbScreen, QtCore.SIGNAL(_fromUtf8("accepted()")), rulesDialog.accept)
        QtCore.QObject.connect(self.bbScreen, QtCore.SIGNAL(_fromUtf8("rejected()")), rulesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(rulesDialog)

    def retranslateUi(self, rulesDialog):
        rulesDialog.setWindowTitle(_translate("rulesDialog", "Dialog", None))
        self.labelRuleNum.setText(_translate("rulesDialog", "TextLabel", None))
        self.rbRuleAt.setText(_translate("rulesDialog", "RadioButton", None))
        self.rbRuleEvery.setText(_translate("rulesDialog", "RadioButton", None))
        self.teRuleAt.setDisplayFormat(_translate("rulesDialog", "hh:mm:ss", None))
        self.teRuleEvery.setDisplayFormat(_translate("rulesDialog", "hh:mm:ss", None))
        self.pbRuleRemove.setText(_translate("rulesDialog", "PushButton", None))

