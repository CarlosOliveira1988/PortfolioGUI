import pandas as pd

from extrato.lib.extrato_dataframes_kit import DataframesDBKitInterface, ExtratoDBKit

from positions.lib.closed_columns import ClosedPositionDBColumns


class ClosedPositionDBKit(DataframesDBKitInterface):
    def __init__(self) -> None:
        """Structure to handle a Pandas dataframe to show Closed Positions."""
        self.__columns_object = ClosedPositionDBColumns()
        super().__init__(self.__columns_object)
        
        self.__extrato_kit_object = ExtratoDBKit()
        self.__addValuesToCalculatedColumns()
        self.formatDataframes()

    def __setTickerClassificationColumns(self, slice_index: int, data_list: list, column_name_list: list) -> None:
        # Market
        column_name_list.append(self.__columns_object._market_col.getName())
        data_list.append(
            self.__extrato_kit_object.getUniqueValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._market_col,
            )
        )
        
        # Ticker
        column_name_list.append(self.__columns_object._ticker_col.getName())
        data_list.append(
            self.__extrato_kit_object.getUniqueValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._ticker_col,
            )
        )
        
        # Indexer
        column_name_list.append(self.__columns_object._indexer_col.getName())
        data_list.append(
            self.__extrato_kit_object.getUniqueValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._indexer_col,
            )
        )

    def __setYieldColumns(self, slice_index: int, data_list: list, column_name_list: list) -> None:
        # Minimum Yield
        column_name_list.append(self.__columns_object._yield_min_col.getName())
        data_list.append(
            self.__extrato_kit_object.getMinMaxValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._hired_rate_col,
                minimum_value_flag=True,
                only_buy_operation=True,
            )
        )

        # Maximum Yield
        column_name_list.append(self.__columns_object._yield_max_col.getName())
        data_list.append(
            self.__extrato_kit_object.getMinMaxValueFromExtratoSlice(
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
            self.__extrato_kit_object.getMinMaxValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._date_col,
                minimum_value_flag=True,
                only_buy_operation=False,
            )
        )

        # Final Date
        column_name_list.append(self.__columns_object._final_date_col.getName())
        data_list.append(
            self.__extrato_kit_object.getMinMaxValueFromExtratoSlice(
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
        extrato_df_slice_list = self.__extrato_kit_object.getExtratoSliceList()
        for slice_index in extrato_df_slice_list:
            if self.__extrato_kit_object.isClosedPositionSliceType(slice_index):
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
