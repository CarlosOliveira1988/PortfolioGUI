import pandas as pd

from common.filter import FilterInterface

from positions.lib.closed_columns import ClosedPositionColumns
from positions.lib.closed_dataframes_kit import ClosedPositionKit


class ClosedPositionFilter(FilterInterface):
    def __init__(self) -> None:
        """Structure to apply filters based on 'Closed Position' objects."""
        self.__columns_object = ClosedPositionColumns()
        self.__df_interface_object = ClosedPositionKit()
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
