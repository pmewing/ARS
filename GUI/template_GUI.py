# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'template_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.barcode_parent_label = QtWidgets.QLabel(self.centralwidget)
        self.barcode_parent_label.setGeometry(QtCore.QRect(700, 50, 671, 34))
        self.barcode_parent_label.setObjectName("barcode_parent_label")

        self.barcode_parent_button = QtWidgets.QPushButton(self.centralwidget)
        self.barcode_parent_button.setGeometry(QtCore.QRect(70, 50, 425, 48))
        self.barcode_parent_button.setObjectName("barcode_parent_button")

        self.merged_reads_button = QtWidgets.QPushButton(self.centralwidget)
        self.merged_reads_button.setGeometry(QtCore.QRect(70, 120, 525, 48))
        self.merged_reads_button.setObjectName("merged_reads_button")

        self.merged_reads_label = QtWidgets.QLabel(self.centralwidget)
        self.merged_reads_label.setGeometry(QtCore.QRect(700, 130, 671, 34))
        self.merged_reads_label.setObjectName("merged_reads_label")

        self.analyze_button = QtWidgets.QPushButton(self.centralwidget)
        self.analyze_button.setGeometry(QtCore.QRect(625, 350, 150, 48))
        self.analyze_button.setObjectName("analyze_button")

        self.guppy_alignment = QtWidgets.QPushButton(self.centralwidget)
        self.guppy_alignment.setGeometry(QtCore.QRect(70, 190, 250, 48))
        self.guppy_alignment.setObjectName("guppy_alignment")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 39))
        self.menubar.setObjectName("menubar")

        self.menuMethods = QtWidgets.QMenu(self.menubar)
        self.menuMethods.setObjectName("menuMethods")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionGuppy_Alignment = QtWidgets.QAction(MainWindow)
        self.actionGuppy_Alignment.setObjectName("actionGuppy_Alignment")

        self.actionCount_Reads = QtWidgets.QAction(MainWindow)
        self.actionCount_Reads.setObjectName("actionCount_Reads")

        self.actionMerge_Files = QtWidgets.QAction(MainWindow)
        self.actionMerge_Files.setObjectName("actionMerge_Files")

        self.menuMethods.addAction(self.actionCount_Reads)
        self.menuMethods.addAction(self.actionMerge_Files)
        self.menubar.addAction(self.menuMethods.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.barcode_parent_label.setText(_translate("MainWindow", "Save Location"))
        self.barcode_parent_button.setText(_translate("MainWindow", "Select Barcode Parent Folder"))
        self.merged_reads_button.setText(_translate("MainWindow", "Select Save Location of Merged Reads"))
        self.merged_reads_label.setText(_translate("MainWindow", "Save Location"))
        self.analyze_button.setText(_translate("MainWindow", "Analyze"))
        self.guppy_alignment.setText(_translate("MainWindow", "Guppy Alignment"))
        self.menuMethods.setTitle(_translate("MainWindow", "Methods"))
        self.actionGuppy_Alignment.setText(_translate("MainWindow", "Guppy Alignment"))
        self.actionGuppy_Alignment.setToolTip(_translate("MainWindow", "GuppyAlignmentUI"))
        self.actionCount_Reads.setText(_translate("MainWindow", "Count Reads"))
        self.actionMerge_Files.setText(_translate("MainWindow", "Merge Files"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
