import pandas as pd

from common.filter import FilterInterface

from positions.lib.closed_columns import ClosedPositionRawColumns, ClosedPositionDBColumns
from positions.lib.closed_dataframes_kit import ClosedPositionRawKit, ClosedPositionDBKit


class ClosedPositionFilterInterface(FilterInterface):
    def __init__(self, columns_object, df_interface_object) -> None:
        """Structure to apply filters based on 'Closed Position' objects."""
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

class ClosedPositionRawFilter(ClosedPositionFilterInterface):
    def __init__(self) -> None:
        """Structure to apply filters based on 'Closed Position' objects."""
        self.__columns_object = ClosedPositionRawColumns()
        self.__df_interface_object = ClosedPositionRawKit()
        super().__init__(self.__columns_object, self.__df_interface_object)


class ClosedPositionDBFilter(ClosedPositionFilterInterface):
    def __init__(self) -> None:
        """Structure to apply filters based on 'Closed Position' objects."""
        self.__columns_object = ClosedPositionDBColumns()
        self.__df_interface_object = ClosedPositionDBKit()
        super().__init__(self.__columns_object, self.__df_interface_object)
