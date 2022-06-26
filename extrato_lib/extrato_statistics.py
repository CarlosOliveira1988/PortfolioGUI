import pandas as pd

from extrato_lib.extrato_columns import ExtratoColumns
from extrato_lib.extrato_dataframe import ExtratoDataframe


class ExtratoStatistics:
    def __init__(self, pos_operation: str, neg_operation: str) -> None:
        """Structure used to calculate statistics related to Extrato."""
        self.__pos_operation = pos_operation
        self.__neg_operation = neg_operation
        self.__positive_list = [None, None]
        self.__negative_list = [None, None]
        self.__delta_list = [None, None]
        self.__extrato = ExtratoDataframe()
        self.__columns_object = ExtratoColumns()
        self.__filtered_date_df = ExtratoDataframe().getNotNanDataframe()
        self.__result_df = self.__getResultDataframe()

    def __getOperationsDataframe(self, op_string: str, negative_flag=False) -> pd.DataFrame:
        op_column = self.__columns_object._operation_col.getName()
        total_column = self.__columns_object._total_price_col.getName()
        date_column = self.__columns_object._date_col.getName()
        target_dataframe = self.__filtered_date_df.copy()
        df = target_dataframe.loc[target_dataframe[op_column] == op_string]
        if negative_flag:
            df[total_column] = df[total_column] * (-1)
        df = df[[date_column, total_column]]
        df = df.rename(columns={total_column: op_string})
        return df
    
    def __getConcatDataframes(self, df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        date_column = self.__columns_object._date_col.getName()
        df = pd.concat([df1, df2])
        df = df.rename(columns={date_column:'index'}).set_index('index')
        return df
    
    def __setStatisticsList(self, df: pd.DataFrame) -> tuple:
        col1 = self.__pos_operation
        col2 = self.__neg_operation
        list1 = [df[col1].sum(), df[col1].count()]
        list2 = [df[col2].sum() * -1, df[col2].count()]
        delta = [list1[0] - list2[0], list1[1] - list2[1]]
        self.__positive_list, self.__negative_list, self.__delta_list = list1, list2, delta
    
    def __formatStatisticsList(self) -> None:
        lists = [self.__positive_list, self.__negative_list, self.__delta_list]
        for statistic_list in lists:
            statistic_list[0] = self.__extrato._getMoneyString(statistic_list[0])
            statistic_list[1] = ' [' + str(statistic_list[1]) + ']'
    
    def __getResultDataframe(self):
        df1 = self.__getOperationsDataframe(self.__pos_operation)
        df2 = self.__getOperationsDataframe(self.__neg_operation, True)
        return self.__getConcatDataframes(df1, df2)
    
    def __runStatistics(self) -> None:
        self.__result_df = self.__getResultDataframe()
        self.__setStatisticsList(self.__result_df)
        self.__formatStatisticsList()
    
    def setDataframe(self, dataframe):
        self.__filtered_date_df = dataframe
        self.__runStatistics()
    
    def getResultDataframe(self):
        return self.__result_df
    
    def getPositiveOperationString(self):
        return self.__positive_list[0] + self.__positive_list[1]
    
    def getNegativeOperationString(self):
        return self.__negative_list[0] + self.__negative_list[1]
    
    def getDeltaOperationString(self):
        return self.__delta_list[0] + self.__delta_list[1]
