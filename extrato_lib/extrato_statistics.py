import pandas as pd

from common_lib.dataframes_kit import SingleFormatter

from extrato_lib.extrato_columns import ExtratoDBColumns
from extrato_lib.extrato_dataframes_kit import ExtratoDBKit


class StatisticsCell:
    def __init__(self) -> None:
        """Structure useful to calculate basic statistics in any dataframe.
        
        The main outputs are:
        - column value sum
        - column non-NaN value count
        """
        self.__sum_a = 0
        self.__sum_b = 0
        self.__count_a = 0
        self.__count_b = 0
        self.__diff_sum = 0
        self.__diff_count = 0
    
    def __updateDiffVariables(self) -> None:
        self.__diff_sum = self.__sum_a - self.__sum_b
        self.__diff_count = self.__count_a - self.__count_b
    
    def setPositiveValues(self, df: pd.DataFrame, pos_operation: str) -> None:
        self.__sum_a = df[pos_operation].sum()
        self.__count_a = df[pos_operation].loc[df[pos_operation] != 0.0].count()
        self.__updateDiffVariables()
    
    def setNegativeValues(self, df: pd.DataFrame, neg_operation: str) -> None:
        self.__sum_b = df[neg_operation].sum() * (-1)
        self.__count_b = df[neg_operation].loc[df[neg_operation] != 0.0].count()
        self.__updateDiffVariables()
    
    def getPositiveSum(self) -> float:
        return self.__sum_a
    
    def getPositiveCount(self) -> int:
        return self.__count_a
    
    def getNegativeSum(self) -> float:
        return self.__sum_b
    
    def getNegativeCount(self) -> int:
        return self.__count_b
    
    def getDeltaSum(self) -> float:
        return self.__diff_sum

    def getDeltaCount(self) -> int:
        return self.__diff_count


class StatisticsInterface:
    def __init__(self, pos_operation: str, neg_operation: str) -> None:
        """Structure useful to format some statistics in any dataframe.
        
        Args:
        - pos_operation (str): the column to be considered as 'positive values'
        - neg_operation (str): the column to be considered as 'negative values'
        """
        self.__pos_operation = pos_operation
        self.__neg_operation = neg_operation
        self.__formatter = SingleFormatter()
        self.__statistics = StatisticsCell()
        self.__initColumnVariables()
        self.__initDataframes()

    def __initColumnVariables(self) -> None:
        columns_object = ExtratoDBColumns()
        self.__date_column = columns_object._date_col.getName()

    def __initDataframes(self) -> None:
        self.__input_dataframe = ExtratoDBKit().getNotNanDataframe()
        self.__output_dataframe = self.__getResultDataframe()

    def __getResultDataframe(self) -> pd.DataFrame:
        # Basically, return a 3 columns dataframe: 'Date', 'Price+' and 'Price-'
        target_dataframe = self.__input_dataframe.copy()
        df = target_dataframe[[self.__date_column, self.__pos_operation, self.__neg_operation]]
        df[self.__neg_operation] = df[self.__neg_operation] * (-1)
        return self.__setDateColumnAsIndex(df)

    def __setStatisticsDataframe(self, df: pd.DataFrame) -> tuple:
        self.__statistics.setPositiveValues(df, self.__pos_operation)
        self.__statistics.setNegativeValues(df, self.__neg_operation)

    def __runStatistics(self) -> None:
        self.__output_dataframe = self.__getResultDataframe()
        self.__setStatisticsDataframe(self.__output_dataframe)

    def __setDateColumnAsIndex(self, df):
        return df.rename(columns={self.__date_column:'index'}).set_index('index')

    def __getFormattedString(self, sum_value: float, count_value: int) -> str:
        str_a = self.__formatter.getMoneyString(sum_value)
        str_b = ' [' + str(count_value) + ']'
        return str_a + str_b

    def getPositiveOperationString(self) -> str:
        return self.__getFormattedString(self.__statistics.getPositiveSum(), self.__statistics.getPositiveCount())

    def getNegativeOperationString(self) -> str:
        return self.__getFormattedString(self.__statistics.getNegativeSum(),self.__statistics.getNegativeCount())
    
    def getDeltaOperationString(self) -> str:
        return self.__getFormattedString(self.__statistics.getDeltaSum(), self.__statistics.getDeltaCount())

    def getResultDataframe(self) -> pd.DataFrame:
        return self.__output_dataframe.copy()

    def setDataframe(self, dataframe) -> None:
        self.__input_dataframe = dataframe
        self.__runStatistics()
