import locale

import pandas as pd
import numpy as np

from common_lib.columns import ColumnsInterface


class SingleFormatter:
    def __init__(self) -> None:
        """Structure used to format values to perform 'nice visualization'."""
        self.__setFormatterLocalParameters()

    def __setFormatterLocalParameters(self):
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

    def getMoneyString(self, value: str) -> str:
        try:
            return locale.currency(float(value), grouping=True)
        except ValueError:
            if value == "":
                return locale.currency(0.0, grouping=True)
    
    def getPercentageString(self, value: str) -> str:
        return '{:.2%}'.format(value) if (value != "") else ""
    
    def getNumberString(self, value: str) -> str:
        return locale.str(value)


class DataframesKitFormatter:
    def __init__(self, columns_object: ColumnsInterface) -> None:
        """Structure used to format dataframes for 'nice visualization'.
        
        The main format values are related to:
        - currency
        - percentage
        - numbers
        
        Besides that, this class defines the 'columns order' when displaying dataframes.
        """
        self.__columns_object = columns_object
        self.__formatter = SingleFormatter()
        self.formatDataframes(self.__getRawDataframe(pd.DataFrame(columns=self.__columns_object.getColumnsNameList())))

    def __getRawDataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        return self.__defineDisplayedColumns(dataframe)

    def __defineDisplayedColumns(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        # There are cases the User spreadsheet has a lot more columns than expected
        # We want to display only the target columns in the defined order
        return dataframe[self.__columns_object.getColumnsNameList()].copy()

    def __setupDateColumns(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        for column, type_value in self.__columns_object.getColumnsTypeDict().items():
            if self.__columns_object.isDateType(type_value):
                dataframe[column] = pd.to_datetime(dataframe[column]).dt.date
        return dataframe
    
    def __setupNanColumns(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        for column, nan_value in self.__columns_object.getColumnsNanDict().items():
            dataframe[column] = dataframe[column].fillna(nan_value)
        return dataframe

    def __getNotNanDataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = self.__defineDisplayedColumns(dataframe)
        dataframe = self.__setupDateColumns(dataframe)
        dataframe = self.__setupNanColumns(dataframe)
        return dataframe

    def __getFormattedDataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        df = dataframe.copy()
        if not df.empty:
            for column, type_value in self.__columns_object.getColumnsTypeDict().items():
                if self.__columns_object.isCurrencyType(type_value):
                    df[column] = df[column].apply(self.__formatter.getMoneyString)
                elif self.__columns_object.isPercentageType(type_value):
                    df[column] = df[column].apply(self.__formatter.getPercentageString)
                elif self.__columns_object.isNumberType(type_value):
                    df[column] = df[column].apply(self.__formatter.getNumberString)
        return df

    def formatDataframes(self, raw_dataframe) -> None:
        self.__not_nan_df = self.__getNotNanDataframe(raw_dataframe)
        self.__formatted_df = self.__getFormattedDataframe(self.__not_nan_df)

    def getNotNanDataframe(self) -> pd.DataFrame:
        return self.__not_nan_df.copy()
    
    def getFormattedDataframe(self) -> pd.DataFrame:
        return self.__formatted_df.copy()


class DataframesKitInterface:
    def __init__(self, columns_object: ColumnsInterface) -> None:
        """Structure to handle different types of dataframes.
        
        The main outputs of this class are:
        - raw dataframe
        - formatted dataframe
        - nan dataframe
        
        Args:
        - columns_object: any instance based on 'ColumnsInterface' class
        """
        self.__columns_object = columns_object
        self.__kit_formatter = DataframesKitFormatter(self.__columns_object)
        self._raw_df = pd.DataFrame(columns=self.__columns_object.getColumnsNameList())
        self.formatDataframes()

    def addColumnIfNotExists(self, dataframe):
        # Create the column witn NaN values
        for column, raw_column_obj in self.__columns_object.getRawColumnsDict().items():
            if column not in dataframe.columns:
                dataframe[column] = np.nan
        return dataframe

    def formatDataframes(self):
        self.__kit_formatter.formatDataframes(self._raw_df)

    def readExcelFile(self, file) -> None:
        self._raw_df = self.addColumnIfNotExists(pd.read_excel(file))
        self.formatDataframes()

    def getRawDataframe(self) -> pd.DataFrame:
        return self._raw_df.copy()
    
    def getNotNanDataframe(self) -> pd.DataFrame:
        return self.__kit_formatter.getNotNanDataframe()
    
    def getFormattedDataframe(self) -> pd.DataFrame:
        return self.__kit_formatter.getFormattedDataframe()
