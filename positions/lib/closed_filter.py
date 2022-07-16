import pandas as pd

from common.filter import FilterInterface

from positions.lib.closed_columns import ClosedPositionDBColumns
from positions.lib.closed_dataframes_kit import ClosedPositionDBKit

class ClosedPositionDBFilter(FilterInterface):
    def __init__(self, columns_object: ClosedPositionDBColumns, df_interface_object: ClosedPositionDBKit) -> None:
        """Structure to apply filters based on 'Closed Position' objects.
        
        Args:
        - columns_object: any object instance inherited from 'ClosedPositionDBColumns'
        - df_interface_object: any object instance inherited from 'ClosedPositionDBKit'
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
