from extrato.lib.extrato_columns import ExtratoOperations
from extrato.lib.extrato_dataframes_kit import DataframesDBKitInterface, ExtratoDBKit, ExtratoDBSlicer

from positions.lib.closed_columns import ClosedPositionDBColumns


class ClosedPositionDBKit(DataframesDBKitInterface):
    def __init__(self) -> None:
        """Structure to handle a Pandas dataframe to show Closed Positions."""
        self.__columns_object = ClosedPositionDBColumns()
        super().__init__(self.__columns_object)
        
        self.__extrato_kit_object = ExtratoDBKit()
        self.__extrato_slicer = ExtratoDBSlicer()
        self.__operations_object = ExtratoOperations()
        self.__addValuesToCalculatedColumns()
        self.formatDataframes()


    """Row-by-row calculation."""

    def __getEmptyDataLineLists(self):
        data_list = []
        column_name_list = []
        return data_list, column_name_list

    def __setTickerClassificationColumns(self, data_list: list, column_name_list: list) -> None:
        # Market
        column_name_list.append(self.__columns_object._market_col.getName())
        data_list.append(
            self.__extrato_slicer.getUniqueValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._market_col,
                first_line_value=True,
            )
        )
        
        # Ticker
        column_name_list.append(self.__columns_object._ticker_col.getName())
        data_list.append(
            self.__extrato_slicer.getUniqueValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._ticker_col,
                first_line_value=True,
            )
        )
        
        # Indexer
        column_name_list.append(self.__columns_object._indexer_col.getName())
        data_list.append(
            self.__extrato_slicer.getUniqueValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._indexer_col,
                first_line_value=True,
            )
        )

    def __setYieldColumns(self, data_list: list, column_name_list: list) -> None:
        # Minimum Yield
        column_name_list.append(self.__columns_object._yield_min_col.getName())
        data_list.append(
            self.__extrato_slicer.getMinMaxValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._hired_rate_col,
                minimum_value_flag=True,
                only_buy_operation=True,
            )
        )

        # Maximum Yield
        column_name_list.append(self.__columns_object._yield_max_col.getName())
        data_list.append(
            self.__extrato_slicer.getMinMaxValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._hired_rate_col,
                minimum_value_flag=False,
                only_buy_operation=True,
            )
        )

    def __setDateColumns(self, data_list: list, column_name_list: list) -> None:
        # Initial Date
        column_name_list.append(self.__columns_object._initial_date_col.getName())
        data_list.append(
            self.__extrato_slicer.getMinMaxValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._date_col,
                minimum_value_flag=True,
                only_buy_operation=False,
            )
        )

        # Final Date
        column_name_list.append(self.__columns_object._final_date_col.getName())
        data_list.append(
            self.__extrato_slicer.getMinMaxValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._date_col,
                minimum_value_flag=False,
                only_buy_operation=False,
            )
        )

    def __setBuyColumns(self, data_list: list, column_name_list: list) -> None:
        # Quantity
        column_name_list.append(self.__columns_object._quantity_buy_col.getName())
        data_list.append(
            self.__extrato_slicer.getSumValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._quantity_col,
                self.__operations_object.getBuyOperation(),
            )
        )
        
        # Total Price
        column_name_list.append(self.__columns_object._total_buy_price_col.getName())
        data_list.append(
            self.__extrato_slicer.getSumValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._buy_price_col,
                self.__operations_object.getBuyOperation(),
            )
        )
        
        # IR
        column_name_list.append(self.__columns_object._IR_buy_col.getName())
        data_list.append(
            self.__extrato_slicer.getSumValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._IR_col,
                self.__operations_object.getBuyOperation(),
            )
        )
        
        # Taxes
        column_name_list.append(self.__columns_object._taxes_buy_col.getName())
        data_list.append(
            self.__extrato_slicer.getSumValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._taxes_col,
                self.__operations_object.getBuyOperation(),
            )
        )
    
    def __setSellColumns(self, data_list: list, column_name_list: list) -> None:
        # Quantity
        column_name_list.append(self.__columns_object._quantity_sell_col.getName())
        data_list.append(
            self.__extrato_slicer.getSumValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._quantity_col,
                self.__operations_object.getSellOperation(),
            )
        )
        
        # Total Price
        column_name_list.append(self.__columns_object._total_sell_price_col.getName())
        data_list.append(
            self.__extrato_slicer.getSumValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._sell_price_col,
                self.__operations_object.getSellOperation(),
            )
        )
        
        # IR
        column_name_list.append(self.__columns_object._IR_sell_col.getName())
        data_list.append(
            self.__extrato_slicer.getSumValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._IR_col,
                self.__operations_object.getSellOperation(),
            )
        )
        
        # Taxes
        column_name_list.append(self.__columns_object._taxes_sell_col.getName())
        data_list.append(
            self.__extrato_slicer.getSumValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._taxes_col,
                self.__operations_object.getSellOperation(),
            )
        )

    def __setTotalCostsColumns(self, data_list: list, column_name_list: list) -> None:
        # Total taxes
        column_name_list.append(self.__columns_object._total_taxes_col.getName())
        data_list.append(
            self.__extrato_slicer.getSumValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._taxes_col,
            )
        )

        # Total IR
        column_name_list.append(self.__columns_object._total_IR_col.getName())
        data_list.append(
            self.__extrato_slicer.getSumValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._IR_col,
            )
        )

    def __setIncomeColumns(self, data_list: list, column_name_list: list) -> None:
        # Dividends
        column_name_list.append(self.__columns_object._dividends_col.getName())
        data_list.append(
            self.__extrato_slicer.getSumValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._dividends_col,
            )
        )

        # JCP
        column_name_list.append(self.__columns_object._JCP_col.getName())
        data_list.append(
            self.__extrato_slicer.getSumValueFromSlicedDataframe(
                self.__extrato_kit_object.getColumnsObject()._JCP_col,
            )
        )


    """Column-to-column calculation."""

    def __setBuyCostsColumns(self) -> None:
        self.sumTwoColumns(
            self.__columns_object._taxes_buy_col.getName(),
            self.__columns_object._IR_buy_col.getName(),
            self.__columns_object._costs_buy_col.getName(),
        )

    def __setSellCostsColumns(self) -> None:
        self.sumTwoColumns(
            self.__columns_object._taxes_sell_col.getName(),
            self.__columns_object._IR_sell_col.getName(),
            self.__columns_object._costs_sell_col.getName(),
        )

    def __setMeanBuyPriceColumns(self) -> None:
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
    
    def __setMeanSellPriceColumns(self) -> None:
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

    def __setOtherCostsColumns(self) -> None:
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

    def __setTotalIncomeColumns(self) -> None:
        self.sumTwoColumns(
            self.__columns_object._dividends_col.getName(),
            self.__columns_object._JCP_col.getName(),
            self.__columns_object._total_earnings_col.getName(),
        )

    def __setFinalResultsColumns(self) -> None:
        """Calculate the final result columns based in the following method:
        
            * "Venda-Compra" = "Preço Total[V]" - "Preço Total[C]"

            * "Margem Bruta" = "Venda-Compra" + "Proventos Totais"
            * "Margem Bruta (%)" = "Margem Bruta" / "Preço Total[C]"

            * "Margem Líquida" = "Margem Bruta" - "Custos Totais"
            * "Margem Líquida (%)" = "Margem Líquida" / "Preço Total[C]"
        """
        # Sell-Buy
        self.subtractTwoColumns(
            self.__columns_object._total_sell_price_col.getName(),
            self.__columns_object._total_buy_price_col.getName(),
            self.__columns_object._delta_sell_buy_col.getName(),
        )
        
        # Gross margin
        self.sumTwoColumns(
            self.__columns_object._delta_sell_buy_col.getName(),
            self.__columns_object._total_earnings_col.getName(),
            self.__columns_object._gross_margin_col.getName(),
        )

        # Gross margin (%)
        self.divideTwoColumns(
            self.__columns_object._gross_margin_col.getName(),
            self.__columns_object._total_buy_price_col.getName(),
            self.__columns_object._gross_margin_p_col.getName(),
        )

        # Net margin
        self.subtractTwoColumns(
            self.__columns_object._gross_margin_col.getName(),
            self.__columns_object._total_costs_col.getName(),
            self.__columns_object._net_margin_col.getName(),
        )

        # Net margin (%)
        self.divideTwoColumns(
            self.__columns_object._net_margin_col.getName(),
            self.__columns_object._total_buy_price_col.getName(),
            self.__columns_object._net_margin_p_col.getName(),
        )


    """Main frames for calculation."""

    def __addValuesCalculatedRowByRow(self) -> None:
        self.__extrato_slicer.setExtratoDataframe(self.__extrato_kit_object.getNotNanDataframe())
        for slice_index in self.__extrato_slicer.getExtratoSliceIndexList():
            self.__extrato_slicer.updateSlicedDataframeByIndex(slice_index)
            if self.__extrato_slicer.isClosedPositionSlicedDataframe():
                data_list, column_name_list = self.__getEmptyDataLineLists()
                self.__setTickerClassificationColumns(data_list, column_name_list)
                self.__setYieldColumns(data_list, column_name_list)
                self.__setDateColumns(data_list, column_name_list)
                self.__setBuyColumns(data_list, column_name_list)
                self.__setSellColumns(data_list, column_name_list)
                self.__setTotalCostsColumns(data_list, column_name_list)
                self.__setIncomeColumns(data_list, column_name_list)
                self.appendNewDataLine(data_list, column_name_list) 

    def __addValuesCalculatedColToCol(self) -> None:
        self.__setBuyCostsColumns()
        self.__setSellCostsColumns()
        self.__setMeanBuyPriceColumns()
        self.__setMeanSellPriceColumns()
        self.__setOtherCostsColumns()
        self.__setTotalIncomeColumns()
        self.__setFinalResultsColumns()

    def __addValuesToCalculatedColumns(self) -> None:
        self.__addValuesCalculatedRowByRow()
        self.__addValuesCalculatedColToCol()        
        self.resetDataframeIndex()


    def readExcelFile(self, file) -> None:
        """Method Overridden from 'DataframesDBKitInterface' class."""
        self.__extrato_kit_object.readExcelFile(file)
        self.__addValuesToCalculatedColumns()
        self.formatDataframes()
