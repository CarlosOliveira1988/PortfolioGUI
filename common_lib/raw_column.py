class RawColumn:
    def __init__(self, column_name: str, column_type: str) -> None:
        """Structure to define some column parameters.

        Args:
            column_name (str): the column title
            column_type (str): 'string', 'date', '$', '%', 'number'
        """
        self.__column_name = column_name
        self.__column_type = column_type
        
        # There are cases that we need to create extra columns when they do not exist
        # This flag is useful to handle this state: 'unknown', 'user data' or 'not user data'
        self.__user_data_state = None
    
    def getName(self) -> str:
        return self.__column_name

    def getType(self) -> str:
        return self.__column_type
    
    def setAsUserData(self, flag: bool) -> None:
        self.__user_data_state = flag
    
    def getUserDataState(self) -> bool:
        return self.__user_data_state
