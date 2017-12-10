# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'searchform.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(612, 620)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(10, 560, 411, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.listView = QtWidgets.QListView(Form)
        self.listView.setGeometry(QtCore.QRect(10, 20, 341, 501))
        self.listView.setObjectName("listView")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(400, 310, 161, 81))
        self.groupBox.setObjectName("groupBox")
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(70, 50, 91, 22))
        self.comboBox.setEditable(True)
        self.comboBox.setMaxVisibleItems(10)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(380, 20, 201, 271))
        self.graphicsView.setObjectName("graphicsView")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(440, 560, 121, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(370, 470, 101, 51))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Form)
        self.comboBox.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "검색창"))
        self.groupBox.setTitle(_translate("Form", "결과 최대 표시 개수"))
        self.comboBox.setItemText(0, _translate("Form", "1"))
        self.comboBox.setItemText(1, _translate("Form", "2"))
        self.comboBox.setItemText(2, _translate("Form", "3"))
        self.comboBox.setItemText(3, _translate("Form", "4"))
        self.comboBox.setItemText(4, _translate("Form", "5"))
        self.comboBox.setItemText(5, _translate("Form", "6"))
        self.comboBox.setItemText(6, _translate("Form", "7"))
        self.comboBox.setItemText(7, _translate("Form", "8"))
        self.comboBox.setItemText(8, _translate("Form", "9"))
        self.comboBox.setItemText(9, _translate("Form", "10"))
        self.comboBox.setItemText(10, _translate("Form", "11"))
        self.comboBox.setItemText(11, _translate("Form", "12"))
        self.comboBox.setItemText(12, _translate("Form", "13"))
        self.comboBox.setItemText(13, _translate("Form", "14"))
        self.comboBox.setItemText(14, _translate("Form", "15"))
        self.comboBox.setItemText(15, _translate("Form", "16"))
        self.comboBox.setItemText(16, _translate("Form", "17"))
        self.comboBox.setItemText(17, _translate("Form", "18"))
        self.comboBox.setItemText(18, _translate("Form", "19"))
        self.comboBox.setItemText(19, _translate("Form", "20"))
        self.pushButton.setText(_translate("Form", "검색"))
        self.pushButton_2.setText(_translate("Form", "책 선택"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

