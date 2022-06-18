from extrato_lib.raw_column import ExtratoRawColumn

class ExtratoColumns:
    def __init__(self):
        """Structure to define all the Extrato columns."""
        # Additional columns parameters
        self.__columns_name_list = []
        self.__columns_type_list = []
        self.__columns_nan_list = []

        # Raw columns
        self._market_col = self.__addRawColumn("Mercado", "string")
        self._ticker_col = self.__addRawColumn("Ticker", "string")
        self._operation_col = self.__addRawColumn("Operação", "string")
        self._date_col = self.__addRawColumn("Data", "date")
        self._hired_rate_col = self.__addRawColumn("Rentabilidade Contratada", "%")
        self._indexer_col = self.__addRawColumn("Indexador", "string")
        self._due_date_col = self.__addRawColumn("Vencimento", "date")
        self._quantity_col = self.__addRawColumn("Quantidade", "number")
        self._unit_price_col = self.__addRawColumn("Preço Unitário", "$")
        self._total_price_col = self.__addRawColumn("Preço Total", "$")
        self._taxes_col = self.__addRawColumn("Taxas", "$")
        self._IR_col = self.__addRawColumn("IR", "$")
        self._dividends_col = self.__addRawColumn("Dividendos", "$")
        self._JCP_col = self.__addRawColumn("JCP", "$")
        self._total_costs_col = self.__addRawColumn("Custo Total", "$")
        self._notes_col = self.__addRawColumn("Notas", "string")
    
    def __addRawColumn(self, column_name: str, column_type: str) -> ExtratoRawColumn:
        raw_column = ExtratoRawColumn(column_name, column_type)
        self.__columns_name_list.append(column_name)
        self.__columns_type_list.append(column_type)
        self.__columns_nan_list.append(self.getNanValueDict().get(column_name, ""))
        return raw_column
    
    def getColumnsNameList(self) -> list:
        return self.__columns_name_list.copy()
    
    def getColumnsTypeList(self) -> list:
        return self.__columns_type_list.copy()

    def getColumnsNanList(self) -> list:
        return self.__columns_nan_list.copy()
    
    def getColumnsTypeDict(self) -> dict:
        return dict(zip(self.getColumnsNameList(), self.getColumnsTypeList()))
    
    def getColumnsNanDict(self) -> dict:
        return dict(zip(self.getColumnsNameList(), self.getColumnsNanList()))
    
    def getNanValueDict(self) -> dict:
        nan_dict = {
            "string": "",
            "date": "",
            "number": 0.0,
            "$": 0.0,
            "%": 0.0,
        }
        return nan_dict
    
    def isStringType(self, column_type: str) -> bool:
        return column_type == "string"
    
    def isDateType(self, column_type: str) -> bool:
        return column_type == "date"
    
    def isNumberType(self, column_type: str) -> bool:
        return column_type == "number"

    def isCurrencyType(self, column_type: str) -> bool:
        return column_type == "$"
    
    def isPercentageType(self, column_type: str) -> bool:
        return column_type == "%"
