import numpy as np

from common_lib.dataframes_kit import DataframesKitInterface

from extrato_lib.extrato_columns import ExtratoColumnsInterface, ExtratoRawColumns, ExtratoDBColumns, ExtratoOperations


class ExtratoDataframesKitInterface(DataframesKitInterface):
    def __init__(self, columns_object: ExtratoColumnsInterface) -> None:
        """Structure to handle a group of Pandas dataframes for 'Extrato' objects.
        
        Args:
        - columns_object: any object instance inherited from 'ExtratoColumnsInterface'
        """
        self._columns_object = columns_object
        super().__init__(self._columns_object)


class ExtratoRawKit(ExtratoDataframesKitInterface):
    def __init__(self) -> None:
        """Structure to handle a Pandas dataframe based on Raw Extrato spreadsheet."""
        self._columns_object = ExtratoRawColumns()
        super().__init__(self._columns_object)


class ExtratoDBKit(ExtratoDataframesKitInterface):
    def __init__(self) -> None:
        """Structure to handle a Pandas dataframe based on Extrato Database."""
        self._columns_object = ExtratoDBColumns()
        self._operations_object = ExtratoOperations()
        super().__init__(self._columns_object)
        self._calculateColumnsIfNotExists()

    def __setTotalPriceColumn(self):
        # If the column is not present in the User data, add values to the created column
        # 'Total Price' = 'Quantity' * 'Unit Price'
        if not self._columns_object._total_price_col.getUserDataState():
            self.multiplyTwoColumns(
                self._columns_object._quantity_col.getName(), 
                self._columns_object._unit_price_col.getName(),
                self._columns_object._total_price_col.getName(),
            )

    def __setTotalCostsColumn(self):
        # If the column is not present in the User data, add values to the created column
        # 'Total Costs' = 'IR' + 'Taxes'
        if not self._columns_object._total_costs_col.getUserDataState():
            self.sumTwoColumns(
                self._columns_object._IR_col.getName(), 
                self._columns_object._taxes_col.getName(),
                self._columns_object._total_costs_col.getName(),
            )

    def __setTotalEarningsColumn(self):
        # If the column is not present in the User data, add values to the created column
        # 'Total Earns' = 'Dividends' + 'JCP'
        if not self._columns_object._total_earnings_col.getUserDataState():
            self.sumTwoColumns(
                self._columns_object._dividends_col.getName(),
                self._columns_object._JCP_col.getName(),
                self._columns_object._total_earnings_col.getName(),
            )

    def __copyTotalPriceToNewColumn(self, operation_name: str, operation_col_name):
        # Copy the 'Total Price' data to the column 'operation_col_name', where:
        # - the 'Operation' is equal to 'operation_name'
        # - replace values in other conditions to 0 or NaN
        operation_col = self._columns_object._operation_col.getName()
        total_price_col = self._columns_object._total_price_col.getName()
        self.copyColumnToColumn(total_price_col, operation_col_name)
        self.replaceAllValuesInColumnExcept(operation_col_name, np.nan, operation_col, operation_name)

    def __setContributionsColumn(self):
        # Copy the 'Total Price' data to the column 'Contributions', where
        # the column 'Operation' is equal to 'Contribution';
        # Replace values in other conditions to 0 or NaN
        self.__copyTotalPriceToNewColumn(
            self._operations_object.getContributionOperation(),
            self._columns_object._contributions_col.getName(),
        )
    
    def __setRescuesColumn(self):
        # Copy the 'Total Price' data to the column 'Rescues', where
        # the column 'Operation' is equal to 'Rescue';
        # Replace values in other conditions to 0 or NaN
        self.__copyTotalPriceToNewColumn(
            self._operations_object.getRescueOperation(),
            self._columns_object._rescues_col.getName(),
        )
    
    def __setBuyPriceColumn(self):
        # Copy the 'Total Price' data to the column 'Buy Price', where
        # the column 'Operation' is equal to 'Buy';
        # Replace values in other conditions to 0 or NaN
        self.__copyTotalPriceToNewColumn(
            self._operations_object.getBuyOperation(),
            self._columns_object._buy_price_col.getName(),
        )
    
    def __setSellPriceColumn(self):
        # Copy the 'Total Price' data to the column 'Sell Price', where
        # the column 'Operation' is equal to 'Sell';
        # Replace values in other conditions to 0 or NaN
        self.__copyTotalPriceToNewColumn(
            self._operations_object.getSellOperation(),
            self._columns_object._sell_price_col.getName(),
        )

    def _calculateColumnsIfNotExists(self):
        """Method Inherited from 'DataframesKitInterface' class.
        
        Perform calculation with some specific columns, in case the User forgets to put those columns in his file.
        Please, check the context related to this method in its class to understand better its usage.
        """
        self.__setTotalPriceColumn()
        self.__setTotalCostsColumn()
        self.__setTotalEarningsColumn()
        self.__setContributionsColumn()
        self.__setRescuesColumn()
        self.__setBuyPriceColumn()
        self.__setSellPriceColumn()

    def getColumnsObject(self) -> ExtratoDBColumns:
        return self._columns_object
