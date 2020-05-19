# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GuppyAnalysis.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GuppyAlignmentUI(object):
    def setupUi(self, GuppyAlignmentUI):
        GuppyAlignmentUI.setObjectName("GuppyAlignmentUI")
        GuppyAlignmentUI.resize(1400, 500)
        self.centralwidget = QtWidgets.QWidget(GuppyAlignmentUI)
        self.centralwidget.setObjectName("centralwidget")
        self.guppy_input_folder_label = QtWidgets.QLabel(self.centralwidget)
        self.guppy_input_folder_label.setGeometry(QtCore.QRect(700, 50, 672, 34))
        self.guppy_input_folder_label.setObjectName("guppy_input_folder_label")
        self.guppy_input_folder_button = QtWidgets.QPushButton(self.centralwidget)
        self.guppy_input_folder_button.setGeometry(QtCore.QRect(70, 50, 300, 48))
        self.guppy_input_folder_button.setObjectName("guppy_input_folder_button")
        self.guppy_output_folder_label = QtWidgets.QLabel(self.centralwidget)
        self.guppy_output_folder_label.setGeometry(QtCore.QRect(700, 120, 671, 34))
        self.guppy_output_folder_label.setObjectName("guppy_output_folder_label")
        self.guppy_output_folder_button = QtWidgets.QPushButton(self.centralwidget)
        self.guppy_output_folder_button.setGeometry(QtCore.QRect(70, 120, 325, 48))
        self.guppy_output_folder_button.setObjectName("guppy_output_folder_button")
        self.guppy_reference_file_label = QtWidgets.QLabel(self.centralwidget)
        self.guppy_reference_file_label.setGeometry(QtCore.QRect(700, 190, 671, 34))
        self.guppy_reference_file_label.setObjectName("guppy_reference_file_label")
        self.guppy_reference_sequence_button = QtWidgets.QPushButton(self.centralwidget)
        self.guppy_reference_sequence_button.setGeometry(QtCore.QRect(70, 190, 425, 48))
        self.guppy_reference_sequence_button.setObjectName("guppy_reference_sequence_button")
        GuppyAlignmentUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(GuppyAlignmentUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 39))
        self.menubar.setObjectName("menubar")
        GuppyAlignmentUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(GuppyAlignmentUI)
        self.statusbar.setObjectName("statusbar")
        GuppyAlignmentUI.setStatusBar(self.statusbar)

        self.retranslateUi(GuppyAlignmentUI)
        QtCore.QMetaObject.connectSlotsByName(GuppyAlignmentUI)

    def retranslateUi(self, GuppyAlignmentUI):
        _translate = QtCore.QCoreApplication.translate
        GuppyAlignmentUI.setWindowTitle(_translate("GuppyAlignmentUI", "MainWindow"))
        self.guppy_input_folder_label.setText(_translate("GuppyAlignmentUI", "Save Location"))
        self.guppy_input_folder_button.setText(_translate("GuppyAlignmentUI", "Input Folder Location"))
        self.guppy_output_folder_label.setText(_translate("GuppyAlignmentUI", "Save Location"))
        self.guppy_output_folder_button.setText(_translate("GuppyAlignmentUI", "Output Folder Location"))
        self.guppy_reference_file_label.setText(_translate("GuppyAlignmentUI", "Save Location"))
        self.guppy_reference_sequence_button.setText(_translate("GuppyAlignmentUI", "Reference Sequence Location"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    GuppyAlignmentUI = QtWidgets.QMainWindow()
    ui = Ui_GuppyAlignmentUI()
    ui.setupUi(GuppyAlignmentUI)
    GuppyAlignmentUI.show()
    sys.exit(app.exec_())

