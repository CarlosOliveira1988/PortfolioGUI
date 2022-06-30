from common_lib.columns_group import ColumnsInterface


class OpenedPositionColumns(ColumnsInterface):
    def __init__(self) -> None:
        """Structure to define all the Opened Position columns.
        
        Those columns are created while finding the Opened Positions from the Extrato.
        """
        super().__init__()
        
        # Data for Ticker classification
        self._indexer_col = self.addRawColumn("Indexador", "string")
        
        # Yield columns for Fixed Income, Treasury Bonds and Stocks (dividend-yield)
        self._yield_col = self.addRawColumn("Yield", "%")
        self._adj_yield_col = self.addRawColumn("Yield Ajustado", "%")
        
        # Dates
        self._initial_date_col = self.addRawColumn("Data Inicial", "date")
        self._today_date_col = self.addRawColumn("Data Hoje", "date")
        
        # Buy data
        self._quantity_buy_col = self.addRawColumn("Quantidade Compra", "number")
        self._taxes_buy_col = self.addRawColumn("Taxas Compra", "$")
        self._IR_buy_col = self.addRawColumn("IR Compra", "$")
        self._mean_buy_price_col = self.addRawColumn("Preço Médio Compra", "$")
        self._mean_tax_buy_price_col = self.addRawColumn("Preço Médio Compra [taxas]", "$")
        self._total_buy_price_col = self.addRawColumn("Preço Total Compra", "$")
        
        # Sell data
        self._quantity_sell_col = self.addRawColumn("Quantidade Venda", "number")
        self._taxes_sell_col = self.addRawColumn("Taxas Venda", "$")
        self._IR_sell_col = self.addRawColumn("IR Venda", "$")
        self._mean_sell_price_col = self.addRawColumn("Preço Médio Venda", "$")
        self._mean_tax_sell_price_col = self.addRawColumn("Preço Médio Venda [taxas]", "$")
        self._total_sell_price_col = self.addRawColumn("Preço Total Venda", "$")
        
        # Current values
        self._quantity_col = self.addRawColumn("Quantidade Atual", "number") # "Quantidade Compra" - "Quantidade Venda"
        self._invested_price_col = self.addRawColumn("Valor Investido", "$") # "Preço Médio Compra" * "Quantidade Atual"
        self._quotation_col = self.addRawColumn("Cotação Atual", "$") # Web scrapping
        self._market_price_col = self.addRawColumn("Valor Atual", "$") # "Cotação Atual" * "Quantidade Atual"
        
        # Taxes
        self._add_taxes_col = self.addRawColumn("Taxas Adicionais", "$") # Excluding buy and sell taxes
        self._taxes_col = self.addRawColumn("Taxas Totais", "$")
        
        # IR
        self._add_IR_col = self.addRawColumn("IR Adicional", "$") # Excluding buy and sell IR
        self._IR_col = self.addRawColumn("IR Total", "$")
        
        # Total costs
        self._costs_col = self.addRawColumn("Custos Totais", "$") # "Taxas Totais" + "IR Total"
        
        # Earnings
        self._dividends_col = self.addRawColumn("Dividendos", "$")
        self._JCP_col = self.addRawColumn("JCP", "$")
        self._earnings_col = self.addRawColumn("Proventos Totais", "$") # "Dividendos" + "JCP"

        # Results
        self._delta_value_col = self.addRawColumn("Atual-Investido", "$") # "Valor Atual" - "Valor Investido"
        self._delta_value_p_col = self.addRawColumn("Atual-Investido [%]", "%") # ("Valor Atual" / "Valor Investido") - 1
        self._net_value_col = self.addRawColumn("Líquido Parcial", "$") # "Atual-Investido" + "Proventos Totais" - "Custos Totais"
        self._net_value_p_col = self.addRawColumn("Líquido Parcial [%]", "%") # "Líquido Parcial" / "Valor Investido"
