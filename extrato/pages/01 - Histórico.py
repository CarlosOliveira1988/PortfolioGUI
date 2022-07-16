import pandas as pd
import streamlit as st

from extrato.lib.extrato_dataframes_kit import ExtratoRawKit
from extrato.lib.extrato_side_bar import ExtratoRawSideBar


class ExtratoRawTableInfo:
    def __init__(self) -> None:
        """Structure used to show an interactive table related to the 'Extrato'."""
        self.__filtered_fmtdf = ExtratoRawKit().getFormattedDataframe()

    def __showMainTitle(self) -> None:
        st.write('#### Histórico de transações')
    
    def __showDataframe(self) -> None:
        st.write("", self.__filtered_fmtdf.astype(str))

    def setDataframe(self, dataframe: pd.DataFrame) -> None:
        self.__filtered_fmtdf = dataframe
    
    def showInfo(self) -> None:
        self.__showMainTitle()
        self.__showDataframe()


class ExtratoHistoryGUI:
    def __init__(self) -> None:
        """Structure used to show tables and filters related to Extrato."""
        self.__side_bar = ExtratoRawSideBar()
        self.__table = ExtratoRawTableInfo()
        self.__setDataframes()

    def __setDataframes(self) -> None:
        self.__table.setDataframe(self.__side_bar.getFilteredFormattedDataframe())

    def setDataframe(self, file: str) -> None:
        self.__side_bar.updateDataframe(file)
        self.__setDataframes()
        self.__table.showInfo()


history_gui = ExtratoHistoryGUI()
history_gui.setDataframe(st.session_state.extrato_file)
