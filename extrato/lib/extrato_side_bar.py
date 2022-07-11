import pandas as pd
import streamlit as st

from extrato.lib.extrato_columns import ExtratoColumnsInterface, ExtratoRawColumns, ExtratoDBColumns
from extrato.lib.extrato_filter import ExtratoFilterInterface, ExtratoRawFilter, ExtratoDBFilter


class ExtratoSideBarInterface:
    def __init__(
        self,
        columns_object: ExtratoColumnsInterface,
        filter_object: ExtratoFilterInterface,
        market_filter = True,
        ticker_filter = True,
        operation_filter = True,
        period_filter = True,
    ) -> None:
        """Structure to draw an 'Extrato Filter' Side Bar.
        
        Args:
        - columns_object: any object instance inherited from 'ExtratoColumnsInterface'
        - filter_object: any object instance inherited from 'ExtratoFilterInterface'
        """
        self.__columns_object = columns_object
        self.__filter_object = filter_object
        self.__market_filter = market_filter
        self.__ticker_filter = ticker_filter
        self.__operation_filter = operation_filter
        self.__period_filter = period_filter
    
    def __showSubHearder(self) -> None:
        st.sidebar.subheader('Filtros')
    
    def __showMarketFilter(self) -> list:
        column = self.__columns_object._market_col.getName()
        market_default_series = self.__filter_object.getDataframe()[column].drop_duplicates()
        market_list_filter = st.sidebar.multiselect('Mercado:', market_default_series.sort_values())
        self.__filter_object.applyMarketFilter(market_list_filter)

    def __showTickerFilter(self) -> str:
        column = self.__columns_object._ticker_col.getName()
        ticker_default_list = ["Exibir todos"]
        ticker_default_list.extend(self.__filter_object.getDataframe()[column].drop_duplicates().sort_values())
        ticker_filter = st.sidebar.selectbox('Ticker:', ticker_default_list)
        self.__filter_object.applyTickerFilter(ticker_filter)

    def __showOperationFilter(self) -> str:
        column = self.__columns_object._operation_col.getName()
        op_default_list = ["Exibir todas"]
        op_default_list.extend(self.__filter_object.getDataframe()[column].drop_duplicates().sort_values())
        operation_filter = st.sidebar.selectbox('Operação:', op_default_list)
        self.__filter_object.applyOperationFilter(operation_filter)
    
    def __showPeriodFilter(self) -> tuple:
        column = self.__columns_object._date_col.getName()
        start_date = self.__filter_object.getDataframe()[column].min()
        end_date = self.__filter_object.getDataframe()[column].max()
        if self.__filter_object.getDataframe().empty:
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
        self.__filter_object.applyDateFilter(init_date, finish_date)
    
    def __showSideBar(self) -> None:
        self.__showSubHearder()
        if self.__market_filter:
            self.__showMarketFilter()
        if self.__ticker_filter:
            self.__showTickerFilter()
        if self.__operation_filter:
            self.__showOperationFilter()
        if self.__period_filter:
            self.__showPeriodFilter()
    
    def updateDataframe(self, file) -> None:
        self.__filter_object.updateDataframe(file)
        self.__showSideBar()
    
    def getFilteredDataframe(self) -> pd.DataFrame:
        return self.__filter_object.getDataframe().copy()
    
    def getFilteredFormattedDataframe(self) -> pd.DataFrame:
        return self.__filter_object.getFormattedDataframe().copy()


class ExtratoRawSideBar(ExtratoSideBarInterface):
    def __init__(
        self,
        market_filter = True,
        ticker_filter = True,
        operation_filter = True,
        period_filter = True,
    ) -> None:
        """Structure to draw an Extrato Filter's Side Bar."""
        self.__columns_object = ExtratoRawColumns()
        self.__filter_object = ExtratoRawFilter()
        super().__init__(
            self.__columns_object, self.__filter_object,
            market_filter, ticker_filter, operation_filter, period_filter,
        )


class ExtratoDBSideBar(ExtratoSideBarInterface):
    def __init__(
        self,
        market_filter = True,
        ticker_filter = True,
        operation_filter = True,
        period_filter = True,
    ) -> None:
        """Structure to draw an Extrato Filter's Side Bar."""
        self.__columns_object = ExtratoDBColumns()
        self.__filter_object = ExtratoDBFilter()
        super().__init__(
            self.__columns_object, self.__filter_object,
            market_filter, ticker_filter, operation_filter, period_filter,
        )
