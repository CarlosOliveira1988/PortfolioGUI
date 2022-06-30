from extrato_lib.extrato_columns import ExtratoColumns
from common_lib.dataframe_group import DataframeInterface


class ExtratoDataframe(DataframeInterface):
    def __init__(self) -> None:
        """Structure to handle a Pandas dataframe based on Extrato spreadsheet."""
        self._columns_object = ExtratoColumns()
        super().__init__(self._columns_object)
        self._calculateColumnsIfNotExists()

    def __setTotalPriceColumn(self):
        # If the column is not present in the User data, add values to the created column
        # 'Total Price' = 'Quantity' * 'Unit Price'
        if not self._columns_object._total_price_col.getUserDataState():
            self.multiplyTwoColumns(
                self._columns_object._quantity_col.getName(), 
                self._columns_object._unit_price_col.getName(),
                self._columns_object._total_price_col.getName()
            )

    def __setTotalCostsColumn(self):
        # If the column is not present in the User data, add values to the created column
        # 'Total Costs' = 'IR' + 'Taxes'
        if not self._columns_object._total_costs_col.getUserDataState():
            self.sumTwoColumns(
                self._columns_object._IR_col.getName(), 
                self._columns_object._taxes_col.getName(),
                self._columns_object._total_costs_col.getName()
            )

    def __setTotalEarningsColumn(self):
        # If the column is not present in the User data, add values to the created column
        # 'Total Earns' = 'Dividends' + 'JCP'
        if not self._columns_object._total_earnings_col.getUserDataState():
            self.sumTwoColumns(
                self._columns_object._dividends_col.getName(),
                self._columns_object._JCP_col.getName(),
                self._columns_object._total_earnings_col.getName()
            )

    def _calculateColumnsIfNotExists(self):
        """Method Inherited from 'DataframeInterface' class.
        
        Perform calculation with some specific columns, in case the User forgets to put those columns in his file.
        Please, check the context related to this method in its class to understand better its usage.
        """
        self.__setTotalPriceColumn()
        self.__setTotalCostsColumn()
        self.__setTotalEarningsColumn()

    def getColumnsObject(self) -> ExtratoColumns:
        return self._columns_object
