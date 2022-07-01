import pandas as pd

from extrato_lib.extrato_columns import ExtratoColumns
from extrato_lib.extrato_dataframes_kit import ExtratoDataframe
from common_lib.filter import FilterInterface


class ExtratoFilter(FilterInterface):
    def __init__(self) -> None:
        """Structure to apply filters based on Extrato objects."""
        self.__columns_object = ExtratoColumns()
        super().__init__(ExtratoDataframe(), self.__columns_object)
    
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
