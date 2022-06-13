import pandas as pd
import streamlit as st
import numpy as np
import locale
import altair as alt


file = r"D:\Dudu\Finanças\Investimentos\Mercado Financeiro\Extrato Poupança.xlsx"


class ExtratoDataframe:
    def __init__(self):
        self.columns_list = [
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
        self.extrato = pd.DataFrame(columns=self.columns_list)
    
    def __setupNAN(self, column_list, nan_value):
        for column in column_list:
            self.extrato[column] = self.extrato[column].replace(np.nan, nan_value)
    
    def __setupDateColumns(self):
        self.extrato["Data"] = pd.to_datetime(self.extrato["Data"], dayfirst=True, errors='coerce').dt.date
        self.extrato["Vencimento"] = pd.to_datetime(self.extrato["Vencimento"], dayfirst=True, errors='coerce').dt.date
    
    def __setupStringColumns(self):
        self.__setupNAN(["Mercado", "Ticker", "Operação", "Rentabilidade Contratada", "Indexador", "Notas"], "")
    
    def __setupNumberColumns(self):
        self.__setupNAN(["Quantidade", "Preço Unitário", "Preço Total", "Taxas", "IR", "Dividendos", "JCP", "Custo Total"], 0.0)
    
    def __defineDisplayedColumns(self):
        self.extrato = self.extrato[self.columns_list]
    
    def read(self, file):
        self.extrato = pd.read_excel(file)
        self.__defineDisplayedColumns()
        self.__setupStringColumns()
        self.__setupNumberColumns()
        self.__setupDateColumns()
        return self.extrato


class ExtratoGUI:
    def __init__(self):
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
        self.extrato = pd.DataFrame()
        self.filtered_extrato = pd.DataFrame()

    def __showMainTitle(self):
        st.write('# Extrato')
        st.write('Veja a seguir todo o histórico de transações realizadas ao longo do período.')
    
    def __setupMoney(self, column_list):
        for column in column_list:
            self.filtered_extrato[column] = self.filtered_extrato.apply(lambda x: locale.currency(float(x[column])), axis=1)
    
    def __setupMoneyColumns(self):
        self.__setupMoney(["Preço Unitário", "Preço Total", "Taxas", "IR", "Dividendos", "JCP", "Custo Total"])
    
    def __setupPercentageColumns(self):
        self.filtered_extrato.loc[:, "Rentabilidade Contratada"] = self.filtered_extrato["Rentabilidade Contratada"].map(lambda x: '{:.2%}'.format(x) if (x != "") else "")
    
    def __setupQuantityColumns(self):
        self.filtered_extrato.loc[:, "Quantidade"] = self.filtered_extrato["Quantidade"].map(lambda x: locale.str(x))
    
    def __setupNAN(self):
        self.filtered_extrato.fillna("")
        self.filtered_extrato["Vencimento"].replace({pd.NaT: ""}, inplace=True)
    
    def __showDataframe(self):
        self.__setupNAN()
        self.__setupMoneyColumns()
        self.__setupPercentageColumns()
        self.__setupQuantityColumns()
        st.write("", self.filtered_extrato.astype(str))

    def __showMercadoFilter(self):
        mercado_default_series = self.filtered_extrato["Mercado"].drop_duplicates()
        mercado_list = st.sidebar.multiselect('Mercado:', mercado_default_series.sort_values())
        if mercado_list:
            self.filtered_extrato = self.filtered_extrato.loc[self.filtered_extrato['Mercado'].isin(mercado_list)]

    def __showTickerFilter(self):
        ticker_default_list = ["Exibir todos"]
        ticker_default_list.extend(self.filtered_extrato["Ticker"].drop_duplicates().sort_values())
        ticker_option = st.sidebar.selectbox('Ticker:', ticker_default_list)
        if ticker_option != "Exibir todos":
            self.filtered_extrato = self.filtered_extrato.loc[self.filtered_extrato['Ticker'] == ticker_option]

    def __showOperationFilter(self):
        op_default_list = ["Exibir todas"]
        op_default_list.extend(self.filtered_extrato["Operação"].drop_duplicates().sort_values())
        op_option = st.sidebar.selectbox('Operação:', op_default_list)
        if op_option != "Exibir todas":
            self.filtered_extrato = self.filtered_extrato.loc[self.filtered_extrato['Operação'] == op_option]
    
    def __showDataFilter(self):
        start_date = self.filtered_extrato["Data"].min()
        end_date = self.filtered_extrato["Data"].max()
        if start_date == end_date:
            date_option = st.sidebar.slider('Período:', disabled=True)
        else:
            date_option = st.sidebar.slider('Período:', min_value=start_date, max_value=end_date, value=(start_date, end_date))
            init_date = date_option[0]
            finish_date = date_option[1]
            self.filtered_extrato = self.filtered_extrato.loc[(init_date <= self.filtered_extrato['Data']) & (self.filtered_extrato['Data'] <= finish_date)]

    def __showSideBar(self):
        self.__showMercadoFilter()
        self.__showTickerFilter()
        self.__showOperationFilter()
        self.__showDataFilter()

    def setDataframe(self, dataframe):
        self.extrato = dataframe
        self.filtered_extrato = self.extrato.copy()
        self.__showMainTitle()
        self.__showSideBar()
        self.__showDataframe()


extrato = ExtratoDataframe()


gui = ExtratoGUI()
gui.setDataframe(extrato.read(file))
