import pandas as pd

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
        """Structure useful to format some statistics in any dataframe."""
        self.__pos_operation = pos_operation
        self.__neg_operation = neg_operation
        self.__extrato = ExtratoDBKit()
        self.__statistics = StatisticsCell()

    def __getFormattedString(self, sum_value: float, count_value: int) -> str:
        str_a = self.__extrato._getMoneyString(sum_value)
        str_b = ' [' + str(count_value) + ']'
        return str_a + str_b

    def __runStatistics(self) -> None:
        self._output_dataframe = self._getResultDataframe()
        self.setStatisticsDataframe(self._output_dataframe)

    def _initDataframes(self) -> None:
        self._input_dataframe = ExtratoDBKit().getNotNanDataframe()
        self._output_dataframe = self._getResultDataframe()
    
    def _getConcatDataframes(self, df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        # Basically, return a 3 columns dataframe: 'Date', 'Price+' and 'Price-'
        df = pd.concat([df1, df2])
        return self._setDateColumnAsIndex(df)
    
    def _setDateColumnAsIndex(self, df):
        columns_object = ExtratoDBColumns()
        self.__date_column = columns_object._date_col.getName()
        return df.rename(columns={self.__date_column:'index'}).set_index('index')
    
    def _getResultDataframe(self) -> pd.DataFrame:
        return self._input_dataframe.copy()

    def setStatisticsDataframe(self, df: pd.DataFrame) -> tuple:
        self.__statistics.setPositiveValues(df, self.__pos_operation)
        self.__statistics.setNegativeValues(df, self.__neg_operation)

    def getPositiveOperationString(self) -> str:
        return self.__getFormattedString(self.__statistics.getPositiveSum(), self.__statistics.getPositiveCount())
    
    def getNegativeOperationString(self) -> str:
        return self.__getFormattedString(self.__statistics.getNegativeSum(),self.__statistics.getNegativeCount())
    
    def getDeltaOperationString(self) -> str:
        return self.__getFormattedString(self.__statistics.getDeltaSum(), self.__statistics.getDeltaCount())

    def setDataframe(self, dataframe) -> None:
        self._input_dataframe = dataframe
        self.__runStatistics()

    def getResultDataframe(self) -> pd.DataFrame:
        return self._output_dataframe.copy()


class OperationTotalPriceStatistics(StatisticsInterface):
    def __init__(self, pos_operation: str, neg_operation: str) -> None:
        """Structure used to prepare a dataframe to calculate statistics related to Extrato.
        
        This class uses the following columns to extract useful data:
        - 'Data'
        - 'Operação'
        - 'Preço Total'
        
        Args:
        - pos_operation (str): column defined as 'positive values' (Example: 'Venda')
        - neg_operation (str): column defined as 'negative values' (Example: 'Compra')
        """
        super().__init__(pos_operation, neg_operation)
        self._initColumnVariables(pos_operation, neg_operation)
        self._initDataframes()

    def _initColumnVariables(self, pos_operation: str, neg_operation: str) -> None:
        columns_object = ExtratoDBColumns()
        self.__date_column = columns_object._date_col.getName()
        self.__op_column = columns_object._operation_col.getName()
        self.__total_column = columns_object._total_price_col.getName()
        self.__pos_operation = pos_operation
        self.__neg_operation = neg_operation

    def __getOperationsDataframe(self, op_string: str, negative_flag=False) -> pd.DataFrame:
        # Basically, return a 2 columns dataframe, in 2 different situations:
        # - 'Date' and 'Price+'; or
        # - 'Date' and 'Price-'
        target_dataframe = self._input_dataframe.copy()
        df = target_dataframe.loc[target_dataframe[self.__op_column] == op_string]
        if negative_flag:
            df[self.__total_column] = df[self.__total_column] * (-1)
        df = df[[self.__date_column, self.__total_column]]
        df = df.rename(columns={self.__total_column: op_string})
        return df
    
    def _getResultDataframe(self) -> pd.DataFrame:
        # Basically, return a 3 columns dataframe: 'Date', 'Price+' and 'Price-'
        df1 = self.__getOperationsDataframe(self.__pos_operation)
        df2 = self.__getOperationsDataframe(self.__neg_operation, negative_flag=True)
        return self._getConcatDataframes(df1, df2)


class EarnsCostsStatistics(StatisticsInterface):
    def __init__(self) -> None:
        """Structure used to calculate statistics related to Extrato.
        
        This class uses the following columns to extract useful data:
        - 'Data'
        - 'Proventos Totais' (positive values)
        - 'Custo Total' (negative values)
        """
        self._initColumnVariables()
        super().__init__(self.__pos_operation, self.__neg_operation)
        self._initDataframes()
    
    def _initColumnVariables(self):
        columns_object = ExtratoDBColumns()
        self.__date_column = columns_object._date_col.getName()
        self.__total_earnings_column = columns_object._total_earnings_col .getName()
        self.__total_costs_column = columns_object._total_costs_col.getName()
        self.__pos_operation = self.__total_earnings_column
        self.__neg_operation = self.__total_costs_column

    def _getResultDataframe(self) -> pd.DataFrame:
        # Basically, return a 3 columns dataframe: 'Date', 'Price+' and 'Price-'
        target_dataframe = self._input_dataframe.copy()
        df = target_dataframe[[self.__date_column, self.__total_earnings_column, self.__total_costs_column]]
        df[self.__total_costs_column] = df[self.__total_costs_column] * (-1)
        return self._setDateColumnAsIndex(df)
