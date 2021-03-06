import os

import streamlit as st

from extrato_lib.extrato_file_manager import FileManager


class ExtratoGuiLocal:
    def __init__(self) -> None:
        """Structure used to open files related to Extrato.
        
        When running in 'Local Environment', the Extrato file management is done by the 'FileManager' class.
        In 'Local Environment' mode, the applications needs to know the user Extrato file path.
        Due some 'Streamlit' limitation, the user needs to reset the script every time he sets a new Extrato file
        or the file is updated.
        
        The 'FileManager' works based on '.env' files:
        - If the '.env' file does not exist, create a new one with the Extrato empty template path
        - If the '.env' file already exists, then uses the last saved Extrato spreadsheet path
        """
        self.file_manager = FileManager()
        st.session_state.extrato_file = self.file_manager.getExtratoFile()
        self.__showInfo()

    def __showMainTitle(self) -> None:
        st.write('# Extrato')

    def __showFolderSelector(self) -> None:
        folder_path_default = os.path.dirname(st.session_state.extrato_file)
        self.folder_path = st.text_input(
            "Digite no campo o local do arquivo Extrato: ",
            value = folder_path_default,
        )

    def __showFileSelector(self):
        filenames = [file for file in os.listdir(self.folder_path) if file.endswith((".xls", ".xlsx"))]
        selected_filename = st.selectbox('Selecione o arquivo Extrato: ', filenames)
        self.file_path = os.path.join(self.folder_path, selected_filename)

    def __showSelectedFile(self):
        st.write('Planilha atual: ', st.session_state.extrato_file)

    def __showUpdateFileButton(self):
        if st.button("Selecionar"):
            self.__updateExtratoFile()

    def __updateExtratoFile(self):
        if os.path.isfile(self.file_path):
            if self.file_path != st.session_state.extrato_file:
                self.file_manager.setExtratoFile(self.file_path)
                # At this point, 'st.session_state.extrato_file' is an "string" object
                st.session_state.extrato_file = self.file_manager.getExtratoFile()
                self.__showBadBehaviorInfo()

    def __showBadBehaviorInfo(self):
        st.write('Planilha selecionada: ', st.session_state.extrato_file)
        st.markdown(
            """
            :disappointed_relieved: Por limita????es do Streamlit, ainda n??o resolvidas...
            
            :sweat_smile: **Por favor, reinicie a aplica????o para carregar o novo arquivo!**
            ?? necess??rio fechar tanto a p??gina quanto o prompt de comandos.
            """
        )
        st.stop()

    def __showInfo(self) -> None:
        self.__showMainTitle()
        self.__showFolderSelector()
        self.__showFileSelector()
        self.__showSelectedFile()
        self.__showUpdateFileButton()


if __name__ == "__main__":
    extrato_gui = ExtratoGuiLocal()
