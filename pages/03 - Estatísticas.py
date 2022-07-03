import streamlit as st

from extrato_lib.extrato_side_bar import ExtratoDBSideBar
from extrato_lib.extrato_statistics import OperationTotalPriceStatistics, EarnsCostsStatistics


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
        self.__statistics = EarnsCostsStatistics()
        
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


class ExtratoStatisticsGUI:
    def __init__(self) -> None:
        """Structure used to show data, graphs and filters related to Extrato."""
        self.__side_bar = ExtratoDBSideBar(operation_filter=False)
        self.__assets_info = ExtratoAssetsInfo()
        self.__earns_costs_info = ExtratoEarnsCostsInfo()
        self.__setDataframes()

    def __setDataframes(self) -> None:
        self.__assets_info.setDataframe(self.__side_bar.getFilteredDataframe())
        self.__earns_costs_info.setDataframe(self.__side_bar.getFilteredDataframe())

    def setDataframe(self, file) -> None:
        self.__side_bar.updateDataframe(file)
        self.__setDataframes()
        self.__assets_info.showInfo()
        self.__earns_costs_info.showInfo()


statistics_gui = ExtratoStatisticsGUI()
statistics_gui.setDataframe(st.session_state.extrato_file)
