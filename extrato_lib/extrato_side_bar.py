import pandas as pd
import streamlit as st

from extrato_lib.extrato_columns import ExtratoColumns
from extrato_lib.extrato_filter import ExtratoFilter


class ExtratoSideBar:
    def __init__(self):
        """Structure to draw an Extrato Filter's Side Bar."""
        self.__columns_object = ExtratoColumns()
        self.__date_filter = ExtratoFilter()
        self.__any_filter = ExtratoFilter()
    
    def __showSubHearder(self) -> None:
        st.sidebar.subheader('Filtros')
    
    def __showMarketFilter(self) -> list:
        column = self.__columns_object._market_col.getName()
        market_default_series = self.__any_filter.getDataframe()[column].drop_duplicates()
        market_list_filter = st.sidebar.multiselect('Mercado:', market_default_series.sort_values())
        self.__any_filter.applyMarketFilter(market_list_filter)

    def __showTickerFilter(self) -> str:
        column = self.__columns_object._ticker_col.getName()
        ticker_default_list = ["Exibir todos"]
        ticker_default_list.extend(self.__any_filter.getDataframe()[column].drop_duplicates().sort_values())
        ticker_filter = st.sidebar.selectbox('Ticker:', ticker_default_list)
        self.__any_filter.applyTickerFilter(ticker_filter)

    def __showOperationFilter(self) -> str:
        column = self.__columns_object._operation_col.getName()
        op_default_list = ["Exibir todas"]
        op_default_list.extend(self.__any_filter.getDataframe()[column].drop_duplicates().sort_values())
        operation_filter = st.sidebar.selectbox('Operação:', op_default_list)
        self.__any_filter.applyOperationFilter(operation_filter)
    
    def __showDateFilter(self) -> tuple:
        column = self.__columns_object._date_col.getName()
        start_date = self.__any_filter.getDataframe()[column].min()
        end_date = self.__any_filter.getDataframe()[column].max()
        if self.__any_filter.getDataframe().empty:
            date_option = st.sidebar.slider('Período:', disabled=True)
            init_date = None
            finish_date = None
        elif start_date == end_date:
            date_option = st.sidebar.slider('Período:', disabled=True)
            init_date = date_option
            finish_date = date_option
        else:
            date_option = st.sidebar.slider('Período:', min_value=start_date, max_value=end_date, value=(start_date, end_date))
            init_date = date_option[0]
            finish_date = date_option[1]
        self.__any_filter.applyDateFilter(init_date, finish_date)
        self.__date_filter.applyDateFilter(init_date, finish_date)
    
    def __showSideBar(self) -> None:
        self.__showSubHearder()
        self.__showMarketFilter()
        self.__showTickerFilter()
        self.__showOperationFilter()
        self.__showDateFilter()
    
    def updateDataframe(self, file) -> None:
        self.__date_filter.updateDataframe(file)
        self.__any_filter.updateDataframe(file)
        self.__showSideBar()
    
    def getFilteredDataframe(self) -> pd.DataFrame:
        return self.__any_filter.getDataframe().copy()
    
    def getFilteredFormattedDataframe(self) -> pd.DataFrame:
        return self.__any_filter.getFormattedDataframe().copy()

    def getDateFilteredDataframe(self) -> pd.DataFrame:
        return self.__date_filter.getDataframe().copy()
    
    def getDateFilteredFormattedDataframe(self) -> pd.DataFrame:
        return self.__date_filter.getFormattedDataframe().copy()
