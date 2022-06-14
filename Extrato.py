import pandas as pd
import streamlit as st
import numpy as np
import locale


file = r"D:\Dudu\Finanças\Investimentos\Mercado Financeiro\Extrato Poupança.xlsx"


class ExtratoDataframe:
    def __init__(self):
        self.__columns_list = [
            "Mercado",
            "Ticker",
            "Operação",
            "Data",
            "Rentabilidade Contratada",
            "Indexador",
            "Vencimento",
            "Quantidade",
            "Preço Unitário",
            "Preço Total",
            "Taxas",
            "IR",
            "Dividendos",
            "JCP",
            "Custo Total",
            "Notas",
        ]
        self.__df = pd.DataFrame(columns=self.__columns_list)
    
    def __setupNAN(self, column_list, nan_value):
        for column in column_list:
            self.__df[column] = self.__df[column].replace(np.nan, nan_value)
    
    def __setupDateColumns(self):
        self.__df["Data"] = pd.to_datetime(self.__df["Data"]).dt.date
        self.__df["Vencimento"] = pd.to_datetime(self.__df["Vencimento"]).dt.date
    
    def __setupStringColumns(self):
        self.__setupNAN(["Mercado", "Ticker", "Operação", "Rentabilidade Contratada", "Indexador", "Notas"], "")
    
    def __setupNumberColumns(self):
        self.__setupNAN(["Quantidade", "Preço Unitário", "Preço Total", "Taxas", "IR", "Dividendos", "JCP", "Custo Total"], 0.0)
    
    def __defineDisplayedColumns(self):
        self.__df = self.__df[self.__columns_list]
    
    def read(self, file):
        self.__df = pd.read_excel(file)
        self.__defineDisplayedColumns()
        self.__setupStringColumns()
        self.__setupNumberColumns()
        self.__setupDateColumns()
        return self.__df


class ExtratoGUI:
    def __init__(self):
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
        self.__df = pd.DataFrame()
        self.__filtered_df = pd.DataFrame()
        self.__formatted_df = pd.DataFrame()

    def __showMainTitle(self):
        st.write('# Extrato')
        st.write('#### Histórico de transações')
    
    def __getMoneyString(self, value):
        return locale.currency(float(value), grouping=True)
    
    def __setupMoney(self, column_list):
        for column in column_list:
            self.__formatted_df[column] = self.__formatted_df.apply(lambda x: self.__getMoneyString(x[column]), axis=1)
    
    def __setupMoneyColumns(self):
        self.__setupMoney(["Preço Unitário", "Preço Total", "Taxas", "IR", "Dividendos", "JCP", "Custo Total"])
    
    def __setupPercentageColumns(self):
        self.__formatted_df.loc[:, "Rentabilidade Contratada"] = self.__formatted_df["Rentabilidade Contratada"].map(lambda x: '{:.2%}'.format(x) if (x != "") else "")
    
    def __setupQuantityColumns(self):
        self.__formatted_df.loc[:, "Quantidade"] = self.__formatted_df["Quantidade"].map(lambda x: locale.str(x))
    
    def __setupNAN(self):
        self.__formatted_df.fillna("")
        self.__formatted_df["Vencimento"].replace({pd.NaT: ""}, inplace=True)
    
    def __showDataframe(self):
        self.__setupNAN()
        self.__setupMoneyColumns()
        self.__setupPercentageColumns()
        self.__setupQuantityColumns()
        st.write("", self.__formatted_df.astype(str))

    def __showAccountBarChart(self):
        # Transfers
        df1 = self.__filtered_df.loc[self.__filtered_df['Operação'] == "Transferência"] # '+'
        df1 = df1[["Data", "Preço Total"]]
        df1 = df1.rename(columns={'Preço Total':'Transferência'})
        
        # Rescues
        df2 = self.__filtered_df.loc[self.__filtered_df['Operação'] == "Resgate"] # '-'
        df2["Preço Total"] = df2["Preço Total"] * (-1)
        df2 = df2[["Data", "Preço Total"]]
        df2 = df2.rename(columns={'Preço Total':'Resgate'})
        
        # Concatenate the dataframes
        df = pd.concat([df1, df2])
        df = df.rename(columns={'Data':'index'}).set_index('index')
        
        # Show the information
        transferencias = df['Transferência'].sum()
        resgates = df['Resgate'].sum() * -1
        saldo = transferencias - resgates
        st.write('#### Fluxo de entradas e saídas da conta')
        st.write('Transferências: ', self.__getMoneyString(transferencias))
        st.write('Resgates: ', self.__getMoneyString(resgates))
        st.write('Saldo: ', self.__getMoneyString(saldo))
        st.bar_chart(df)

    def __showAssetsBarChart(self):
        # Sell
        df1 = self.__filtered_df.loc[self.__filtered_df['Operação'] == "Venda"] # '+'
        df1 = df1[["Data", "Preço Total"]]
        df1 = df1.rename(columns={'Preço Total':'Venda'})
        
        # Buy
        df2 = self.__filtered_df.loc[self.__filtered_df['Operação'] == "Compra"] # '-'
        df2["Preço Total"] = df2["Preço Total"] * (-1)
        df2 = df2[["Data", "Preço Total"]]
        df2 = df2.rename(columns={'Preço Total':'Compra'})
        
        # Concatenate the dataframes
        df = pd.concat([df1, df2])
        df = df.rename(columns={'Data':'index'}).set_index('index')
        
        # Show the information
        vendas = df['Venda'].sum()
        compras = df['Compra'].sum() * -1
        saldo = vendas - compras
        st.write('#### Fluxo de compras e vendas de ativos')
        st.write('Compras: ', self.__getMoneyString(compras))
        st.write('Vendas: ', self.__getMoneyString(vendas))
        st.write('Saldo: ', self.__getMoneyString(saldo))
        st.bar_chart(df)

    def __showMercadoFilter(self):
        mercado_default_series = self.__filtered_df["Mercado"].drop_duplicates()
        mercado_list = st.sidebar.multiselect('Mercado:', mercado_default_series.sort_values())
        if mercado_list:
            self.__filtered_df = self.__filtered_df.loc[self.__filtered_df['Mercado'].isin(mercado_list)]

    def __showTickerFilter(self):
        ticker_default_list = ["Exibir todos"]
        ticker_default_list.extend(self.__filtered_df["Ticker"].drop_duplicates().sort_values())
        ticker_option = st.sidebar.selectbox('Ticker:', ticker_default_list)
        if ticker_option != "Exibir todos":
            self.__filtered_df = self.__filtered_df.loc[self.__filtered_df['Ticker'] == ticker_option]

    def __showOperationFilter(self):
        op_default_list = ["Exibir todas"]
        op_default_list.extend(self.__filtered_df["Operação"].drop_duplicates().sort_values())
        op_option = st.sidebar.selectbox('Operação:', op_default_list)
        if op_option != "Exibir todas":
            self.__filtered_df = self.__filtered_df.loc[self.__filtered_df['Operação'] == op_option]
    
    def __showDataFilter(self):
        start_date = self.__filtered_df["Data"].min()
        end_date = self.__filtered_df["Data"].max()
        if start_date == end_date:
            date_option = st.sidebar.slider('Período:', disabled=True)
        else:
            date_option = st.sidebar.slider('Período:', min_value=start_date, max_value=end_date, value=(start_date, end_date))
            init_date = date_option[0]
            finish_date = date_option[1]
            self.__filtered_df = self.__filtered_df.loc[(init_date <= self.__filtered_df['Data']) & (self.__filtered_df['Data'] <= finish_date)]

    def __showSideBar(self):
        self.__showMercadoFilter()
        self.__showTickerFilter()
        self.__showOperationFilter()
        self.__showDataFilter()

    def setDataframe(self, dataframe):
        self.__df = dataframe
        self.__filtered_df = self.__df.copy()
        self.__showMainTitle()
        self.__showSideBar()
        self.__formatted_df = self.__filtered_df.copy()
        self.__showDataframe()
        self.__showAccountBarChart()
        self.__showAssetsBarChart()


extrato = ExtratoDataframe()


gui = ExtratoGUI()
gui.setDataframe(extrato.read(file))
