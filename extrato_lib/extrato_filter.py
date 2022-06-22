import pandas as pd

from extrato_lib.extrato_columns import ExtratoColumns
from extrato_lib.extrato_dataframe import ExtratoDataframe


class ExtratoFilter:
    def __init__(self):
        """Structure to apply filters based on Extrato objects."""
        self.__extrato = ExtratoDataframe()
        self.__columns_object = ExtratoColumns()
        self.__updateDataframes()
    
    def __updateDataframes(self):
        self.__filtered_df = self.__extrato.getNotNanDataframe()
        self.__filtered_fmtdf = self.__extrato.getFormattedDataframe()
    
    def applyMarketFilter(self, market_list: list) -> None:
        column = self.__columns_object._market_col.getName()
        if market_list:
            self.__filtered_df = self.__filtered_df.loc[self.__filtered_df[column].isin(market_list)]
            self.__filtered_fmtdf = self.__filtered_fmtdf.loc[self.__filtered_fmtdf[column].isin(market_list)]
    
    def applyTickerFilter(self, ticker: str) -> None:
        column = self.__columns_object._ticker_col.getName()
        if ticker != "Exibir todos":
            self.__filtered_df = self.__filtered_df.loc[self.__filtered_df[column] == ticker]
            self.__filtered_fmtdf = self.__filtered_fmtdf.loc[self.__filtered_fmtdf[column] == ticker]
    
    def applyOperationFilter(self, operation: str) -> None:
        column = self.__columns_object._operation_col.getName()
        if operation != "Exibir todas":
            self.__filtered_df = self.__filtered_df.loc[self.__filtered_df[column] == operation]
            self.__filtered_fmtdf = self.__filtered_fmtdf.loc[self.__filtered_fmtdf[column] == operation]
    
    def applyDateFilter(self, start_date: pd.Timestamp, end_date: pd.Timestamp) -> None:
        column = self.__columns_object._date_col.getName()
        if start_date and end_date:
            self.__filtered_df = self.__filtered_df.loc[(start_date <= self.__filtered_df[column]) & (self.__filtered_df[column] <= end_date)]
            self.__filtered_fmtdf = self.__filtered_fmtdf.loc[(start_date <= self.__filtered_fmtdf[column]) & (self.__filtered_fmtdf[column] <= end_date)]

    def updateDataframe(self, file) -> None:
        self.__extrato.readExcelFile(file)
        self.__updateDataframes()

    def getDataframe(self) -> pd.DataFrame:
        return self.__filtered_df.copy()
    
    def getFormattedDataframe(self) -> pd.DataFrame:
        return self.__filtered_fmtdf.copy()
