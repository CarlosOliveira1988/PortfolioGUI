import pandas as pd
import streamlit as st

from extrato.lib.extrato_columns import ExtratoRawColumns
from extrato.lib.extrato_dataframes_kit import ExtratoRawKit
from extrato.lib.extrato_side_bar import ExtratoRawSideBar


class ExtratoRawTableInfo:
    def __init__(self) -> None:
        """Structure used to show an interactive table related to the 'Extrato'."""
        self.__filtered_fmtdf = ExtratoRawKit().getFormattedDataframe()
        self.__columns_list = ExtratoRawColumns().getColumnsNameList()

    def __showMainTitle(self) -> None:
        st.write('#### Histórico de transações')
    
    def __showColumnsViewer(self):
        columns_not_displayed = st.multiselect('Ocultar colunas:', self.__columns_list)
        if columns_not_displayed:
            if not self.__filtered_fmtdf.empty:
                columns_displayed = [column for column in self.__columns_list if column not in columns_not_displayed]
                self.__filtered_fmtdf = self.__filtered_fmtdf[columns_displayed]
    
    def __showDataframe(self) -> None:
        st.write("", self.__filtered_fmtdf.astype(str))
        expander = st.expander("Informações:")
        expander.write(
            """A tabela acima é uma cópia da planilha __Extrato__, incluindo todas as transações
            registradas pelo usuário.
            """
        )

    def setDataframe(self, dataframe: pd.DataFrame) -> None:
        self.__filtered_fmtdf = dataframe
    
    def showInfo(self) -> None:
        self.__showMainTitle()
        self.__showColumnsViewer()
        self.__showDataframe()


class ExtratoHistoryGUI:
    def __init__(self) -> None:
        """Structure used to show tables and filters related to Extrato."""
        self.__side_bar = ExtratoRawSideBar()
        self.__table = ExtratoRawTableInfo()
        self.__setDataframes()

    def __setDataframes(self) -> None:
        self.__table.setDataframe(self.__side_bar.getFilteredFormattedDataframe())

    def setDataframe(self, dataframe: pd.DataFrame) -> None:
        self.__side_bar.updateDataframe(dataframe)
        self.__setDataframes()
        self.__table.showInfo()


history_gui = ExtratoHistoryGUI()
history_gui.setDataframe(st.session_state.extrato_dataframe)
