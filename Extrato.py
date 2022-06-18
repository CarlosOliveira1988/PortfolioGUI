import pandas as pd
import streamlit as st

from extrato_lib.extrato_dataframe import ExtratoDataframe


file = r"D:\Dudu\Finanças\Investimentos\Mercado Financeiro\Extrato Poupança.xlsx"


class ExtratoSideBar:
    def __init__(self):
        """Structure to draw an Extrato Filter's Side Bar."""
        self.extrato = ExtratoDataframe()
        
        # Dataframes for common usage
        self.__filtered_df = self.extrato.getNotNanDataframe()
        self.__filtered_fmtdf = self.extrato.getFormattedDataframe()
        
        # Dataframes ONLY for Date filtering
        self.__filtered_date_df = self.extrato.getNotNanDataframe()
        self.__filtered_date_fmtdf = self.extrato.getFormattedDataframe()
    
    def __showSubHearder(self) -> None:
        st.sidebar.subheader('Filtros')
    
    def __showMarketFilter(self) -> list:
        column = self.extrato.extrato_columns._market_col.getName()
        market_default_series = self.__filtered_df[column].drop_duplicates()
        self.__market_list_filter = st.sidebar.multiselect('Mercado:', market_default_series.sort_values())
        self.__applyMarketFilter()

    def __showTickerFilter(self) -> str:
        column = self.extrato.extrato_columns._ticker_col.getName()
        ticker_default_list = ["Exibir todos"]
        ticker_default_list.extend(self.__filtered_df[column].drop_duplicates().sort_values())
        self.__ticker_option_str_filter = st.sidebar.selectbox('Ticker:', ticker_default_list)
        self.__applyTickerFilter()

    def __showOperationFilter(self) -> str:
        column = self.extrato.extrato_columns._operation_col.getName()
        op_default_list = ["Exibir todas"]
        op_default_list.extend(self.__filtered_df[column].drop_duplicates().sort_values())
        self.__operation_option_str_filter = st.sidebar.selectbox('Operação:', op_default_list)
        self.__applyOperationFilter()
    
    def __showDateFilter(self) -> tuple:
        column = self.extrato.extrato_columns._date_col.getName()
        start_date = self.__filtered_df[column].min()
        end_date = self.__filtered_df[column].max()
        if self.__filtered_df.empty:
            date_option = st.sidebar.slider('Período:', disabled=True)
            init_date = None
            finish_date = None
        elif start_date == end_date:
            date_option = st.sidebar.slider('Período:', disabled=True)
            init_date = date_option
            finish_date = date_option
        else:
            date_option = st.sidebar.slider('Período:', min_value=start_date, max_value=end_date, value=(start_date, end_date))
            init_date = date_option[0]
            finish_date = date_option[1]
        self.__start_date, self.__end_date = init_date, finish_date
        self.__applyDateFilter()
    
    def __showSideBar(self) -> None:
        self.__showSubHearder()
        self.__showMarketFilter()
        self.__showTickerFilter()
        self.__showOperationFilter()
        self.__showDateFilter()
    
    def __applyMarketFilter(self) -> None:
        column = self.extrato.extrato_columns._market_col.getName()
        if self.__market_list_filter:
            self.__filtered_df = self.__filtered_df.loc[self.__filtered_df[column].isin(self.__market_list_filter)]
            self.__filtered_fmtdf = self.__filtered_fmtdf.loc[self.__filtered_fmtdf[column].isin(self.__market_list_filter)]
    
    def __applyTickerFilter(self) -> None:
        column = self.extrato.extrato_columns._ticker_col.getName()
        if self.__ticker_option_str_filter != "Exibir todos":
            self.__filtered_df = self.__filtered_df.loc[self.__filtered_df[column] == self.__ticker_option_str_filter]
            self.__filtered_fmtdf = self.__filtered_fmtdf.loc[self.__filtered_fmtdf[column] == self.__ticker_option_str_filter]
    
    def __applyOperationFilter(self) -> None:
        column = self.extrato.extrato_columns._operation_col.getName()
        if self.__operation_option_str_filter != "Exibir todas":
            self.__filtered_df = self.__filtered_df.loc[self.__filtered_df[column] == self.__operation_option_str_filter]
            self.__filtered_fmtdf = self.__filtered_fmtdf.loc[self.__filtered_fmtdf[column] == self.__operation_option_str_filter]
    
    def __applyDateFilter(self) -> None:
        column = self.extrato.extrato_columns._date_col.getName()
        if self.__start_date and self.__end_date:
            self.__filtered_df = self.__filtered_df.loc[(self.__start_date <= self.__filtered_df[column]) & (self.__filtered_df[column] <= self.__end_date)]
            self.__filtered_fmtdf = self.__filtered_fmtdf.loc[(self.__start_date <= self.__filtered_fmtdf[column]) & (self.__filtered_fmtdf[column] <= self.__end_date)]
            self.__filtered_date_df = self.__filtered_date_df.loc[(self.__start_date <= self.__filtered_date_df[column]) & (self.__filtered_date_df[column] <= self.__end_date)]
            self.__filtered_date_fmtdf = self.__filtered_date_fmtdf.loc[(self.__start_date <= self.__filtered_date_fmtdf[column]) & (self.__filtered_date_fmtdf[column] <= self.__end_date)]
    
    def updateDataframe(self, file):
        self.extrato.readExcelFile(file)
        self.__filtered_df = self.extrato.getNotNanDataframe()
        self.__filtered_fmtdf = self.extrato.getFormattedDataframe()
        self.__filtered_date_df = self.extrato.getNotNanDataframe()
        self.__filtered_date_fmtdf = self.extrato.getFormattedDataframe()
        self.__showSideBar()
    
    def getFilteredDataframe(self):
        return self.__filtered_df.copy()
    
    def getFilteredFormattedDataframe(self):
        return self.__filtered_fmtdf.copy()

    def getDateFilteredDataframe(self):
        return self.__filtered_date_df.copy()
    
    def getDateFilteredFormattedDataframe(self):
        return self.__filtered_date_fmtdf.copy()


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


gui = ExtratoGUI()
gui.setDataframe(file)
