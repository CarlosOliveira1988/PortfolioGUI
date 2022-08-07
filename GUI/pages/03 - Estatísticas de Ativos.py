import pandas as pd
import streamlit as st

from extrato.lib.extrato_columns import ExtratoColumns
from extrato.lib.extrato_side_bar import ExtratoSideBar
from extrato.lib.extrato_statistics import StatisticsInterface


class ExtratoAssetsInfo:
    def __init__(self) -> None:
        """Structure used to show a Bar Chart and other information related to the 'Extrato Assets'.
        
        This class uses the following considerations:
        - column 'Data': filtering data
        - column 'Venda': positive values (put money in the account)
        - column 'Compra': negative values (take money out the account)
        """
        self.__columns_object = ExtratoColumns()
        self.__statistics = StatisticsInterface(
            self.__columns_object._sell_price_col.getName(),
            self.__columns_object._buy_price_col.getName(),
        )
        
    def setDataframe(self, dataframe: pd.DataFrame) -> None:
        self.__statistics.setDataframe(dataframe)
    
    def showInfo(self) -> None:
        st.write('#### Compras e Vendas de ativos no período [R$]')
        st.bar_chart(self.__statistics.getResultDataframe())
        st.write('__Vendas:__ ', self.__statistics.getPositiveOperationString())
        st.write('__Compras:__ ', self.__statistics.getNegativeOperationString())
        st.write('__Diferença:__ ', self.__statistics.getDeltaOperationString())
        expander = st.expander("Informações:")
        expander.write("""
            O gráfico acima mostra os valores de __Compras__ e __Vendas__ de ativos ao longo do período informado.
            \n\nEsses valores são representados na coluna __Operação__ como __Compra__ e __Venda__.
        """)


class ExtratoEarnsCostsInfo:
    def __init__(self) -> None:
        """Structure used to show a Bar Chart and other information related to the 'Extrato Earns & Costs'.
        
        This class uses the following considerations:
        - column 'Data': filtering data
        - column 'Proventos Totais': positive values (put money in the account)
        - column 'Custo Total': negative values (take money out the account)
        """
        self.__columns_object = ExtratoColumns()
        self.__statistics = StatisticsInterface(
            self.__columns_object._total_earnings_col.getName(),
            self.__columns_object._total_costs_col.getName(),
        )
        
    def setDataframe(self, dataframe: pd.DataFrame) -> None:
        self.__statistics.setDataframe(dataframe)
    
    def showInfo(self) -> None:
        st.write('#### Proventos e Custos no período [R$]')
        st.bar_chart(self.__statistics.getResultDataframe())
        st.write('__Proventos:__ ', self.__statistics.getPositiveOperationString())
        st.write('__Custos:__ ', self.__statistics.getNegativeOperationString())
        st.write('__Diferença:__ ', self.__statistics.getDeltaOperationString())
        expander = st.expander("Informações:")
        expander.write("""
            O gráfico acima mostra os valores de __Proventos__ e __Custos__ ao longo do período informado.
            \n\nEsses valores são calculados a partir das colunas __Dividendos__, __JCP__, __IR__ e __Taxas__.
        """)


class ExtratoStatisticsGUI:
    def __init__(self) -> None:
        """Structure used to show data, graphs and filters related to Extrato."""
        self.__side_bar = ExtratoSideBar(operation_filter=False)
        self.__assets_info = ExtratoAssetsInfo()
        self.__earns_costs_info = ExtratoEarnsCostsInfo()
        self.__setDataframes()

    def __setDataframes(self) -> None:
        self.__assets_info.setDataframe(self.__side_bar.getFilteredDataframe())
        self.__earns_costs_info.setDataframe(self.__side_bar.getFilteredDataframe())

    def setDataframe(self, dataframe: pd.DataFrame) -> None:
        self.__side_bar.updateDataframe(dataframe)
        self.__setDataframes()
        self.__assets_info.showInfo()
        self.__earns_costs_info.showInfo()


statistics_gui = ExtratoStatisticsGUI()
statistics_gui.setDataframe(st.session_state.extrato_dataframe)
