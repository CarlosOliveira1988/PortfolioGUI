from common_lib.raw_column import RawColumn

class ColumnsInterface:
    def __init__(self) -> None:
        """Structure to define a group of columns to make easier handling Pandas dataframes.
        
        It is useful to help while formatting and applying NaN values in its cells.
        """
        self.__columns_name_list = []
        self.__columns_type_list = []
        self.__columns_nan_list = []
    
    def addRawColumn(self, column_name: str, column_type: str) -> RawColumn:
        raw_column = RawColumn(column_name, column_type)
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


class MustHaveColumns(ColumnsInterface):
    def __init__(self) -> None:
        """Structure to define some important columns present in most of the structures."""
        super().__init__()
        
        # Columns for Ticker classification
        self._market_col = self.addRawColumn("Mercado", "string")
        self._ticker_col = self.addRawColumn("Ticker", "string")
