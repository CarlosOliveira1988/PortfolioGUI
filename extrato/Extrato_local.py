import os

import streamlit as st

from extrato.lib.extrato_file_manager import FileManager

from extrato.Extrato import SessionStateControl


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
        self.__file_manager = FileManager()
        self.__session_control = SessionStateControl()
        self.__session_control.setUploadedFile(self.__file_manager.getExtratoFile())
        self.__showInfo()

    def __showMainTitle(self) -> None:
        st.write('# Extrato')

    def __showFolderSelector(self) -> None:
        folder_path_default = os.path.dirname(st.session_state.extrato_file_path)
        self.__folder_path = st.text_input(
            "Digite no campo o local do arquivo Extrato: ",
            value = folder_path_default,
        )

    def __showFileSelector(self) -> None:
        filenames = [file for file in os.listdir(self.__folder_path) if file.endswith((".xls", ".xlsx"))]
        selected_filename = st.selectbox('Selecione o arquivo Extrato: ', filenames)
        self.__file_path = os.path.join(self.__folder_path, selected_filename)

    def __showSelectedFile(self) -> None:
        st.write('__Planilha atual:__ ', st.session_state.extrato_file_path)

    def __showUpdateFileButton(self) -> None:
        if st.button("Selecionar"):
            self.__updateExtratoFile()

    def __updateExtratoFile(self) -> None:
        if os.path.isfile(self.__file_path):
            if self.__file_path != st.session_state.extrato_file_path:
                self.__file_manager.setExtratoFile(self.__file_path)
                self.__session_control.setUploadedFile(self.__file_manager.getExtratoFile())
                self.__showBadBehaviorInfo()

    def __showBadBehaviorInfo(self) -> None:
        st.write('Planilha selecionada: ', st.session_state.extrato_file_path)
        st.markdown(
            """
            :disappointed_relieved: Por limitações do Streamlit, ainda não resolvidas...
            
            :sweat_smile: **Por favor, reinicie a aplicação para carregar o novo arquivo!**
            É necessário fechar tanto a página quanto o prompt de comandos.
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
