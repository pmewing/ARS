# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'count_reads.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1300, 349)

        self.open_directory_button = QtWidgets.QPushButton(Dialog)
        self.open_directory_button.setGeometry(QtCore.QRect(40, 40, 225, 48))
        self.open_directory_button.setObjectName("open_directory_button")

        self.save_directory_button = QtWidgets.QPushButton(Dialog)
        self.save_directory_button.setGeometry(QtCore.QRect(40, 150, 200, 48))
        self.save_directory_button.setObjectName("save_directory_button")

        self.count_reads_button = QtWidgets.QPushButton(Dialog)
        self.count_reads_button.setGeometry(QtCore.QRect(538, 250, 225, 48))
        self.count_reads_button.setObjectName("count_reads_button")

        self.open_directory_label = QtWidgets.QLabel(Dialog)
        self.open_directory_label.setGeometry(QtCore.QRect(350, 40, 129, 34))
        self.open_directory_label.setObjectName("open_directory_label")

        self.save_directory_label = QtWidgets.QLabel(Dialog)
        self.save_directory_label.setGeometry(QtCore.QRect(350, 150, 129, 34))
        self.save_directory_label.setObjectName("save_directory_label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

        self.open_directory_button.setText(_translate("Dialog", "Open Directory"))
        self.save_directory_button.setText(_translate("Dialog", "Save Directory"))
        self.count_reads_button.setText(_translate("Dialog", "Count Reads"))
        self.open_directory_label.setText(_translate("Dialog", "TextLabel"))
        self.save_directory_label.setText(_translate("Dialog", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
