from common.columns import ColumnsInterface


class ClosedPositionDBColumns(ColumnsInterface):
    def __init__(self) -> None:
        """Structure to define all columns related to 'Closed Position Database'.
        
        'Closed Position' means an interval of 'buy' and 'sell' operations that:
        - 'buy_value.sum()' and 'buy_quantity.sum()' are considered 'negative' values
        - 'sell_value.sum()' and 'sell_quantity.sum()' are considered 'positive' values
        - 'closed position' occurrs when 'buy_quantity.sum()' + 'sell_quantity.sum()' is equal to 0
        
        All values related to the 'Closed Position' are registered in the User Extrato spreadsheet.
        """
        super().__init__()

        # Columns for Ticker classification
        self._market_col = self.addRawColumn("Mercado", "string")
        self._ticker_col = self.addRawColumn("Ticker", "string")
        self._indexer_col = self.addRawColumn("Indexador", "string")

        # Columns for Yield comparison
        self._yield_min_col = self.addRawColumn("Yield Mínimo", "%")
        self._yield_max_col = self.addRawColumn("Yield Máximo", "%")

        # Dates
        self._initial_date_col = self.addRawColumn("Data Inicial", "date")
        self._final_date_col = self.addRawColumn("Data Final", "date")

        # Total period
        self._length_in_days_col = self.addRawColumn("Dias", "number")
        self._length_in_months_col = self.addRawColumn("Meses", "number")

        # Buy data
        self._quantity_buy_col = self.addRawColumn("Quantidade Compra", "number")
        self._mean_buy_price_col = self.addRawColumn("Preço Médio Compra", "$")
        self._taxes_buy_col = self.addRawColumn("Taxas Compra", "$")
        self._IR_buy_col = self.addRawColumn("IR Compra", "$")
        self._mean_tax_buy_price_col = self.addRawColumn("Preço Médio Compra [taxas]", "$")
        self._total_buy_price_col = self.addRawColumn("Preço Total Compra", "$")

        # Sell data
        self._quantity_sell_col = self.addRawColumn("Quantidade Venda", "number")
        self._mean_sell_price_col = self.addRawColumn("Preço Médio Venda", "$")
        self._taxes_sell_col = self.addRawColumn("Taxas Venda", "$")
        self._IR_sell_col = self.addRawColumn("IR Venda", "$")
        self._mean_tax_sell_price_col = self.addRawColumn("Preço Médio Venda [taxas]", "$")
        self._total_sell_price_col = self.addRawColumn("Preço Total Venda", "$")

        # Other related taxes during the period
        self._additional_taxes_col = self.addRawColumn("Taxas Adicionais", "$") # Excluding buy and sell taxes
        self._total_taxes_col = self.addRawColumn("Taxas Totais", "$")

        # Other related IR during the period
        self._additional_IR_col = self.addRawColumn("IR Adicional", "$") # Excluding buy and sell IR
        self._total_IR_col = self.addRawColumn("IR Total", "$")

        # Total costs
        self._total_costs_col = self.addRawColumn("Custos Totais", "$") # Total taxes + Total IR

        # Earnings during the period
        self._dividends_col = self.addRawColumn("Dividendos", "$")
        self._JCP_col = self.addRawColumn("JCP", "$")
        self._total_earnings_col = self.addRawColumn("Proventos Totais", "$") # Including all dividends and JCP

        # Final results
        self._gross_margin_col = self.addRawColumn("Resultado Bruto", "$")
        self._gross_margin_p_col = self.addRawColumn("Resultado Bruto (%)", "%")
        self._net_margin_col = self.addRawColumn("Resultado Líquido", "$")
        self._net_margin_p_col = self.addRawColumn("Resultado Líquido (%)", "%")
        self._benchmark_IPCA_col = self.addRawColumn("IPCA+ (a.a.)", "%") # comparison to IPCA treasury in the period
        self._benchmark_CDI_col = self.addRawColumn("*CDI (a.a.)", "%") # comparison to CDI in the period
