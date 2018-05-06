# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'crawlingform.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(570, 573)
        self.textBrowser = QtWidgets.QTextBrowser(widget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 551, 121))
        self.textBrowser.setObjectName("textBrowser")
        self.listView = QtWidgets.QListView(widget)
        self.listView.setGeometry(QtCore.QRect(10, 140, 301, 421))
        self.listView.setObjectName("listView")
        self.pushButton = QtWidgets.QPushButton(widget)
        self.pushButton.setGeometry(QtCore.QRect(320, 510, 231, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(widget)
        self.pushButton_2.setGeometry(QtCore.QRect(320, 450, 231, 51))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "크롤링"))
        self.pushButton.setText(_translate("widget", "확인"))
        self.pushButton_2.setText(_translate("widget", "저장하기"))

