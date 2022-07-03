import pandas as pd

from common_lib.filter import FilterInterface

from extrato_lib.extrato_columns import ExtratoColumnsInterface, ExtratoRawColumns, ExtratoDBColumns
from extrato_lib.extrato_dataframes_kit import ExtratoDataframesKitInterface, ExtratoRawKit, ExtratoDBKit


class ExtratoFilterInterface(FilterInterface):
    def __init__(self, columns_object: ExtratoColumnsInterface, df_interface_object: ExtratoDataframesKitInterface) -> None:
        """Structure to apply filters based on Extrato objects.
        
        Args:
        - columns_object: any object instance inherited from 'ColumnsInterface'
        - df_interface_object: any object instance inherited from 'DataframesKitInterface'
        """
        self.__columns_object = columns_object
        self.__df_interface_object = df_interface_object
        super().__init__(self.__df_interface_object, self.__columns_object)
    
    def applyOperationFilter(self, operation: str) -> None:
        column = self.__columns_object._operation_col.getName()
        if operation != "Exibir todas":
            self._filtered_df = self._filtered_df.loc[self._filtered_df[column] == operation]
            self._filtered_fmtdf = self._filtered_fmtdf.loc[self._filtered_fmtdf[column] == operation]
    
    def applyDateFilter(self, start_date: pd.Timestamp, end_date: pd.Timestamp) -> None:
        column = self.__columns_object._date_col.getName()
        if start_date and end_date:
            self._filtered_df = self._filtered_df.loc[(start_date <= self._filtered_df[column]) & (self._filtered_df[column] <= end_date)]
            self._filtered_fmtdf = self._filtered_fmtdf.loc[(start_date <= self._filtered_fmtdf[column]) & (self._filtered_fmtdf[column] <= end_date)]


class ExtratoRawFilter(ExtratoFilterInterface):
    def __init__(self) -> None:
        """Structure to apply filters based on 'RAW' Extrato objects."""
        super().__init__(ExtratoRawColumns(), ExtratoRawKit())


class ExtratoDBFilter(ExtratoFilterInterface):
    def __init__(self) -> None:
        """Structure to apply filters based on 'Database' Extrato objects."""
        super().__init__(ExtratoDBColumns(), ExtratoDBKit())
