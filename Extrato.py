import os

import streamlit as st

from subprocess import call

from extrato_lib.extrato_file_manager import FileManager


class ExtratoGUI:
    def __init__(self) -> None:
        """Structure used to open files related to Extrato.
        
        The 'FileManager' is used in the entire project when handling Extrato spreadsheet path.
        It works based on '.env' files:
        - If the '.env' file does not exist, create a new one with the Extrato spreadsheet path.
        - If the '.env' file already exists, then uses the saved Extrato spreadsheet path.
        """
        self.__showInfo()

    def __showMainTitle(self) -> None:
        st.write('# Extrato')

    def __showFileSelector(self) -> None:
        clicked = st.button("Carregar planilha")
        if clicked:
            self.__openFile()
        st.write('Planilha atual: ', st.session_state.extrato_file)

    def __showInfo(self) -> None:
        self.__showMainTitle()
        self.__showFileSelector()

    def __openFile(self):
        # Workaround to open files using the PyQt instead of Streamlit
        # Unfortunately, Streamlit library does not return the file path
        # when using the 'file_uploader' component
        file_path = os.path.join(os.getcwd(), "extrato_lib", "extrato_file_dialog.py")
        call(["python", file_path])
        file_manager = FileManager()
        st.session_state.extrato_file = file_manager.getExtratoFile()
        st.markdown(
            """
            :disappointed_relieved: Por limitações do Streamlit, ainda não resolvidas...
            
            :sweat_smile: **Por favor, reinicie a aplicação para carregar o novo arquivo!**
            É necessário fechar a página e também o prompt de comandos.
            """
        )
        st.stop()


file_manager = FileManager()
st.session_state.extrato_file = file_manager.getExtratoFile()

extrato_gui = ExtratoGUI()
