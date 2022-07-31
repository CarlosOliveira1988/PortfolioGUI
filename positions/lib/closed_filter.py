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

    def applyPeriodFilter(self, start_date: pd.Timestamp, end_date: pd.Timestamp) -> None:
        initial_date_column = self.__columns_object._initial_date_col.getName()
        final_date_column = self.__columns_object._final_date_col.getName()
        if start_date and end_date:
            self._filtered_df = self._filtered_df.loc[
                (start_date <= self._filtered_df[initial_date_column]) & 
                (self._filtered_df[final_date_column] <= end_date)
            ]
            self._filtered_fmtdf = self._filtered_fmtdf.loc[
                (start_date <= self._filtered_fmtdf[initial_date_column]) &
                (self._filtered_fmtdf[final_date_column] <= end_date)
            ]
