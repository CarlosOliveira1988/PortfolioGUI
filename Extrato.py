import streamlit as st

from common_lib.config import FileManager


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
        st.write('Arquivo: ', st.session_state.extrato_file)

    def __showInfo(self) -> None:
        self.__showMainTitle()
        self.__showFileSelector()

    def __openFile(self):
        # Workaround to open files using the PyQt instead of Streamlit
        # Unfortunately, Streamlit library does not return the file path
        # when using the 'file_uploader' component
        import os
        from subprocess import call
        file_path = os.path.join(os.getcwd(), "common_lib", "file_dialog.py")
        call(["python", file_path])
        file_manager = FileManager()
        st.session_state.extrato_file = file_manager.getExtratoFile()
        st.markdown(
            """Por limitações do Streamlit, ainda não resolvidas, por favor encerre
            e reinicie novamente a aplicação para que o novo arquivo seja carregado.
            """
        )


file_manager = FileManager()
st.session_state.extrato_file = file_manager.getExtratoFile()

extrato_gui = ExtratoGUI()
