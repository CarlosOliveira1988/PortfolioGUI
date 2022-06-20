import locale

import pandas as pd
import numpy as np

from common_lib.columns_group import ColumnsInterface


class DataframeInterface:
    def __init__(self, columns_object: ColumnsInterface):
        """Structure to handle different types of dataframes.
        
        The main output of this class are:
        - raw dataframe
        - formatted dataframe
        - nan dataframe
        
        Args:
        - columns_object: an instance based on 'ColumnsInterface' class
        """
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
        self._columns_object = columns_object
        self.__raw_df = self.__getRawDataframe(pd.DataFrame(columns=self._columns_object.getColumnsNameList()))
        self.__not_nan_df = self.__getNotNanDataframe(self.__raw_df)
        self.__formatted_df = self.__getFormattedDataframe(self.__not_nan_df)
    
    def __getRawDataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        return self.__defineDisplayedColumns(dataframe)
    
    def __getNotNanDataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = self.__defineDisplayedColumns(dataframe)
        dataframe = self.__setupDateColumns(dataframe)
        dataframe = self.__setupNanColumns(dataframe)
        return dataframe
    
    def _getMoneyString(self, value: str) -> str:
        try:
            return locale.currency(float(value), grouping=True)
        except ValueError:
            if value == "":
                return locale.currency(0.0, grouping=True)
    
    def _getPercentageString(self, value: str) -> str:
        return '{:.2%}'.format(value) if (value != "") else ""
    
    def _getNumberString(self, value: str) -> str:
        return locale.str(value)
    
    def __getFormattedDataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        df = dataframe.copy()
        if not df.empty:
            for column, type_value in self._columns_object.getColumnsTypeDict().items():
                if self._columns_object.isCurrencyType(type_value):
                    df[column] = df[column].apply(self._getMoneyString)
                elif self._columns_object.isPercentageType(type_value):
                    df[column] = df[column].apply(self._getPercentageString)
                elif self._columns_object.isNumberType(type_value):
                    df[column] = df[column].apply(self._getNumberString)
        return df
    
    def __defineDisplayedColumns(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        return dataframe[self._columns_object.getColumnsNameList()].copy()
    
    def __setupDateColumns(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        for column, type_value in self._columns_object.getColumnsTypeDict().items():
            if self._columns_object.isDateType(type_value):
                dataframe[column] = pd.to_datetime(dataframe[column]).dt.date
        return dataframe
    
    def __setupNanColumns(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        for column, nan_value in self._columns_object.getColumnsNanDict().items():
            dataframe[column] = dataframe[column].replace(np.nan, nan_value)
        return dataframe
    
    def readExcelFile(self, file) -> None:
        self.__raw_df = self.__getRawDataframe(pd.read_excel(file))
        self.__not_nan_df = self.__getNotNanDataframe(self.__raw_df)
        self.__formatted_df = self.__getFormattedDataframe(self.__not_nan_df)

    def getRawDataframe(self) -> pd.DataFrame:
        return self.__raw_df.copy()
    
    def getNotNanDataframe(self) -> pd.DataFrame:
        return self.__not_nan_df.copy()
    
    def getFormattedDataframe(self) -> pd.DataFrame:
        return self.__formatted_df.copy()
    
    def getColumnsObject(self) -> ColumnsInterface:
        return self._columns_object
