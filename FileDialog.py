from PyQt5.QtWidgets import QFileDialog, QWidget, QApplication
import sys


class Dialog:
    def __init__(self):
        """
        This class will return the open and save locations using PyQT5's getExistingDirectory funciton

        :param: None
        :return: self.data_dialog, self.save_dialog
        """
        pass

    @staticmethod
    def save_dialog(message: str = "Select the save location", default_dir: str = "/home/joshl/"):
        """
        This will return a directory location for saving output of results
        :return save_dialog - The location to save data
        """
        app = QApplication(sys.argv)
        widget = QWidget()
        save_dialog = QFileDialog.getExistingDirectory(
            parent=widget,
            caption=message,
            directory=default_dir
        )
        return save_dialog

    @staticmethod
    def input_dialog(message: str = "Select the input location", default_dir: str = "/home/joshl/"):
        """
        This will return the input location for data
        :return: data_dialog - The location of data to be used as input for analysis
        """
        app = QApplication(
            sys.argv)
        widget = QWidget()
        data_dialog = QFileDialog.getExistingDirectory(
            parent=widget,
            caption=message,
            directory=default_dir
        )
        return data_dialog
