from extrato_lib.extrato_columns import ExtratoColumns
from common_lib.dataframe_group import DataframeInterface


class ExtratoDataframe(DataframeInterface):
    def __init__(self) -> None:
        """Structure to handle a Pandas dataframe based on Extrato spreadsheet."""
        super().__init__(ExtratoColumns())

    def getColumnsObject(self) -> ExtratoColumns:
        return self._columns_object
