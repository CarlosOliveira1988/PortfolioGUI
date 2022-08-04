import locale

import pandas as pd
import numpy as np

from common.columns import ColumnsInterface


class SingleFormatter:
    def __init__(self) -> None:
        """Structure used to format values to perform 'nice visualization'."""
        self.__setFormatterLocalParameters()

    def __setFormatterLocalParameters(self) -> None:
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

    def setDataframe(self, dataframe: pd.DataFrame) -> None:
        self._raw_df = self.addColumnIfNotExists(dataframe)
        self.formatDataframes()

    def addColumnIfNotExists(self, dataframe) -> pd.DataFrame:
        # Create the column witn NaN values
        for column, raw_column_obj in self.__columns_object.getRawColumnsDict().items():
            if column not in dataframe.columns:
                dataframe[column] = np.nan
        return dataframe

    def formatDataframes(self) -> None:
        self.__kit_formatter.formatDataframes(self._raw_df)

    def getRawDataframe(self) -> pd.DataFrame:
        return self._raw_df.copy()
    
    def getNotNanDataframe(self) -> pd.DataFrame:
        return self.__kit_formatter.getNotNanDataframe()
    
    def getFormattedDataframe(self) -> pd.DataFrame:
        return self.__kit_formatter.getFormattedDataframe()

    def getColumnsObject(self) -> ColumnsInterface:
        return self.__columns_object


class DataframesDBKitInterface(DataframesKitInterface):
    def __init__(self, columns_object: ColumnsInterface) -> None:
        """Structure to handle a Pandas dataframe to perform some calculations.
        
        Args:
        - columns_object: any object instance inherited from 'ColumnsInterface'
        """
        self.__columns_object = columns_object
        super().__init__(self.__columns_object)

    def getNonDuplicatedListFromColumn(self, target_col: str, dropna=True, sorted=True) -> list:
        """Return a non-duplicated values list from a given column."""
        df_column = self._raw_df[[target_col]].copy()
        
        if dropna:
            df_column = df_column.dropna()
        
        df_column = df_column.drop_duplicates()
        df_column_list = df_column[target_col].to_list()
        
        if sorted:
            if df_column_list:
                df_column_list.sort()
        
        return df_column_list

    def subtractTwoColumns(self, col_A: str, col_B: str, result_col: str) -> None:
        """Subtract the 'col_A' and 'col_B' to put the result in the 'result_col'."""
        self._raw_df[result_col] = self._raw_df[col_A] - self._raw_df[col_B]

    def sumTwoColumns(self, col_A: str, col_B: str, result_col: str) -> None:
        """Sum the 'col_A' and 'col_B' to put the result in the 'result_col'."""
        self._raw_df[result_col] = self._raw_df[col_A] + self._raw_df[col_B]

    def multiplyTwoColumns(self, col_A: str, col_B: str, result_col: str) -> None:
        """Multiply the 'col_A' and 'col_B' to put the result in the 'result_col'."""
        self._raw_df[result_col] = self._raw_df[col_A] * self._raw_df[col_B]

    def divideTwoColumns(self, col_A: str, col_B: str, result_col: str) -> None:
        """Divide the 'col_A' per the 'col_B' and put the result in the 'result_col'."""
        self._raw_df[result_col] = self._raw_df[col_A].div(
            self._raw_df[col_B].where(self._raw_df[col_B] != 0, np.nan)
        )

    def copyColumnToColumn(self, target_col: str, result_col: str) -> None:
        """Copy the 'target_col' data to the 'result_col'."""
        self._raw_df[result_col] = self._raw_df[target_col]

    def replaceAllValuesInColumnExcept(self, target_col: str, target_val, except_col: str, except_val) -> None:
        """Put the 'target_val' in all cells of the 'target_col'.
        
        The exception case occurrs in the line when the 'except_val' is found in the 'except_col'.
        """
        self._raw_df[target_col] = self._raw_df[target_col].where(
            self._raw_df[except_col] == except_val, target_val
        )

    def appendNewDataLine(self, data_list: list, column_name_list: list) -> None:
        """Insert a new data line given the column name and data lists."""
        data_list = [[data] for data in data_list]
        df = pd.DataFrame.from_dict(dict(zip(column_name_list, data_list)))
        self._raw_df = pd.concat([self._raw_df, df])

    def resetDataframeIndex(self):
        """Reset the index of the dataframe."""
        self._raw_df.reset_index(drop=True, inplace=True)
