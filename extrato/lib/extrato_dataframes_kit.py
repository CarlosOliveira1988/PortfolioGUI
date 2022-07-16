import numpy as np
import pandas as pd

from common.dataframes_kit import DataframesKitInterface, DataframesDBKitInterface

from extrato.lib.extrato_columns import (
    ExtratoOperations, ExtratoColumnsInterface, ExtratoRawColumns, ExtratoDBColumns
)


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


class ExtratoDBKit(DataframesDBKitInterface):
    def __init__(self) -> None:
        """Structure to handle a Pandas dataframe based on Extrato Database."""
        self.__columns_object = ExtratoDBColumns()
        super().__init__(self.__columns_object)
        self.__addValuesToCalculatedColumns()
        self.formatDataframes()

    def __addValuesToCalculatedColumns(self) -> None:
        self.__operations_object = ExtratoOperations()
        self.__setTotalPriceColumn()
        self.__setTotalCostsColumn()
        self.__setTotalEarningsColumn()
        self.__setContributionsColumn()
        self.__setRescuesColumn()
        self.__setBuyPriceColumn()
        self.__setSellPriceColumn()
        self.__setSliceIndexColumn()

    def __setTotalPriceColumn(self) -> None:
        # 'Total Price' = 'Quantity' * 'Unit Price'
        self.multiplyTwoColumns(
            self.__columns_object._quantity_col.getName(), 
            self.__columns_object._unit_price_col.getName(),
            self.__columns_object._total_price_col.getName(),
        )

    def __setTotalCostsColumn(self) -> None:
        # 'Total Costs' = 'IR' + 'Taxes'
        self.sumTwoColumns(
            self.__columns_object._IR_col.getName(), 
            self.__columns_object._taxes_col.getName(),
            self.__columns_object._total_costs_col.getName(),
        )

    def __setTotalEarningsColumn(self) -> None:
        # 'Total Earns' = 'Dividends' + 'JCP'
        self.sumTwoColumns(
            self.__columns_object._dividends_col.getName(),
            self.__columns_object._JCP_col.getName(),
            self.__columns_object._total_earnings_col.getName(),
        )

    def __copyTotalPriceToColumn(self, operation_name: str, operation_col_name: str) -> None:
        # Copy the 'Total Price' data to the column 'operation_col_name', where:
        # - the 'Operation' is equal to 'operation_name'
        # - replace values in other conditions to 0 or NaN
        operation_col = self.__columns_object._operation_col.getName()
        total_price_col = self.__columns_object._total_price_col.getName()
        self.copyColumnToColumn(total_price_col, operation_col_name)
        self.replaceAllValuesInColumnExcept(operation_col_name, np.nan, operation_col, operation_name)

    def __setContributionsColumn(self) -> None:
        # Copy the 'Total Price' data to the column 'Contributions', where
        # the column 'Operation' is equal to 'Contribution';
        # Replace values in other conditions to 0 or NaN
        self.__copyTotalPriceToColumn(
            self.__operations_object.getContributionOperation(),
            self.__columns_object._contributions_col.getName(),
        )
    
    def __setRescuesColumn(self) -> None:
        # Copy the 'Total Price' data to the column 'Rescues', where
        # the column 'Operation' is equal to 'Rescue';
        # Replace values in other conditions to 0 or NaN
        self.__copyTotalPriceToColumn(
            self.__operations_object.getRescueOperation(),
            self.__columns_object._rescues_col.getName(),
        )

    def __setBuyPriceColumn(self) -> None:
        # Copy the 'Total Price' data to the column 'Buy Price', where
        # the column 'Operation' is equal to 'Buy';
        # Replace values in other conditions to 0 or NaN
        self.__copyTotalPriceToColumn(
            self.__operations_object.getBuyOperation(),
            self.__columns_object._buy_price_col.getName(),
        )

    def __setSellPriceColumn(self) -> None:
        # Copy the 'Total Price' data to the column 'Sell Price', where
        # the column 'Operation' is equal to 'Sell';
        # Replace values in other conditions to 0 or NaN
        self.__copyTotalPriceToColumn(
            self.__operations_object.getSellOperation(),
            self.__columns_object._sell_price_col.getName(),
        )

    def __setSliceIndexColumn(self) -> None:
        # Run row-per-row in order to find 'slices'.
        # Slices are group of lines to create an 'Opened Position' or 'Closed Position'
        # 'Closed Positions' are identified by groups of lines that 'quantitiy_buy==quantity_sell'
        # 'Opened Positions' are the rest of them
        
        # Column variables       
        ticker_col = self.__columns_object._ticker_col.getName()
        date_col = self.__columns_object._date_col.getName()
        quantity_col = self.__columns_object._quantity_col.getName()
        operation_col = self.__columns_object._operation_col.getName()
        slice_index_col = self.__columns_object._slice_index_col.getName()
        
        # Operation variables
        buy_operation = self.__operations_object.getBuyOperation()
        sell_operation = self.__operations_object.getSellOperation()
        
        # Non-duplicated ticker list
        unique_ticker_list = self.getNonDuplicatedListFromColumn(ticker_col)
        if unique_ticker_list:
            unique_ticker_list.sort()
        
        # Prepare the dataframe
        df = self._raw_df.copy()
        df = df.fillna(0)
        df = df.sort_values(by=date_col)
        
        # Iterate over the dataframe to identify the 'slices'
        slice_index = 0
        
        for ticker in unique_ticker_list:
            
            df_filter_by_ticker = df.loc[df[ticker_col].isin([ticker])]
            
            # Iterate over each line of the filtered dataframe
            buy_ticker_quantity = 0.0
            sell_ticker_quantity = 0.0
            checked_rows = 0
            df_filter_by_ticker_max_rows = len(df_filter_by_ticker[date_col].to_list())
            for index, df_line in df_filter_by_ticker.iterrows():
                
                # Buy and sell operations
                if df_line[operation_col] == buy_operation:
                    buy_ticker_quantity += df_line[quantity_col]
                elif df_line[operation_col] == sell_operation:
                    sell_ticker_quantity += df_line[quantity_col]
                
                # Set the slice index
                df.at[index, slice_index_col] = slice_index
                self._raw_df.at[index, slice_index_col] = slice_index
                
                # 'Closing Operation' or 'End of the filtered frame'
                checked_rows += 1
                if (buy_ticker_quantity == sell_ticker_quantity) or (checked_rows == df_filter_by_ticker_max_rows):
                    slice_index += 1

    def readExcelFile(self, file) -> None:
        """Method Inherited from 'ExtratoDataframesKitInterface' class."""
        self._raw_df = self.addColumnIfNotExists(pd.read_excel(file))
        self.__addValuesToCalculatedColumns()
        self.formatDataframes()
