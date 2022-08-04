import streamlit as st

from extrato.lib.extrato_xls_reader import ExtratoExcelReader


class SessionStateControl:
    def __init__(self) -> None:
        """Structure used to control the Session State parameters related to Streamlit.
        
        Session States in Streamlit work as global variables and they are acessed maily by the Streamlit Pages.
        """
        self.__xls_reader = ExtratoExcelReader()

    def setUploadedFile(self, uploaded_file) -> None:
        if uploaded_file is not None:
            self.__xls_reader.readExcelFile(uploaded_file)
            st.session_state.extrato_file = uploaded_file
            st.session_state.extrato_from_excel = self.__xls_reader.getRawDataframe()


class ExtratoGuiWeb:
    def __init__(self) -> None:
        """Structure used to open files related to Extrato in 'Streamlit Cloud'.
        
        When running in 'Streamlit Cloud', the user needs to push manually the Extrato file in every iteraction.
        For now, I don't know how to do user file management in 'Streamlit Cloud'.
        """
        self.__session_control = SessionStateControl()
        self.__showInfo()

    def __showMainTitle(self) -> None:
        st.write('# Extrato')

    def __showFileUploader(self) -> None:
        uploaded_file = st.file_uploader('Selecione o arquivo Extrato: ', type=[".xls", ".xlsx"])
        self.__session_control.setUploadedFile(uploaded_file)

    def __showInfo(self) -> None:
        self.__showMainTitle()
        self.__showFileUploader()


if __name__ == "__main__":
    extrato_gui = ExtratoGuiWeb()
