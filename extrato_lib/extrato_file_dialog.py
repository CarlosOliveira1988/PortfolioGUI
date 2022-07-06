"""Workaround to open files using the PyQt instead of Streamlit.

Unfortunately, Streamlit library does not return the file path when using the 'file_uploader' component.

I tried some alternatives but I failed in all of them.

This is the better I could achieve up until now.
"""

import sys
from PyQt5 import QtWidgets
from extrato_file_manager import FileManager


class FileDialogWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.__file_manager = FileManager()

    def runFileDialog(self):
        message = "Selecione o arquivo XLSX relacionado ao portfolio"
        file_name_tuple = QtWidgets.QFileDialog.getOpenFileName(self, message, sys.path[0], "xlsx(*.xlsx)")
        file_name = file_name_tuple[0]
        if ".xlsx" in file_name:
            self.__file_manager.setExtratoFile(file_name)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    file_dialog = FileDialogWindow()
    file_dialog.runFileDialog()
    sys.exit()
