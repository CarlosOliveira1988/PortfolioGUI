import pandas as pd
import streamlit as st

from extrato.lib.extrato_columns import ExtratoColumns
from extrato.lib.extrato_dataframes_kit import ExtratoKit
from extrato.lib.extrato_side_bar import ExtratoSideBar


class ExtratoRawTableInfo:
    def __init__(self) -> None:
        """Structure used to show an interactive table related to the 'Extrato'."""
        self.__filtered_fmtdf = ExtratoKit().getFormattedDataframe()
        self.__hideColumns()

    def __hideColumns(self):
        extrato_columns = ExtratoColumns()
        self.__columns_list = extrato_columns.getColumnsNameList()
        self.__columns_list.remove(extrato_columns._contributions_col.getName())
        self.__columns_list.remove(extrato_columns._rescues_col.getName())
        self.__columns_list.remove(extrato_columns._buy_price_col.getName())
        self.__columns_list.remove(extrato_columns._sell_price_col.getName())
        self.__columns_list.remove(extrato_columns._slice_index_col.getName())
        self.__columns_list.remove(extrato_columns._slice_type_col.getName())

    def __showMainTitle(self) -> None:
        st.write('#### Histórico de transações')
    
    def __showColumnsViewer(self):
        # First columns filter to limit the columns displayed
        self.__filtered_fmtdf = self.__filtered_fmtdf[self.__columns_list]
        
        # Additional columns filter that works according to the user selection
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
        self.__side_bar = ExtratoSideBar()
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
