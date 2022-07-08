class RawColumn:
    def __init__(self, column_name: str, column_type: str) -> None:
        """Structure to define some column parameters.

        Args:
            column_name (str): the column title
            column_type (str): 'string', 'date', '$', '%', 'number'
        """
        self.__column_name = column_name
        self.__column_type = column_type

    def getName(self) -> str:
        return self.__column_name

    def getType(self) -> str:
        return self.__column_type
