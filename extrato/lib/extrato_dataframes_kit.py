import numpy as np
import pandas as pd

from common.dataframes_kit import DataframesKitInterface

from extrato.lib.extrato_columns import ExtratoColumnsInterface, ExtratoRawColumns, ExtratoDBColumns, ExtratoOperations


class ExtratoDataframesKitInterface(DataframesKitInterface):
    def __init__(self, columns_object: ExtratoColumnsInterface) -> None:
        """Structure to handle a group of Pandas dataframes for 'Extrato' objects.
        
        Args:
        - columns_object: any object instance inherited from 'ExtratoColumnsInterface'
        """
        self.__columns_object = columns_object
        super().__init__(self.__columns_object)


class ExtratoRawKit(ExtratoDataframesKitInterface):
    def __init__(self) -> None:
        """Structure to handle a Pandas dataframe based on Raw Extrato spreadsheet."""
        self.__columns_object = ExtratoRawColumns()
        super().__init__(self.__columns_object)


class ExtratoDBKit(ExtratoDataframesKitInterface):
    def __init__(self) -> None:
        """Structure to handle a Pandas dataframe based on Extrato Database."""
        self.__columns_object = ExtratoDBColumns()
        self.__operations_object = ExtratoOperations()
        super().__init__(self.__columns_object)
        self.__addValuesToCalculatedColumns()
        self.formatDataframes()

    def __addValuesToCalculatedColumns(self):
        self.__setTotalPriceColumn()
        self.__setTotalCostsColumn()
        self.__setTotalEarningsColumn()
        self.__setContributionsColumn()
        self.__setRescuesColumn()
        self.__setBuyPriceColumn()
        self.__setSellPriceColumn()

    def __sumTwoColumns(self, col_A: str, col_B: str, result_col: str) -> None:
        """Sum the 'col_A' and 'col_B' to put the result in the 'result_col'."""
        self._raw_df[result_col] = self._raw_df[col_A] + self._raw_df[col_B]

    def __multiplyTwoColumns(self, col_A: str, col_B: str, result_col: str) -> None:
        """Multiply the 'col_A' and 'col_B' to put the result in the 'result_col'."""
        self._raw_df[result_col] = self._raw_df[col_A] * self._raw_df[col_B]

    def __copyColumnToColumn(self, target_col: str, result_col: str) -> None:
        """Copy the 'target_col' data to the 'result_col'."""
        self._raw_df[result_col] = self._raw_df[target_col]

    def __replaceAllValuesInColumnExcept(self, target_col: str, target_val, except_col: str, except_val) -> None:
        """Put the 'target_val' in all cells of the 'target_col'.
        
        The exception case occurrs in the line when the 'except_val' is found in the 'except_col'.
        """
        self._raw_df[target_col] = self._raw_df[target_col].where(self._raw_df[except_col] == except_val, target_val)

    def __setTotalPriceColumn(self):
        # 'Total Price' = 'Quantity' * 'Unit Price'
        self.__multiplyTwoColumns(
            self.__columns_object._quantity_col.getName(), 
            self.__columns_object._unit_price_col.getName(),
            self.__columns_object._total_price_col.getName(),
        )

    def __setTotalCostsColumn(self):
        # 'Total Costs' = 'IR' + 'Taxes'
        self.__sumTwoColumns(
            self.__columns_object._IR_col.getName(), 
            self.__columns_object._taxes_col.getName(),
            self.__columns_object._total_costs_col.getName(),
        )

    def __setTotalEarningsColumn(self):
        # 'Total Earns' = 'Dividends' + 'JCP'
        self.__sumTwoColumns(
            self.__columns_object._dividends_col.getName(),
            self.__columns_object._JCP_col.getName(),
            self.__columns_object._total_earnings_col.getName(),
        )

    def __copyTotalPriceToColumn(self, operation_name: str, operation_col_name):
        # Copy the 'Total Price' data to the column 'operation_col_name', where:
        # - the 'Operation' is equal to 'operation_name'
        # - replace values in other conditions to 0 or NaN
        operation_col = self.__columns_object._operation_col.getName()
        total_price_col = self.__columns_object._total_price_col.getName()
        self.__copyColumnToColumn(total_price_col, operation_col_name)
        self.__replaceAllValuesInColumnExcept(operation_col_name, np.nan, operation_col, operation_name)

    def __setContributionsColumn(self):
        # Copy the 'Total Price' data to the column 'Contributions', where
        # the column 'Operation' is equal to 'Contribution';
        # Replace values in other conditions to 0 or NaN
        self.__copyTotalPriceToColumn(
            self.__operations_object.getContributionOperation(),
            self.__columns_object._contributions_col.getName(),
        )
    
    def __setRescuesColumn(self):
        # Copy the 'Total Price' data to the column 'Rescues', where
        # the column 'Operation' is equal to 'Rescue';
        # Replace values in other conditions to 0 or NaN
        self.__copyTotalPriceToColumn(
            self.__operations_object.getRescueOperation(),
            self.__columns_object._rescues_col.getName(),
        )

    def __setBuyPriceColumn(self):
        # Copy the 'Total Price' data to the column 'Buy Price', where
        # the column 'Operation' is equal to 'Buy';
        # Replace values in other conditions to 0 or NaN
        self.__copyTotalPriceToColumn(
            self.__operations_object.getBuyOperation(),
            self.__columns_object._buy_price_col.getName(),
        )

    def __setSellPriceColumn(self):
        # Copy the 'Total Price' data to the column 'Sell Price', where
        # the column 'Operation' is equal to 'Sell';
        # Replace values in other conditions to 0 or NaN
        self.__copyTotalPriceToColumn(
            self.__operations_object.getSellOperation(),
            self.__columns_object._sell_price_col.getName(),
        )

    def readExcelFile(self, file) -> None:
        """Method Inherited from 'ExtratoDataframesKitInterface' class."""
        self._raw_df = self.addColumnIfNotExists(pd.read_excel(file))
        self.__addValuesToCalculatedColumns()
        self.formatDataframes()
