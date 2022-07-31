import pandas as pd
import streamlit as st

from extrato.lib.extrato_columns import ExtratoDBColumns
from extrato.lib.extrato_side_bar import ExtratoDBSideBar
from extrato.lib.extrato_statistics import StatisticsInterface


class ExtratoAccountInfo:
    def __init__(self) -> None:
        """Structure used to show a Bar Chart and other information related to the 'Extrato Account'.
        
        This class uses the following considerations:
        - column 'Data': filtering data
        - column 'Transferência': positive values (put money in the account)
        - column 'Resgate': negative values (take money out the account)
        """
        self.__columns_object = ExtratoDBColumns()
        self.__statistics = StatisticsInterface(
            self.__columns_object._contributions_col.getName(),
            self.__columns_object._rescues_col.getName(),
        )

    def setDataframe(self, dataframe: pd.DataFrame) -> None:
        self.__statistics.setDataframe(dataframe)
    
    def showInfo(self) -> None:
        st.write('#### Entradas e Saídas da conta no período [R$]')
        st.bar_chart(self.__statistics.getResultDataframe())
        st.write('__Transferências:__ ', self.__statistics.getPositiveOperationString())
        st.write('__Resgates:__ ', self.__statistics.getNegativeOperationString())
        st.write('__Diferença:__ ', self.__statistics.getDeltaOperationString())
        expander = st.expander("Informações:")
        expander.write("""
            O gráfico acima mostra os valores de __Entradas__ e __Saídas__ da conta de investimento ao 
            longo do período informado. \n\n Esses valores são representados na coluna __Operação__ como 
            __Transferência__ e __Resgate__.
        """)


class ExtratoAccountsGUI:
    def __init__(self) -> None:
        """Structure used to show data, graphs and filters related to Extrato."""
        self.__side_bar = ExtratoDBSideBar(market_filter=False, ticker_filter=False, operation_filter=False)
        self.__account_info = ExtratoAccountInfo()
        self.__setDataframes()

    def __setDataframes(self) -> None:
        self.__account_info.setDataframe(self.__side_bar.getFilteredDataframe())

    def setDataframe(self, file) -> None:
        self.__side_bar.updateDataframe(file)
        self.__setDataframes()
        self.__account_info.showInfo()


accounts_gui = ExtratoAccountsGUI()
accounts_gui.setDataframe(st.session_state.extrato_file)
