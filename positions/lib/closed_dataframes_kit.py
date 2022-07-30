import pandas as pd

from extrato.lib.extrato_columns import ExtratoOperations
from extrato.lib.extrato_dataframes_kit import DataframesDBKitInterface, ExtratoDBKit

from positions.lib.closed_columns import ClosedPositionDBColumns


class ClosedPositionDBKit(DataframesDBKitInterface):
    def __init__(self) -> None:
        """Structure to handle a Pandas dataframe to show Closed Positions."""
        self.__columns_object = ClosedPositionDBColumns()
        super().__init__(self.__columns_object)
        
        self.__extrato_kit_object = ExtratoDBKit()
        self.__operations_object = ExtratoOperations()
        self.__addValuesToCalculatedColumns()
        self.formatDataframes()


    def __getEmptyDataLineLists(self):
        data_list = []
        column_name_list = []
        return data_list, column_name_list

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

    def __setBuyColumns(self, slice_index: int, data_list: list, column_name_list: list) -> None:
        # Quantity
        column_name_list.append(self.__columns_object._quantity_buy_col.getName())
        data_list.append(
            self.__extrato_kit_object.getSumValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._quantity_col,
                self.__operations_object.getBuyOperation(),
            )
        )
        
        # Total Price
        column_name_list.append(self.__columns_object._total_buy_price_col.getName())
        data_list.append(
            self.__extrato_kit_object.getSumValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._buy_price_col,
                self.__operations_object.getBuyOperation(),
            )
        )
        
        # IR
        column_name_list.append(self.__columns_object._IR_buy_col.getName())
        data_list.append(
            self.__extrato_kit_object.getSumValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._IR_col,
                self.__operations_object.getBuyOperation(),
            )
        )
        
        # Taxes
        column_name_list.append(self.__columns_object._taxes_buy_col.getName())
        data_list.append(
            self.__extrato_kit_object.getSumValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._taxes_col,
                self.__operations_object.getBuyOperation(),
            )
        )
    
    def __setSellColumns(self, slice_index: int, data_list: list, column_name_list: list) -> None:
        # Quantity
        column_name_list.append(self.__columns_object._quantity_sell_col.getName())
        data_list.append(
            self.__extrato_kit_object.getSumValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._quantity_col,
                self.__operations_object.getSellOperation(),
            )
        )
        
        # Total Price
        column_name_list.append(self.__columns_object._total_sell_price_col.getName())
        data_list.append(
            self.__extrato_kit_object.getSumValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._sell_price_col,
                self.__operations_object.getSellOperation(),
            )
        )
        
        # IR
        column_name_list.append(self.__columns_object._IR_sell_col.getName())
        data_list.append(
            self.__extrato_kit_object.getSumValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._IR_col,
                self.__operations_object.getSellOperation(),
            )
        )
        
        # Taxes
        column_name_list.append(self.__columns_object._taxes_sell_col.getName())
        data_list.append(
            self.__extrato_kit_object.getSumValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._taxes_col,
                self.__operations_object.getSellOperation(),
            )
        )

    def __setTotalCostsColumns(self, slice_index: int, data_list: list, column_name_list: list) -> None:
        # Total taxes
        column_name_list.append(self.__columns_object._total_taxes_col.getName())
        data_list.append(
            self.__extrato_kit_object.getSumValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._taxes_col,
            )
        )

        # Total IR
        column_name_list.append(self.__columns_object._total_IR_col.getName())
        data_list.append(
            self.__extrato_kit_object.getSumValueFromExtratoSlice(
                slice_index,
                self.__extrato_kit_object.getColumnsObject()._IR_col,
            )
        )

    def __appendNewDataLine(self, data_list: list, column_name_list: list) -> None:
        df = pd.DataFrame(columns=column_name_list)
        df = df.append(dict(zip(df.columns, data_list)), ignore_index=True)
        self._raw_df = pd.concat([self._raw_df, df])


    def __setBuyCosts(self):
        self.sumTwoColumns(
            self.__columns_object._taxes_buy_col.getName(),
            self.__columns_object._IR_buy_col.getName(),
            self.__columns_object._costs_buy_col.getName(),
        )

    def __setSellCosts(self):
        self.sumTwoColumns(
            self.__columns_object._taxes_sell_col.getName(),
            self.__columns_object._IR_sell_col.getName(),
            self.__columns_object._costs_sell_col.getName(),
        )

    def __setMeanBuyPrice(self):
        # Mean Buy
        self.divideTwoColumns(
            self.__columns_object._total_buy_price_col.getName(),
            self.__columns_object._quantity_buy_col.getName(),
            self.__columns_object._mean_buy_price_col.getName(),
        )
        
        # Buy + costs: the costs rises the 'buy price'
        self.sumTwoColumns(
            self.__columns_object._total_buy_price_col.getName(),
            self.__columns_object._costs_buy_col.getName(),
            self.__columns_object._total_costs_buy_price_col.getName(),
        )
        
        # Mean Buy + costs: the costs rises the 'mean buy price'
        self.divideTwoColumns(
            self.__columns_object._total_costs_buy_price_col.getName(),
            self.__columns_object._quantity_buy_col.getName(),
            self.__columns_object._mean_costs_buy_price_col.getName(),
        )
    
    def __setMeanSellPrice(self):
        # Mean Sell
        self.divideTwoColumns(
            self.__columns_object._total_sell_price_col.getName(),
            self.__columns_object._quantity_sell_col.getName(),
            self.__columns_object._mean_sell_price_col.getName(),
        )
        
        # Sell + costs: the costs reduces the 'sell price'
        self.subtractTwoColumns(
            self.__columns_object._total_sell_price_col.getName(),
            self.__columns_object._costs_sell_col.getName(),
            self.__columns_object._total_costs_sell_price_col.getName(),
        )
        
        # Mean Sell + costs: the costs reduces the 'mean sell price'
        self.divideTwoColumns(
            self.__columns_object._total_costs_sell_price_col.getName(),
            self.__columns_object._quantity_sell_col.getName(),
            self.__columns_object._mean_costs_sell_price_col.getName(),
        )

    def __setOtherCosts(self):
        # Total costs
        self.sumTwoColumns(
            self.__columns_object._total_taxes_col.getName(),
            self.__columns_object._total_IR_col.getName(),
            self.__columns_object._total_costs_col.getName(),
        )
        
        # Aditional taxes
        # additional_taxes = (taxes_buy + taxes_sell)
        # additional_taxes = total_taxes - additional_taxes
        self.sumTwoColumns(
            self.__columns_object._taxes_buy_col.getName(),
            self.__columns_object._taxes_sell_col.getName(),
            self.__columns_object._additional_taxes_col.getName(), # temporary variable
        )
        self.subtractTwoColumns(
            self.__columns_object._total_taxes_col.getName(),
            self.__columns_object._additional_taxes_col.getName(),
            self.__columns_object._additional_taxes_col.getName(),
        )
        
        # Aditional IR
        # additional_IR = (IR_buy + IR_sell)
        # additional_IR = total_IR - additional_IR
        self.sumTwoColumns(
            self.__columns_object._IR_buy_col.getName(),
            self.__columns_object._IR_sell_col.getName(),
            self.__columns_object._additional_IR_col.getName(), # temporary variable
        )
        self.subtractTwoColumns(
            self.__columns_object._total_IR_col.getName(),
            self.__columns_object._additional_IR_col.getName(),
            self.__columns_object._additional_IR_col.getName(),
        )


    def __addValuesToCalculatedColumns(self) -> None:
        extrato_df_slice_list = self.__extrato_kit_object.getExtratoSliceList()
        
        # Values calculated 'row-by-row'
        for slice_index in extrato_df_slice_list:
            if self.__extrato_kit_object.isClosedPositionSliceType(slice_index):
                data_list, column_name_list = self.__getEmptyDataLineLists()
                self.__setTickerClassificationColumns(slice_index, data_list, column_name_list)
                self.__setYieldColumns(slice_index, data_list, column_name_list)
                self.__setDateColumns(slice_index, data_list, column_name_list)
                self.__setBuyColumns(slice_index, data_list, column_name_list)
                self.__setSellColumns(slice_index, data_list, column_name_list)
                self.__setTotalCostsColumns(slice_index, data_list, column_name_list)
                self.__appendNewDataLine(data_list, column_name_list)        
        
        # Values calculated 'col-to-col'
        self.__setBuyCosts()
        self.__setSellCosts()
        self.__setMeanBuyPrice()
        self.__setMeanSellPrice()
        self.__setOtherCosts()
        
        self._raw_df.reset_index(drop=True, inplace=True)

    def readExcelFile(self, file) -> None:
        """Method Overridden from 'DataframesDBKitInterface' class."""
        self.__extrato_kit_object.readExcelFile(file)
        self.__addValuesToCalculatedColumns()
        self.formatDataframes()
