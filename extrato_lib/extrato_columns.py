from common_lib.columns_group import MustHaveColumns


class ExtratoColumns(MustHaveColumns):
    def __init__(self) -> None:
        """Structure to define all the Extrato columns.
        
        All the defined columns must be present in the Extrato Spreadsheet.
        """
        super().__init__()
        
        # Columns for Ticker classification
        self._operation_col = self.addRawColumn("Operação", "string")
        
        # Date of the spreadsheet entries
        self._date_col = self.addRawColumn("Data", "date")
        
        # Columns for Fixed Income and Treasury Bonds
        self._hired_rate_col = self.addRawColumn("Rentabilidade Contratada", "%")
        self._indexer_col = self.addRawColumn("Indexador", "string")
        self._due_date_col = self.addRawColumn("Vencimento", "date")
        
        # Columns to specify buy, sell and other special events
        self._quantity_col = self.addRawColumn("Quantidade", "number")
        self._unit_price_col = self.addRawColumn("Preço Unitário", "$")
        self._total_price_col = self.addRawColumn("Preço Total", "$")
        
        # Costs
        self._taxes_col = self.addRawColumn("Taxas", "$")
        self._IR_col = self.addRawColumn("IR", "$")
        
        # Earnings
        self._dividends_col = self.addRawColumn("Dividendos", "$")
        self._JCP_col = self.addRawColumn("JCP", "$")
        
        # Total costs
        self._total_costs_col = self.addRawColumn("Custo Total", "$")
        
        # User notes
        self._notes_col = self.addRawColumn("Notas", "string")
