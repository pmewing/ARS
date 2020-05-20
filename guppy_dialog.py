# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guppy_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        # Dialog.setGeometry(1400, 500)
        # Dialog.resize(1400, 500)
        self.guppy_output_folder_label = QtWidgets.QLabel(Dialog)
        self.guppy_output_folder_label.setGeometry(QtCore.QRect(700, 120, 671, 34))
        self.guppy_output_folder_label.setObjectName("guppy_output_folder_label")
        self.guppy_reference_sequence_button = QtWidgets.QPushButton(Dialog)
        self.guppy_reference_sequence_button.setGeometry(QtCore.QRect(70, 190, 425, 48))
        self.guppy_reference_sequence_button.setObjectName("guppy_reference_sequence_button")
        self.guppy_input_folder_button = QtWidgets.QPushButton(Dialog)
        self.guppy_input_folder_button.setGeometry(QtCore.QRect(70, 50, 300, 48))
        self.guppy_input_folder_button.setObjectName("guppy_input_folder_button")
        self.guppy_reference_file_label = QtWidgets.QLabel(Dialog)
        self.guppy_reference_file_label.setGeometry(QtCore.QRect(700, 190, 671, 34))
        self.guppy_reference_file_label.setObjectName("guppy_reference_file_label")
        self.guppy_output_folder_button = QtWidgets.QPushButton(Dialog)
        self.guppy_output_folder_button.setGeometry(QtCore.QRect(70, 120, 325, 48))
        self.guppy_output_folder_button.setObjectName("guppy_output_folder_button")
        self.guppy_input_folder_label = QtWidgets.QLabel(Dialog)
        self.guppy_input_folder_label.setGeometry(QtCore.QRect(700, 50, 672, 34))
        self.guppy_input_folder_label.setObjectName("guppy_input_folder_label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.guppy_output_folder_label.setText(_translate("Dialog", "Save Location"))
        self.guppy_reference_sequence_button.setText(_translate("Dialog", "Reference Sequence Location"))
        self.guppy_input_folder_button.setText(_translate("Dialog", "Input Folder Location"))
        self.guppy_reference_file_label.setText(_translate("Dialog", "Save Location"))
        self.guppy_output_folder_button.setText(_translate("Dialog", "Output Folder Location"))
        self.guppy_input_folder_label.setText(_translate("Dialog", "Save Location"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

