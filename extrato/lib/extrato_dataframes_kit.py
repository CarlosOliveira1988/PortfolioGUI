import numpy as np
import pandas as pd

from common.dataframes_kit import DataframesKitInterface
from common.raw_column import RawColumn

from extrato.lib.extrato_columns import (ExtratoOperations, InvestmentPositionType, ExtratoColumns)


class ExtratoSlicer:
    def __init__(self) -> None:
        """Structure to create slices based on Extrato dataframes.
        
        Slices are small filtered dataframes used to get useful information such as
        Opened and Closed Investment Position.
        """
        self.__columns_object = ExtratoColumns()
        self.__extrato_slice_index_col = self.__columns_object._slice_index_col.getName()
        self.__extrato_slice_type_col = self.__columns_object._slice_type_col.getName()

        self.__postitions_type = InvestmentPositionType()
        self.__operations_object = ExtratoOperations()

        self.extrato_df = pd.DataFrame()
        self.extrato_sliced_df = pd.DataFrame()
        self.slice_index = None

    def setExtratoDataframe(self, extrato_df: pd.DataFrame) -> None:
        self.extrato_df = extrato_df.copy()
        self.extrato_sliced_df = None

    def getExtratoSliceIndexList(self) -> list:
        """Return a list of all slice indexes."""
        df_column = self.extrato_df[[self.__extrato_slice_index_col]].copy()
        df_column = df_column.dropna()
        df_column = df_column.drop_duplicates()
        df_column_list = df_column[self.__extrato_slice_index_col].to_list()
        if df_column_list:
            df_column_list.sort()
        return df_column_list

    def updateSlicedDataframeByIndex(self, slice_index: int) -> pd.DataFrame:
        self.slice_index = slice_index
        self.extrato_sliced_df = self.getSlicedDataframe()

    def getSlicedDataframe(self) -> pd.DataFrame:
        """Return a filtered dataframe per slice index: 'sliced dataframe'."""
        return self.extrato_df.loc[self.extrato_df[self.__extrato_slice_index_col].isin([self.slice_index])]

    def isClosedPositionSlicedDataframe(self) -> bool:
        """Check if the specified 'sliced dataframe' is related to Closed Positions."""
        return not self.extrato_sliced_df.loc[
            self.extrato_sliced_df[self.__extrato_slice_type_col].isin([self.__postitions_type.getClosedPosition()])
        ].empty

    def getUniqueValueFromSlicedDataframe(
        self,
        extrato_raw_column_obj: RawColumn,
        first_line_value=True,
    ):
        """Return an unique value from the 'sliced dataframe'.
        
        This method is useful to get information such as Ticker, Market and other repeated data cells.
        
        If 'first_line_value==True': return the value from the first line
        
        If 'first_line_value==False': return the value from the last line
        """
        extrato_column_value_list = self.extrato_sliced_df[extrato_raw_column_obj.getName()].to_list()
        if first_line_value:
            return extrato_column_value_list[0]
        else:
            return extrato_column_value_list[-1]

    def getMinMaxValueFromSlicedDataframe(
        self,
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
        extrato_df_filtered = self.extrato_sliced_df.copy()

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
            return 0.0

    def getSumValueFromSlicedDataframe(
        self,
        extrato_raw_column_obj: RawColumn,
        operation_type: str = "ALL",
    ):
        """Return the sum value from the 'sliced dataframe'.
        
        This method is useful to get the sum of columns such as Prices, Taxes and other related.
        
        The 'operation_type (str)' is any operation string related to the 'ExtratoOperations' class.
        
        If ' operation_type=="ALL" ', then no subfilter is applied to the sliced dataframe.
        If ' operation_type==some_operation_type ', then a subfilter is applied to the sliced dataframe.
        """
        extrato_df_filtered = self.extrato_sliced_df.copy()

        # Filter per Operation type
        if operation_type != "ALL":
            if operation_type in self.__operations_object.getOperationsList():
                operation_col = self.__columns_object._operation_col.getName()
                extrato_df_filtered = extrato_df_filtered.loc[extrato_df_filtered[operation_col].isin([operation_type])]
            else:
                msg = "The " + str(operation_type) + " is not a valid operation type. See the ExtratoOperations class."
                raise ValueError(msg)

        return sum(extrato_df_filtered[extrato_raw_column_obj.getName()].to_list())


class ExtratoKit(DataframesKitInterface):
    def __init__(self) -> None:
        """Structure to handle a Pandas dataframe based on Extrato Database.
        
        'DBKit' means a data gotten with an extra calculation effort of the generated class.
        """
        self.__operations_object = ExtratoOperations()
        self.__columns_object = ExtratoColumns()
        super().__init__(self.__columns_object)
        self.__addValuesToCalculatedColumns()
        self.formatDataframes()

    def __addValuesToCalculatedColumns(self) -> None:
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

    def setDataframe(self, dataframe: pd.DataFrame) -> None:
        """Method Overridden from 'ExtratoDataframesKitInterface' class."""
        self._raw_df = self.addColumnIfNotExists(dataframe)
        self.__addValuesToCalculatedColumns()
        self.formatDataframes()
