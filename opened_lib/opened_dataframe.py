from opened_lib.opened_columns import OpenedPositionColumns
from common_lib.dataframe_group import DataframeInterface


class OpenedPositionDataframe(DataframeInterface):
    def __init__(self):
        """Structure to handle a special Pandas dataframe related to Portfolio.
        
        Only the Opened Positions are handled with this class.
        """
        super().__init__(OpenedPositionColumns())

    def getColumnsObject(self) -> OpenedPositionColumns:
        return self._columns_object