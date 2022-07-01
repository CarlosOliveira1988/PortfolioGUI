import pandas as pd

from common_lib.columns import ColumnsInterface
from common_lib.dataframes_kit import DataframeInterface


class FilterInterface:
    def __init__(self, df_interface_object: DataframeInterface, columns_object: ColumnsInterface) -> None:
        """Structure to apply filters to different types of DataframeInterface objects.
                
        The main output of this class are:
        - filtered dataframe
        - filtered formatted dataframe
        
        Args:
        - df_interface_object: an instance based on 'DataframeInterface' class
        - columns_object: an instance based on 'ColumnsInterface' class
        """
        self.__df_interface_object = df_interface_object
        self.__columns_object = columns_object
        self._updateMainDataframes()
    
    def _updateMainDataframes(self) -> None:
        self._filtered_df = self.__df_interface_object.getNotNanDataframe()
        self._filtered_fmtdf = self.__df_interface_object.getFormattedDataframe()
    
    def applyMarketFilter(self, market_list: list) -> None:
        column = self.__columns_object._market_col.getName()
        if market_list:
            self._filtered_df = self._filtered_df.loc[self._filtered_df[column].isin(market_list)]
            self._filtered_fmtdf = self._filtered_fmtdf.loc[self._filtered_fmtdf[column].isin(market_list)]
    
    def applyTickerFilter(self, ticker: str) -> None:
        column = self.__columns_object._ticker_col.getName()
        if ticker != "Exibir todos":
            self._filtered_df = self._filtered_df.loc[self._filtered_df[column] == ticker]
            self._filtered_fmtdf = self._filtered_fmtdf.loc[self._filtered_fmtdf[column] == ticker]

    def updateDataframe(self, file) -> None:
        self.__df_interface_object.readExcelFile(file)
        self._updateMainDataframes()

    def getDataframe(self) -> pd.DataFrame:
        return self._filtered_df.copy()
    
    def getFormattedDataframe(self) -> pd.DataFrame:
        return self._filtered_fmtdf.copy()
