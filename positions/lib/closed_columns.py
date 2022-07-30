from common.columns import ColumnsInterface


class ClosedPositionDBColumns(ColumnsInterface):
    def __init__(self) -> None:
        """Structure to define all columns related to 'Closed Position Database'.
        
        'Closed Position' means an interval of 'buy' and 'sell' operations that:
        - 'closed position' occurrs when 'buy_quantity.sum()' + 'sell_quantity.sum()' is equal to 0
        
        All values related to the 'Closed Position' are registered in the User Extrato spreadsheet.
        """
        super().__init__()

        # Columns for Ticker classification
        self._market_col = self.addRawColumn("Mercado", "string") # row-by-row
        self._ticker_col = self.addRawColumn("Ticker", "string") # row-by-row
        self._indexer_col = self.addRawColumn("Indexador", "string") # row-by-row

        # Columns for Yield comparison
        self._yield_min_col = self.addRawColumn("Yield Mínimo", "%") # row-by-row
        self._yield_max_col = self.addRawColumn("Yield Máximo", "%") # row-by-row

        # Dates
        self._initial_date_col = self.addRawColumn("Data Inicial", "date") # row-by-row
        self._final_date_col = self.addRawColumn("Data Final", "date") # row-by-row

        # Total period
        self._length_in_days_col = self.addRawColumn("Dias", "number") # col-to-col
        self._length_in_months_col = self.addRawColumn("Meses", "number") # col-to-col

        # Buy data
        self._quantity_buy_col = self.addRawColumn("Quantidade[C]", "number") # row-by-row
        self._mean_buy_price_col = self.addRawColumn("Preço Médio[C]", "$") # col-to-col
        self._total_buy_price_col = self.addRawColumn("Preço Total[C]", "$") # row-by-row
        self._taxes_buy_col = self.addRawColumn("Taxas[C]", "$") # row-by-row
        self._IR_buy_col = self.addRawColumn("IR[C]", "$") # row-by-row
        self._mean_costs_buy_price_col = self.addRawColumn("Preço Médio c/ Custos[C]", "$") # col-to-col
        self._total_costs_buy_price_col = self.addRawColumn("Preço Total c/ Custos[C]", "$") # col-to-col

        # Sell data
        self._quantity_sell_col = self.addRawColumn("Quantidade[V]", "number") # row-by-row
        self._mean_sell_price_col = self.addRawColumn("Preço Médio[V]", "$") # col-to-col
        self._total_sell_price_col = self.addRawColumn("Preço Total[V]", "$") # row-by-row
        self._taxes_sell_col = self.addRawColumn("Taxas[V]", "$") # row-by-row
        self._IR_sell_col = self.addRawColumn("IR[V]", "$") # row-by-row
        self._mean_costs_sell_price_col = self.addRawColumn("Preço Médio c/ Custos[V]", "$") # col-to-col
        self._total_costs_sell_price_col = self.addRawColumn("Preço Total c/ Custos[V]", "$") # col-to-col

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
