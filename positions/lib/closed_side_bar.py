import pandas as pd
import streamlit as st

from positions.lib.closed_columns import ClosedPositionColumns
from positions.lib.closed_filter import ClosedPositionFilter


class ClosedPositionSideBar:
    def __init__(
        self,
        market_filter = True,
        ticker_filter = True,
        period_filter = True,
    ) -> None:
        """Structure to draw a 'Closed Position Filter' Side Bar.
        
        Args:
        - columns_object: any object instance inherited from 'ClosedPositionDBColumns'
        - filter_object: any object instance inherited from 'ClosedPositionDBFilter'
        """
        self.__columns_object = ClosedPositionColumns()
        self.__filter_object = ClosedPositionFilter()
        self.__market_filter = market_filter
        self.__ticker_filter = ticker_filter
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
    
    def __showPeriodFilter(self) -> tuple:
        initial_date_column = self.__columns_object._initial_date_col.getName()
        final_date_column = self.__columns_object._final_date_col.getName()
        start_date = self.__filter_object.getDataframe()[initial_date_column].min()
        end_date = self.__filter_object.getDataframe()[final_date_column].max()
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
        self.__filter_object.applyPeriodFilter(init_date, finish_date)
    
    def __showSideBar(self) -> None:
        self.__showSubHearder()
        if self.__market_filter:
            self.__showMarketFilter()
        if self.__ticker_filter:
            self.__showTickerFilter()
        if self.__period_filter:
            self.__showPeriodFilter()
    
    def updateDataframe(self, dataframe: pd.DataFrame) -> None:
        self.__filter_object.updateDataframe(dataframe)
        self.__showSideBar()
    
    def getFilteredDataframe(self) -> pd.DataFrame:
        return self.__filter_object.getDataframe().copy()
    
    def getFilteredFormattedDataframe(self) -> pd.DataFrame:
        return self.__filter_object.getFormattedDataframe().copy()
