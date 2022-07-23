import pandas as pd

from common.raw_column import RawColumn

from extrato.lib.extrato_dataframes_kit import DataframesDBKitInterface, ExtratoDBKit
from extrato.lib.extrato_columns import ExtratoOperations, InvestmentPositionType

from positions.lib.closed_columns import ClosedPositionDBColumns


class ClosedPositionDBKit(DataframesDBKitInterface):
    def __init__(self) -> None:
        """Structure to handle a Pandas dataframe to show Closed Positions."""
        self.__columns_object = ClosedPositionDBColumns()
        super().__init__(self.__columns_object)
        
        self.__operations_object = ExtratoOperations()
        self.__postitions_type = InvestmentPositionType()
        self.__extrato_kit_object = ExtratoDBKit()
        self.__addValuesToCalculatedColumns()
        self.formatDataframes()

    def __getFilteredSliceExtrato(self, slice_index: int) -> pd.DataFrame:
        extrato_df = self.__extrato_kit_object.getNotNanDataframe()
        
        extrato_df_columns_object = self.__extrato_kit_object.getColumnsObject()
        extrato_df_slice_index_col = extrato_df_columns_object._slice_index_col.getName()
        
        return extrato_df.loc[extrato_df[extrato_df_slice_index_col].isin([slice_index])]

    def __isClosedPositionSliceType(self, slice_index: int) -> bool:
        extrato_df_filtered_by_slice = self.__getFilteredSliceExtrato(slice_index)
        
        extrato_df_columns_object = self.__extrato_kit_object.getColumnsObject()
        extrato_df_slice_type_col = extrato_df_columns_object._slice_type_col.getName()
        
        closed_position = self.__postitions_type.getClosedPosition()
        
        return not extrato_df_filtered_by_slice.loc[
            extrato_df_filtered_by_slice[extrato_df_slice_type_col].isin([closed_position])
        ].empty

    def __getExtratoSliceList(self) -> list:
        return self.__extrato_kit_object.getNonDuplicatedListFromColumn(
            self.__extrato_kit_object.getColumnsObject()._slice_index_col.getName()
        )

    def __getUniqueValueFromExtratoSlice(
        self,
        slice_index: int,
        extrato_raw_column_obj: RawColumn,
        first_line_value=True,
    ):
        # If 'first_line_value==True': return the value from the first line
        # If 'first_line_value==False': return the value from the last line
        extrato_df_filtered = self.__getFilteredSliceExtrato(slice_index)
        extrato_column_value_list = extrato_df_filtered[extrato_raw_column_obj.getName()].to_list()
        if first_line_value:
            return extrato_column_value_list[0]
        else:
            return extrato_column_value_list[-1]

    def __getMinMaxValueFromExtratoSlice(
        self,
        slice_index: int,
        extrato_raw_column_obj: RawColumn,
        only_buy_operation=True,
        minimum_value_flag=True,
    ):
        extrato_df_filtered = self.__getFilteredSliceExtrato(slice_index)

        # Filter per Buy Operation
        if only_buy_operation:
            buy_operation = self.__operations_object.getBuyOperation()
            operation_col = self.__extrato_kit_object.getColumnsObject()._operation_col.getName()
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

    def __setTickerClassificationColumns(self, slice_index: int, data_list: list, column_name_list: list) -> None:
        # Market
        column_name_list.append(self.__columns_object._market_col.getName())
        data_list.append(
            self.__getUniqueValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._market_col,
            )
        )
        
        # Ticker
        column_name_list.append(self.__columns_object._ticker_col.getName())
        data_list.append(
            self.__getUniqueValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._ticker_col,
            )
        )
        
        # Indexer
        column_name_list.append(self.__columns_object._indexer_col.getName())
        data_list.append(
            self.__getUniqueValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._indexer_col,
            )
        )

    def __setYieldColumns(self, slice_index: int, data_list: list, column_name_list: list) -> None:
        # Minimum Yield
        column_name_list.append(self.__columns_object._yield_min_col.getName())
        data_list.append(
            self.__getMinMaxValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._hired_rate_col,
                minimum_value_flag=True,
                only_buy_operation=True,
            )
        )

        # Maximum Yield
        column_name_list.append(self.__columns_object._yield_max_col.getName())
        data_list.append(
            self.__getMinMaxValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._hired_rate_col,
                minimum_value_flag=False,
                only_buy_operation=True,
            )
        )

    def __setDateColumns(self, slice_index: int, data_list: list, column_name_list: list) -> None:
        # Initial Date
        column_name_list.append(self.__columns_object._initial_date_col.getName())
        data_list.append(
            self.__getMinMaxValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._date_col,
                minimum_value_flag=True,
                only_buy_operation=False,
            )
        )

        # Final Date
        column_name_list.append(self.__columns_object._final_date_col.getName())
        data_list.append(
            self.__getMinMaxValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._date_col,
                minimum_value_flag=False,
                only_buy_operation=False,
            )
        )

    def __appendNewDataLine(self, data_list: list, column_name_list: list) -> None:
        df = pd.DataFrame(columns=column_name_list)
        df = df.append(dict(zip(df.columns, data_list)), ignore_index=True)
        self._raw_df = pd.concat([self._raw_df, df])

    def __addValuesToCalculatedColumns(self) -> None:
        extrato_df_slice_list = self.__getExtratoSliceList()
        for slice_index in extrato_df_slice_list:
            if self.__isClosedPositionSliceType(slice_index):
                data_list = []
                column_name_list = []
                self.__setTickerClassificationColumns(slice_index, data_list, column_name_list)
                self.__setYieldColumns(slice_index, data_list, column_name_list)
                self.__setDateColumns(slice_index, data_list, column_name_list)
                self.__appendNewDataLine(data_list, column_name_list)
        self._raw_df.reset_index(drop=True, inplace=True)

    def readExcelFile(self, file) -> None:
        """Method Overridden from 'DataframesDBKitInterface' class."""
        self.__extrato_kit_object.readExcelFile(file)
        self.__addValuesToCalculatedColumns()
        self.formatDataframes()
