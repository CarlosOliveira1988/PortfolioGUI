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
        self.formatDataframes(
            self.__getRawDataframe(pd.DataFrame(columns=self.__columns_object.getColumnsNameList()))
        )

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
            dataframe[column] = dataframe[column].replace(np.nan, nan_value)
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
        self._columns_object = columns_object
        self.__kit_formatter = DataframesKitFormatter(self._columns_object)
        self.__raw_df = pd.DataFrame(columns=self._columns_object.getColumnsNameList())
        self.__formatDataframes()
    
    def __formatDataframes(self):
        self.__kit_formatter.formatDataframes(self.__raw_df)
    
    def __addColumnsIfNotExists(self, dataframe):
        # There are cases that we want to create more columns than exists in the User spreadsheet
        # Then we need to create them witn NaN values
        # The 'setAsUserData' method help us to indicate the state of the data
        for column, raw_column_obj in self._columns_object.getRawColumnsDict().items():
            if column not in dataframe.columns:
                # The data column is not present in the User spreadsheet
                # Afterwards, probably it will needed to check this state when hanlding the data
                dataframe[column] = np.nan
                raw_column_obj.setAsUserData(False)
            else:
                # The application will just consume the User data
                raw_column_obj.setAsUserData(True)
        return dataframe
    
    def _calculateColumnsIfNotExists(self):
        """Abstract method to perform any calculation with non-exists dataframe columns."""
        pass
    
    def readExcelFile(self, file) -> None:
        self.__raw_df = self.__addColumnsIfNotExists(pd.read_excel(file))
        self._calculateColumnsIfNotExists()
        self.__formatDataframes()

    def getRawDataframe(self) -> pd.DataFrame:
        return self.__raw_df.copy()
    
    def getNotNanDataframe(self) -> pd.DataFrame:
        return self.__kit_formatter.getNotNanDataframe()
    
    def getFormattedDataframe(self) -> pd.DataFrame:
        return self.__kit_formatter.getFormattedDataframe()
    
    def getColumnsObject(self) -> ColumnsInterface:
        return self._columns_object
    
    def sumTwoColumns(self, col_A: str, col_B: str, result_col: str) -> None:
        self.__raw_df[result_col] = self.__raw_df[col_A] + self.__raw_df[col_B]
        self.__formatDataframes()
    
    def multiplyTwoColumns(self, col_A: str, col_B: str, result_col: str) -> None:
        self.__raw_df[result_col] = self.__raw_df[col_A] * self.__raw_df[col_B]
        self.__formatDataframes()
    
    def copyColumnToColumn(self, target_col: str, result_col: str) -> None:
        """Copy the 'target_col' data to the 'result_col'."""
        self.__raw_df[result_col] = self.__raw_df[target_col]
        self.__formatDataframes()
    
    def replaceAllValuesInColumnExcept(self, target_col: str, target_val, except_col: str, except_val) -> None:
        """Put the 'target_val' in the 'target_col' in all cells.
        
        The exception case occurrs when the 'except_val' is found in the same row of the 'except_col'.
        """
        self.__raw_df[target_col] = self.__raw_df[target_col].where(self.__raw_df[except_col] == except_val, target_val)
        self.__formatDataframes()
