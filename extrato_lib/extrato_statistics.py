import pandas as pd

from extrato_lib.extrato_columns import ExtratoColumns
from extrato_lib.extrato_dataframe import ExtratoDataframe


class StatisticsCell:
    def __init__(self):
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
    
    def __updateDiffVariables(self):
        self.__diff_sum = self.__sum_a - self.__sum_b
        self.__diff_count = self.__count_a - self.__count_b
    
    def setPositiveValues(self, df: pd.DataFrame, pos_operation: str):
        self.__sum_a = df[pos_operation].sum()
        self.__count_a = df[pos_operation].count()
        self.__updateDiffVariables()
    
    def setNegativeValues(self, df: pd.DataFrame, neg_operation: str):
        self.__sum_b = df[neg_operation].sum() * (-1)
        self.__count_b = df[neg_operation].count()
        self.__updateDiffVariables()
    
    def getPositiveSum(self):
        return self.__sum_a
    
    def getPositiveCount(self):
        return self.__count_a
    
    def getNegativeSum(self):
        return self.__sum_b
    
    def getNegativeCount(self):
        return self.__count_b
    
    def getDeltaSum(self):
        return self.__diff_sum

    def getDeltaCount(self):
        return self.__diff_count


class StatisticsInterface:
    def __init__(self, pos_operation: str, neg_operation: str) -> None:
        """Structure useful to format some statistics in any dataframe."""
        self.__pos_operation = pos_operation
        self.__neg_operation = neg_operation
        self.__extrato = ExtratoDataframe()
        self.__statistics = StatisticsCell()
    
    def __getFormattedString(self, sum_value: float, count_value: int) -> str:
        str_a = self.__extrato._getMoneyString(sum_value)
        str_b = ' [' + str(count_value) + ']'
        return str_a + str_b
    
    def setStatisticsDataframe(self, df: pd.DataFrame) -> tuple:
        self.__statistics.setPositiveValues(df, self.__pos_operation)
        self.__statistics.setNegativeValues(df, self.__neg_operation)

    def getPositiveOperationString(self):
        return self.__getFormattedString(self.__statistics.getPositiveSum(), self.__statistics.getPositiveCount())
    
    def getNegativeOperationString(self):
        return self.__getFormattedString(self.__statistics.getNegativeSum(),self.__statistics.getNegativeCount())
    
    def getDeltaOperationString(self):
        return self.__getFormattedString(self.__statistics.getDeltaSum(), self.__statistics.getDeltaCount())


class OperationTotalPriceStatistics(StatisticsInterface):
    def __init__(self, pos_operation: str, neg_operation: str) -> None:
        """Structure used to prepare a dataframe to calculate statistics related to Extrato.
        
        This class uses the following columns to extract useful data:
        - 'Data'
        - 'Operação'
        - 'Preço Unitário'
        
        Args:
        - pos_operation (str): column defined as 'positive values' (Example: 'Venda')
        - neg_operation (str): column defined as 'negative values' (Example: 'Compra')
        """
        super().__init__(pos_operation, neg_operation)
        self.__initColumnVariables(pos_operation, neg_operation)
        self.__initDataframes()

    def __initColumnVariables(self, pos_operation, neg_operation):
        columns_object = ExtratoColumns()
        self.__op_column = columns_object._operation_col.getName()
        self.__total_column = columns_object._total_price_col.getName()
        self.__date_column = columns_object._date_col.getName()
        self.__pos_operation = pos_operation
        self.__neg_operation = neg_operation

    def __initDataframes(self):
        self.__input_dataframe = ExtratoDataframe().getNotNanDataframe()
        self.__output_dataframe = self.__getResultDataframe()

    def __getOperationsDataframe(self, op_string: str, negative_flag=False) -> pd.DataFrame:
        # Basically, return a 2 columns dataframe, in 2 different situations:
        # - 'Date' and 'Price+'; or
        # - 'Date' and 'Price-'
        target_dataframe = self.__input_dataframe.copy()
        df = target_dataframe.loc[target_dataframe[self.__op_column] == op_string]
        if negative_flag:
            df[self.__total_column] = df[self.__total_column] * (-1)
        df = df[[self.__date_column, self.__total_column]]
        df = df.rename(columns={self.__total_column: op_string})
        return df
    
    def __getConcatDataframes(self, df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        # Basically, return a 3 columns dataframe: 'Date', 'Price+' and 'Price-'
        df = pd.concat([df1, df2])
        df = df.rename(columns={self.__date_column:'index'}).set_index('index')
        return df
    
    def __getResultDataframe(self):
        # Basically, return a 3 columns dataframe: 'Date', 'Price+' and 'Price-'
        df1 = self.__getOperationsDataframe(self.__pos_operation)
        df2 = self.__getOperationsDataframe(self.__neg_operation, negative_flag=True)
        return self.__getConcatDataframes(df1, df2)
    
    def __runStatistics(self) -> None:
        self.__output_dataframe = self.__getResultDataframe()
        self.setStatisticsDataframe(self.__output_dataframe)
    
    def setDataframe(self, dataframe):
        self.__input_dataframe = dataframe
        self.__runStatistics()
    
    def getResultDataframe(self):
        return self.__output_dataframe.copy()
