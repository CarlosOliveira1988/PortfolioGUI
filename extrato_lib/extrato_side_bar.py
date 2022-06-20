import streamlit as st

from extrato_lib.extrato_dataframe import ExtratoDataframe


class ExtratoSideBar:
    def __init__(self):
        """Structure to draw an Extrato Filter's Side Bar."""
        self.extrato = ExtratoDataframe()
        self.__columns_object = self.extrato.getColumnsObject()
        
        # Dataframes for common usage
        self.__filtered_df = self.extrato.getNotNanDataframe()
        self.__filtered_fmtdf = self.extrato.getFormattedDataframe()
        
        # Dataframes ONLY for Date filtering
        self.__filtered_date_df = self.extrato.getNotNanDataframe()
        self.__filtered_date_fmtdf = self.extrato.getFormattedDataframe()
    
    def __showSubHearder(self) -> None:
        st.sidebar.subheader('Filtros')
    
    def __showMarketFilter(self) -> list:
        column = self.__columns_object._market_col.getName()
        market_default_series = self.__filtered_df[column].drop_duplicates()
        self.__market_list_filter = st.sidebar.multiselect('Mercado:', market_default_series.sort_values())
        self.__applyMarketFilter()

    def __showTickerFilter(self) -> str:
        column = self.__columns_object._ticker_col.getName()
        ticker_default_list = ["Exibir todos"]
        ticker_default_list.extend(self.__filtered_df[column].drop_duplicates().sort_values())
        self.__ticker_option_str_filter = st.sidebar.selectbox('Ticker:', ticker_default_list)
        self.__applyTickerFilter()

    def __showOperationFilter(self) -> str:
        column = self.__columns_object._operation_col.getName()
        op_default_list = ["Exibir todas"]
        op_default_list.extend(self.__filtered_df[column].drop_duplicates().sort_values())
        self.__operation_option_str_filter = st.sidebar.selectbox('Operação:', op_default_list)
        self.__applyOperationFilter()
    
    def __showDateFilter(self) -> tuple:
        column = self.__columns_object._date_col.getName()
        start_date = self.__filtered_df[column].min()
        end_date = self.__filtered_df[column].max()
        if self.__filtered_df.empty:
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
        self.__start_date, self.__end_date = init_date, finish_date
        self.__applyDateFilter()
    
    def __showSideBar(self) -> None:
        self.__showSubHearder()
        self.__showMarketFilter()
        self.__showTickerFilter()
        self.__showOperationFilter()
        self.__showDateFilter()
    
    def __applyMarketFilter(self) -> None:
        column = self.__columns_object._market_col.getName()
        if self.__market_list_filter:
            self.__filtered_df = self.__filtered_df.loc[self.__filtered_df[column].isin(self.__market_list_filter)]
            self.__filtered_fmtdf = self.__filtered_fmtdf.loc[self.__filtered_fmtdf[column].isin(self.__market_list_filter)]
    
    def __applyTickerFilter(self) -> None:
        column = self.__columns_object._ticker_col.getName()
        if self.__ticker_option_str_filter != "Exibir todos":
            self.__filtered_df = self.__filtered_df.loc[self.__filtered_df[column] == self.__ticker_option_str_filter]
            self.__filtered_fmtdf = self.__filtered_fmtdf.loc[self.__filtered_fmtdf[column] == self.__ticker_option_str_filter]
    
    def __applyOperationFilter(self) -> None:
        column = self.__columns_object._operation_col.getName()
        if self.__operation_option_str_filter != "Exibir todas":
            self.__filtered_df = self.__filtered_df.loc[self.__filtered_df[column] == self.__operation_option_str_filter]
            self.__filtered_fmtdf = self.__filtered_fmtdf.loc[self.__filtered_fmtdf[column] == self.__operation_option_str_filter]
    
    def __applyDateFilter(self) -> None:
        column = self.__columns_object._date_col.getName()
        if self.__start_date and self.__end_date:
            self.__filtered_df = self.__filtered_df.loc[(self.__start_date <= self.__filtered_df[column]) & (self.__filtered_df[column] <= self.__end_date)]
            self.__filtered_fmtdf = self.__filtered_fmtdf.loc[(self.__start_date <= self.__filtered_fmtdf[column]) & (self.__filtered_fmtdf[column] <= self.__end_date)]
            self.__filtered_date_df = self.__filtered_date_df.loc[(self.__start_date <= self.__filtered_date_df[column]) & (self.__filtered_date_df[column] <= self.__end_date)]
            self.__filtered_date_fmtdf = self.__filtered_date_fmtdf.loc[(self.__start_date <= self.__filtered_date_fmtdf[column]) & (self.__filtered_date_fmtdf[column] <= self.__end_date)]
    
    def updateDataframe(self, file):
        self.extrato.readExcelFile(file)
        self.__filtered_df = self.extrato.getNotNanDataframe()
        self.__filtered_fmtdf = self.extrato.getFormattedDataframe()
        self.__filtered_date_df = self.extrato.getNotNanDataframe()
        self.__filtered_date_fmtdf = self.extrato.getFormattedDataframe()
        self.__showSideBar()
    
    def getFilteredDataframe(self):
        return self.__filtered_df.copy()
    
    def getFilteredFormattedDataframe(self):
        return self.__filtered_fmtdf.copy()

    def getDateFilteredDataframe(self):
        return self.__filtered_date_df.copy()
    
    def getDateFilteredFormattedDataframe(self):
        return self.__filtered_date_fmtdf.copy()