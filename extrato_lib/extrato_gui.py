import pandas as pd
import streamlit as st

from extrato_lib.extrato_side_bar import ExtratoSideBar
from extrato_lib.extrato_statistics import OperationTotalPriceStatistics
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
        self.__account_statistics = OperationTotalPriceStatistics("Transferência", "Resgate")

    def setDataframe(self, dataframe):
        self.__account_statistics.setDataframe(dataframe)
    
    def showInfo(self) -> None:
        st.write('#### Entradas e Saídas da conta no período [R$]')
        st.bar_chart(self.__account_statistics.getResultDataframe())
        st.write('Transferências: ', self.__account_statistics.getPositiveOperationString())
        st.write('Resgates: ', self.__account_statistics.getNegativeOperationString())
        st.write('Diferença: ', self.__account_statistics.getDeltaOperationString())
        expander = st.expander("Informações:")
        expander.write("""
            O gráfico acima mostra os valores de Entradas e Saídas da conta de investimento. \n\n
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
        self.__assets_statistics = OperationTotalPriceStatistics("Venda", "Compra")
        
    def setDataframe(self, dataframe):
        self.__assets_statistics.setDataframe(dataframe)
    
    def showInfo(self) -> None:
        st.write('#### Compras e Vendas de ativos no período [R$]')
        st.bar_chart(self.__assets_statistics.getResultDataframe())
        st.write('Vendas: ', self.__assets_statistics.getPositiveOperationString())
        st.write('Compras: ', self.__assets_statistics.getNegativeOperationString())
        st.write('Diferença: ', self.__assets_statistics.getDeltaOperationString())
        expander = st.expander("Informações:")
        expander.write("""
            O gráfico acima mostra os valores de Compras e Vendas de ativos. \n\n
            Esses valores são representados na coluna 'Operação' como 'Compra' e 'Venda'.
        """)


class ExtratoGUI:
    def __init__(self) -> None:
        """Structure used to show tables and graphs related to Extrato."""
        self.__side_bar = ExtratoSideBar()
        self.__table = ExtratoTableInfo()
        self.__account_info = ExtratoAccountInfo()
        self.__assets_info = ExtratoAssetsInfo()
        self.__setDataframes()

    def __setDataframes(self) -> None:
        self.__table.setDataframe(self.__side_bar.getFilteredFormattedDataframe())
        self.__account_info.setDataframe(self.__side_bar.getDateFilteredDataframe())
        self.__assets_info.setDataframe(self.__side_bar.getDateFilteredDataframe())

    def setDataframe(self, file) -> None:
        self.__side_bar.updateDataframe(file)
        self.__setDataframes()
        self.__table.showInfo()
        self.__account_info.showInfo()
        self.__assets_info.showInfo()
