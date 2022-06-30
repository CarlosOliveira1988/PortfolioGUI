import pandas as pd
import streamlit as st

from extrato_lib.extrato_side_bar import ExtratoSideBar
from extrato_lib.extrato_statistics import OperationTotalPriceStatistics, MarketEarnsCostsStatistics
from extrato_lib.extrato_dataframe import ExtratoDataframe


class ExtratoTableInfo:
    def __init__(self) -> None:
        """Structure used to show an interactive table related to the 'Extrato'."""
        self.__filtered_fmtdf = ExtratoDataframe().getFormattedDataframe()

    def __showMainTitle(self) -> None:
        st.write('# Extrato')
        st.write('#### Histórico de transações')
    
    def __showDataframe(self) -> None:
        st.write("", self.__filtered_fmtdf.astype(str))

    def setDataframe(self, dataframe: pd.DataFrame):
        self.__filtered_fmtdf = dataframe
    
    def showInfo(self):
        self.__showMainTitle()
        self.__showDataframe()


class ExtratoAccountInfo:
    def __init__(self) -> None:
        """Structure used to show a Bar Chart and other information related to the 'Extrato Account'.
        
        This class uses the following considerations:
        - it uses the columns 'Data', 'Operação' and 'Preço Unitário' to extract useful data
        - 'Operação::Transferência' are positive values (put money in the account)
        - 'Operação::Resgate' are negative values (take money from the account)
        """
        self.__statistics = OperationTotalPriceStatistics("Transferência", "Resgate")

    def setDataframe(self, dataframe):
        self.__statistics.setDataframe(dataframe)
    
    def showInfo(self) -> None:
        st.write('#### Entradas e Saídas da conta no período [R$]')
        st.bar_chart(self.__statistics.getResultDataframe())
        st.write('Transferências: ', self.__statistics.getPositiveOperationString())
        st.write('Resgates: ', self.__statistics.getNegativeOperationString())
        st.write('Diferença: ', self.__statistics.getDeltaOperationString())
        expander = st.expander("Informações:")
        expander.write("""
            O gráfico acima mostra os valores de Entradas e Saídas da conta de investimento ao longo do período informado. \n\n
            Esses valores são representados na coluna 'Operação' como 'Transferência' e 'Resgate'.
        """)


class ExtratoAssetsInfo:
    def __init__(self) -> None:
        """Structure used to show a Bar Chart and other information related to the 'Extrato Assets'.
        
        This class uses the following considerations:
        - it uses the columns 'Data', 'Operação' and 'Preço Unitário' to extract useful data
        - 'Operação::Venda' are positive values (put money in the account)
        - 'Operação::Compra' are negative values (take money from the account)
        """
        self.__statistics = OperationTotalPriceStatistics("Venda", "Compra")
        
    def setDataframe(self, dataframe):
        self.__statistics.setDataframe(dataframe)
    
    def showInfo(self) -> None:
        st.write('#### Compras e Vendas de ativos no período [R$]')
        st.bar_chart(self.__statistics.getResultDataframe())
        st.write('Vendas: ', self.__statistics.getPositiveOperationString())
        st.write('Compras: ', self.__statistics.getNegativeOperationString())
        st.write('Diferença: ', self.__statistics.getDeltaOperationString())
        expander = st.expander("Informações:")
        expander.write("""
            O gráfico acima mostra os valores de Compras e Vendas de ativos ao longo do período informado. \n\n
            Esses valores são representados na coluna 'Operação' como 'Compra' e 'Venda'.
        """)


class ExtratoEarnsCostsInfo:
    def __init__(self) -> None:
        """Structure used to show a Bar Chart and other information related to the 'Extrato Earns & Costs'.
        
        This class uses the following considerations:
        - it uses the columns 'Data', 'Proventos Totais' and 'Custo Total' to extract useful data
        - 'Proventos Totais' are positive values (put money in the account)
        - 'Custo Total' are negative values (take money from the account)
        """
        self.__statistics = MarketEarnsCostsStatistics()
        
    def setDataframe(self, dataframe):
        self.__statistics.setDataframe(dataframe)
    
    def showInfo(self) -> None:
        st.write('#### Proventos e Custos no período [R$]')
        st.bar_chart(self.__statistics.getResultDataframe())
        st.write('Proventos: ', self.__statistics.getPositiveOperationString())
        st.write('Custos: ', self.__statistics.getNegativeOperationString())
        st.write('Diferença: ', self.__statistics.getDeltaOperationString())
        expander = st.expander("Informações:")
        expander.write("""
            O gráfico acima mostra os valores de Proventos e Custos ao longo do período informado. \n\n
            Esses valores são calculados a partir das colunas 'Dividendos', 'JCP', 'IR' e 'Taxas'.
        """)


class ExtratoGUI:
    def __init__(self) -> None:
        """Structure used to show tables and graphs related to Extrato."""
        self.__side_bar = ExtratoSideBar()
        self.__table = ExtratoTableInfo()
        self.__account_info = ExtratoAccountInfo()
        self.__assets_info = ExtratoAssetsInfo()
        self.__earns_costs_info = ExtratoEarnsCostsInfo()
        self.__setDataframes()

    def __setDataframes(self) -> None:
        self.__table.setDataframe(self.__side_bar.getFilteredFormattedDataframe())
        self.__account_info.setDataframe(self.__side_bar.getDateFilteredDataframe())
        self.__assets_info.setDataframe(self.__side_bar.getDateFilteredDataframe())
        self.__earns_costs_info.setDataframe(self.__side_bar.getDateFilteredDataframe())

    def setDataframe(self, file) -> None:
        self.__side_bar.updateDataframe(file)
        self.__setDataframes()
        self.__table.showInfo()
        self.__account_info.showInfo()
        self.__assets_info.showInfo()
        self.__earns_costs_info.showInfo()
