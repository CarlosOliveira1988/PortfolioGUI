import easygui
import streamlit as st

from extrato_lib.extrato_file_manager import FileManager


class ExtratoGUI:
    def __init__(self) -> None:
        """Structure used to open files related to Extrato.
        
        The 'FileManager' is used in the entire project when handling Extrato spreadsheet path.
        It works based on '.env' files:
        - If the '.env' file does not exist, create a new one with the Extrato spreadsheet path.
        - If the '.env' file already exists, then uses the saved Extrato spreadsheet path.
        """
        self.file_manager = FileManager()
        st.session_state.extrato_file = self.file_manager.getExtratoFile()
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
        file_path = easygui.fileopenbox(
            "Selecione o arquivo XLSX relacionado ao portfolio",
            filetypes = ["*.xlsx", "*.xls"]
        )
        if file_path:
            self.file_manager.setExtratoFile(file_path)
            st.session_state.extrato_file = self.file_manager.getExtratoFile()
            st.markdown(
                """
                :disappointed_relieved: Por limitações do Streamlit, ainda não resolvidas...
                
                :sweat_smile: **Por favor, reinicie a aplicação para carregar o novo arquivo!**
                É necessário fechar tanto a página quanto o prompt de comandos.
                """
            )
            st.stop()


extrato_gui = ExtratoGUI()
