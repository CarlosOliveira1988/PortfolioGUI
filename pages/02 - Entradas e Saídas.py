import streamlit as st

from extrato_lib.extrato_side_bar import ExtratoDBSideBar
from extrato_lib.extrato_statistics import OperationTotalPriceStatistics


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
