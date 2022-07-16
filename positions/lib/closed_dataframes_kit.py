import pandas as pd

from extrato.lib.extrato_dataframes_kit import ExtratoDBKitInterface, ExtratoDBKit

from positions.lib.closed_columns import ClosedPositionDBColumns


class ClosedPositionDBKit(ExtratoDBKitInterface):
    def __init__(self) -> None:
        """Structure to handle a Pandas dataframe to show Closed Positions."""
        self.__extrato_kit_object = ExtratoDBKit()
        self.__columns_object = ClosedPositionDBColumns()
        super().__init__(self.__columns_object)
        self.__addValuesToCalculatedColumns()
        self.formatDataframes()

    def __addValuesToCalculatedColumns(self) -> None:
        pass

    def readExcelFile(self, file) -> None:
        """Method Inherited from 'ExtratoDBKitInterface' class."""
        self._raw_df = self.addColumnIfNotExists(pd.read_excel(file))
        self.__addValuesToCalculatedColumns()
        self.formatDataframes()
