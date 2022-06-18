import pandas as pd
import streamlit as st

from extrato_lib.extrato_side_bar import ExtratoSideBar


class ExtratoGUI:
    def __init__(self):
        """Structure used to show tables and graphs related to Extrato."""
        self.__side_bar = ExtratoSideBar()
        self.__filtered_fmtdf = self.__side_bar.getFilteredFormattedDataframe()
        self.__filtered_date_df = self.__side_bar.getDateFilteredDataframe()

    def __showMainTitle(self):
        st.write('# Extrato')
        st.write('#### Histórico de transações')
    
    def __showDataframe(self):
        st.write("", self.__filtered_fmtdf.astype(str))

    def __getPositiveDataframe(self, op_string):
        op_column = self.__side_bar.extrato.extrato_columns._operation_col.getName()
        total_column = self.__side_bar.extrato.extrato_columns._total_price_col.getName()
        date_column = self.__side_bar.extrato.extrato_columns._date_col.getName()
        df1 = self.__filtered_date_df.loc[self.__filtered_date_df[op_column] == op_string]
        df1 = df1[[date_column, total_column]]
        df1 = df1.rename(columns={total_column: op_string})
        return df1

    def __getNegativeDataframe(self, op_string):
        op_column = self.__side_bar.extrato.extrato_columns._operation_col.getName()
        total_column = self.__side_bar.extrato.extrato_columns._total_price_col.getName()
        date_column = self.__side_bar.extrato.extrato_columns._date_col.getName()
        df2 = self.__filtered_date_df.loc[self.__filtered_date_df[op_column] == op_string]
        df2[total_column] = df2[total_column] * (-1)
        df2 = df2[[date_column, total_column]]
        df2 = df2.rename(columns={total_column: op_string})
        return df2
    
    def __getConcatDataframes(self, df1, df2):
        date_column = self.__side_bar.extrato.extrato_columns._date_col.getName()
        df = pd.concat([df1, df2])
        df = df.rename(columns={date_column:'index'}).set_index('index')
        return df

    def __getStatistics(self, df, col1, col2):
        list1 = [df[col1].sum(), df[col1].count()]
        list2 = [df[col2].sum() * -1, df[col2].count()]
        delta = [list1[0] - list2[0], list1[1] - list2[1]]
        return list1, list2, delta
    
    def __formatStatistics(self, lists):
        for statistic_list in lists:
            statistic_list[0] = self.__side_bar.extrato._getMoneyString(statistic_list[0])
            statistic_list[1] = '[' + str(statistic_list[1]) + ']'

    def __showAccountBarChart(self):
        df1 = self.__getPositiveDataframe("Transferência")
        df2 = self.__getNegativeDataframe("Resgate")
        df = self.__getConcatDataframes(df1, df2)
        transferencias, resgates, delta = self.__getStatistics(df, "Transferência", "Resgate")
        self.__formatStatistics([transferencias, resgates, delta])
        st.write('#### Entradas e Saídas da conta [R$]')
        st.bar_chart(df)
        st.write('Transferências: ', transferencias[0], transferencias[1])
        st.write('Resgates: ', resgates[0], resgates[1])
        st.write('Diferença: ', delta[0], delta[1])
        expander = st.expander("Informações:")
        expander.write("""
            O gráfico acima mostra os valores de Entradas e Saídas da conta de investimento. \n\n
            Esses valores são representados na coluna 'Operação' como 'Transferência' e 'Resgate'.
        """)

    def __showAssetsBarChart(self):
        df1 = self.__getPositiveDataframe("Venda")
        df2 = self.__getNegativeDataframe("Compra")
        df = self.__getConcatDataframes(df1, df2)
        vendas, compras, delta = self.__getStatistics(df, "Venda", "Compra")
        self.__formatStatistics([vendas, compras, delta])
        st.write('#### Compras e Vendas de ativos [R$]')
        st.bar_chart(df)
        st.write('Vendas: ', vendas[0], vendas[1])
        st.write('Compras: ', compras[0], compras[1])
        st.write('Diferença: ', delta[0], delta[1])
        expander = st.expander("Informações:")
        expander.write("""
            O gráfico acima mostra os valores de Compras e Vendas de ativos. \n\n
            Esses valores são representados na coluna 'Operação' como 'Compra' e 'Venda'.
        """)

    def setDataframe(self, file):
        self.__side_bar.updateDataframe(file)
        self.__filtered_fmtdf = self.__side_bar.getFilteredFormattedDataframe()
        self.__filtered_date_df = self.__side_bar.getDateFilteredDataframe()
        self.__showMainTitle()
        self.__showDataframe()
        self.__showAccountBarChart()
        self.__showAssetsBarChart()