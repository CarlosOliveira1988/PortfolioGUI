from common_lib.columns import ColumnsInterface


class ExtratoOperations:
    def __init__(self) -> None:
        """Structure to define possible values for the column 'Operação'."""
        self.__main_operations_list = []
        self.__buy = self.__addMainOperation("Compra")
        self.__sell = self.__addMainOperation("Venda")
        self.__rescue = self.__addMainOperation("Resgate")
        self.__contribution = self.__addMainOperation("Transferência")
        
        self.__sec_operations_list = []
        self.__income = self.__addSecondaryOperation("Provento")
        self.__charge = self.__addSecondaryOperation("Cobrança")
    
    def __addMainOperation(self, operation_string: str) -> str:
        self.__main_operations_list.append(operation_string)
        return operation_string
    
    def __addSecondaryOperation(self, operation_string: str) -> str:
        self.__sec_operations_list.append(operation_string)
        return operation_string

    def getMainOperationsList(self):
        return self.__main_operations_list.copy()

    def getSecondaryOperationsList(self):
        return self.__sec_operations_list.copy()
    
    def getBuyOperation(self):
        return self.__buy
    
    def getSellOperation(self):
        return self.__sell
    
    def getRescueOperation(self):
        return self.__rescue

    def getContributionOperation(self):
        return self.__contribution
    
    def getIncomeOperation(self):
        return self.__income
    
    def getChargeOperation(self):
        return self.__charge


class ExtratoColumnsInterface(ColumnsInterface):
    def __init__(self) -> None:
        """Structure to define an interface of 'Extrato' columns."""
        super().__init__()
        
        # Date of the spreadsheet entries
        self._date_col = self.addRawColumn("Data", "date")
        
        # Columns for Ticker classification
        self._market_col = self.addRawColumn("Mercado", "string")
        self._ticker_col = self.addRawColumn("Ticker", "string")
        self._operation_col = self.addRawColumn("Operação", "string")
        
        # Columns for Fixed Income and Treasury Bonds
        self._hired_rate_col = self.addRawColumn("Rentabilidade Contratada", "%")
        self._indexer_col = self.addRawColumn("Indexador", "string")
        self._due_date_col = self.addRawColumn("Vencimento", "date")
        
        # Columns to specify buy, sell and other special events
        self._quantity_col = self.addRawColumn("Quantidade", "number")
        self._unit_price_col = self.addRawColumn("Preço Unitário", "$")
        
        # Costs
        self._taxes_col = self.addRawColumn("Taxas", "$")
        self._IR_col = self.addRawColumn("IR", "$")
        
        # Earnings
        self._dividends_col = self.addRawColumn("Dividendos", "$")
        self._JCP_col = self.addRawColumn("JCP", "$")
        
        # User notes
        self._notes_col = self.addRawColumn("Notas", "string")


class ExtratoRawColumns(ExtratoColumnsInterface):
    def __init__(self) -> None:
        """Structure to define all the 'RAW' Extrato columns.
        
        All the defined columns must be present in the Extrato Spreadsheet.
        """
        super().__init__()


class ExtratoDBColumns(ExtratoColumnsInterface):
    def __init__(self) -> None:
        """Structure to define all columns related to the 'Extrato Database'.
        
        This class was created in order to make easier some calculations, such as:
        - sum of the 'dividends', 'costs'
        - count the 'Buy' and 'Sell' operations
        - etc.
        
        Basically, our target is splitting the 'Extrato' columns in several new ones.
        """
        super().__init__()

        # "Custo Total": It could be not present in the User spreadsheet, but it is
        # Anyway, the app may calculate it easily
        self._total_price_col = self.addRawColumn("Preço Total", "$")
        
        # "Custo Total": It could be not present in the User spreadsheet, but it is
        # Anyway, the app may calculate it easily
        self._total_costs_col = self.addRawColumn("Custo Total", "$")
        
        # "Proventos Totais": It is NOT present in the User spreadsheet, but the app may calculate it easily
        self._total_earnings_col = self.addRawColumn("Proventos Totais", "$")

        # The below columns can be extracted from the column 'Operação' and 'Preço Total'
        self._contributions_col = self.addRawColumn("Transferência", "$")
        self._rescues_col = self.addRawColumn("Resgate", "$")
        self._buy_price_col = self.addRawColumn("Compra", "$")
        self._sell_price_col = self.addRawColumn("Venda", "$")
