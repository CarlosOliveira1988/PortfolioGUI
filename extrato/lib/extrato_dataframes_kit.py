import numpy as np
import pandas as pd

from common.dataframes_kit import DataframesKitInterface, DataframesDBKitInterface
from common.raw_column import RawColumn

from extrato.lib.extrato_columns import (
    ExtratoOperations, ExtratoColumnsInterface, ExtratoRawColumns, ExtratoDBColumns, InvestmentPositionType
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
        self.__postitions_type = InvestmentPositionType()
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
        self.__setSliceTypeColumn()

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

    def __setSliceTypeColumn(self) -> None:
        # Column variables    
        slice_index_col = self.__columns_object._slice_index_col.getName()
        slice_type_col = self.__columns_object._slice_type_col.getName()
        quantity_col = self.__columns_object._quantity_col.getName()
        operation_col = self.__columns_object._operation_col.getName()
        
        # Operation variables
        buy_operation = self.__operations_object.getBuyOperation()
        sell_operation = self.__operations_object.getSellOperation()
        
        # Position variables
        position_type = InvestmentPositionType()
        closed_position = position_type.getClosedPosition()
        opened_position = position_type.getOpenedPosition()
        
        # Iterate over the slices
        slice_index_list = self.getNonDuplicatedListFromColumn(slice_index_col)
        for slice_index in slice_index_list:
            
            df_filtered_by_slice_index = self._raw_df.loc[self._raw_df[slice_index_col].isin([slice_index])]
            
            df_filtered_by_buy = df_filtered_by_slice_index.loc[df_filtered_by_slice_index[operation_col].isin([buy_operation])]
            buy_ticker_quantity = df_filtered_by_buy[quantity_col].sum()
            
            df_filtered_by_sell = df_filtered_by_slice_index.loc[df_filtered_by_slice_index[operation_col].isin([sell_operation])]
            sell_ticker_quantity = df_filtered_by_sell[quantity_col].sum()
            
            if buy_ticker_quantity == sell_ticker_quantity:
                self._raw_df.loc[self._raw_df[slice_index_col] == slice_index, [slice_type_col]] = closed_position
            else:
                self._raw_df.loc[self._raw_df[slice_index_col] == slice_index, [slice_type_col]] = opened_position


    def getFilteredSliceExtrato(self, slice_index: int) -> pd.DataFrame:
        """Return a filtered dataframe per slice index: 'sliced dataframe'."""
        extrato_df = self.getNotNanDataframe()
        extrato_df_slice_index_col = self.__columns_object._slice_index_col.getName()
        return extrato_df.loc[extrato_df[extrato_df_slice_index_col].isin([slice_index])]

    def isClosedPositionSliceType(self, slice_index: int) -> bool:
        """Check if the specified 'sliced dataframe' is related to Closed Positions."""
        extrato_df_filtered_by_slice = self.getFilteredSliceExtrato(slice_index)
        extrato_df_slice_type_col = self.__columns_object._slice_type_col.getName()
        closed_position = self.__postitions_type.getClosedPosition()
        return not extrato_df_filtered_by_slice.loc[
            extrato_df_filtered_by_slice[extrato_df_slice_type_col].isin([closed_position])
        ].empty

    def getExtratoSliceList(self) -> list:
        """Return a list of all slice indexes."""
        return self.getNonDuplicatedListFromColumn(self.__columns_object._slice_index_col.getName())

    def getUniqueValueFromExtratoSlice(
        self,
        slice_index: int,
        extrato_raw_column_obj: RawColumn,
        first_line_value=True,
    ):
        """Return an unique value from the 'sliced dataframe'.
        
        This method is useful to get information such as Ticker, Market and other repeated data cells.
        
        If 'first_line_value==True': return the value from the first line
        
        If 'first_line_value==False': return the value from the last line
        """
        extrato_df_filtered = self.getFilteredSliceExtrato(slice_index)
        extrato_column_value_list = extrato_df_filtered[extrato_raw_column_obj.getName()].to_list()
        if first_line_value:
            return extrato_column_value_list[0]
        else:
            return extrato_column_value_list[-1]

    def getMinMaxValueFromExtratoSlice(
        self,
        slice_index: int,
        extrato_raw_column_obj: RawColumn,
        only_buy_operation=True,
        minimum_value_flag=True,
    ):
        """Return a minimum/maximum value from the 'sliced dataframe'.
        
        This method is useful to get data such as Prices, Yield and other number's cells.
        
        If 'minimum_value_flag==True': return the minimum value in the given column.
        If 'minimum_value_flag==False': return the maximum value in the given column.
        
        If 'only_buy_operation==True': consider only lines with the tag 'buy'
        If 'only_buy_operation==False': consider all lines of the 'sliced dataframe'
        """
        extrato_df_filtered = self.getFilteredSliceExtrato(slice_index)

        # Filter per Buy Operation
        if only_buy_operation:
            buy_operation = self.__operations_object.getBuyOperation()
            operation_col = self.__columns_object._operation_col.getName()
            extrato_df_filtered = extrato_df_filtered.loc[extrato_df_filtered[operation_col].isin([buy_operation])]

        extrato_col_data_list = extrato_df_filtered[extrato_raw_column_obj.getName()].to_list()
        if extrato_col_data_list:
            # Return Minimum/Maximum value
            if minimum_value_flag:
                return min(extrato_df_filtered[extrato_raw_column_obj.getName()].to_list())
            else:
                return max(extrato_df_filtered[extrato_raw_column_obj.getName()].to_list())
        else:
            return 0

    def getSumValueFromExtratoSlice(
        self,
        slice_index: int,
        extrato_raw_column_obj: RawColumn,
        operation_type: str,
    ):
        """Return the sum value from the 'sliced dataframe'.
        
        This method is useful to get the sum of columns such as Prices, Taxes and other related.
        
        The 'operation_type (str)' is any operation string related to the 'ExtratoOperations' class.
        """
        extrato_df_filtered = self.getFilteredSliceExtrato(slice_index)

        # Filter per Operation type
        if operation_type in self.__operations_object.getOperationsList():
            operation_col = self.__columns_object._operation_col.getName()
            extrato_df_filtered = extrato_df_filtered.loc[extrato_df_filtered[operation_col].isin([operation_type])]
        else:
            msg = "The " + str(operation_type) + " is not a valid operation type. See the ExtratoOperations class."
            raise ValueError(msg)

        return sum(extrato_df_filtered[extrato_raw_column_obj.getName()].to_list())


    def readExcelFile(self, file) -> None:
        """Method Overridden from 'ExtratoDataframesKitInterface' class."""
        self._raw_df = self.addColumnIfNotExists(pd.read_excel(file))
        self.__addValuesToCalculatedColumns()
        self.formatDataframes()


    def getColumnsObject(self) -> ExtratoDBColumns:
        return self.__columns_object
