import pandas as pd
import streamlit as st

from positions.lib.closed_dataframes_kit import ClosedPositionDBKit
from positions.lib.closed_side_bar import ClosedPositionDBSideBar


class ClosedPositionsTableInfo:
    def __init__(self) -> None:
        """Structure used to show an interactive table related to the 'Closed Positions'."""
        self.__filtered_fmtdf = ClosedPositionDBKit().getFormattedDataframe()

    def __showMainTitle(self) -> None:
        st.write('#### Histórico de posições encerradas')
    
    def __showDataframe(self) -> None:
        st.write("", self.__filtered_fmtdf.astype(str))
        expander = st.expander("Informações:")
        expander.write("""A tabela acima mostra todas as __Posições Encerradas__ registradas na planilha __Extrato__.
            As  __Posições Encerradas__ são identificadas a partir das colunas __Ticker__ e __Quantidade__,
            combinadas com as colunas __Data__ e __Operação__. Basicamente:\n\n1. a tabela da planilha __Extrato__ é 
            ordenada pela coluna __Data__; então, gera-se uma lista de __Ticker__;\n2. para cada __Ticker__ da lista,
            o algoritmo irá buscar quantidades associadas à __Operação:Compra__ e __Operação:Venda__, varrendo linha 
            a linha da planilha __Extrato__, somando as quantidades de cada linha; \n3. quando o somatório da __quantidade
            de compra__ for igual ao somatório da __quantidade de venda__, então temos uma __Posição Encerrada__.
            """
        )

    def setDataframe(self, dataframe: pd.DataFrame) -> None:
        self.__filtered_fmtdf = dataframe
    
    def showInfo(self) -> None:
        self.__showMainTitle()
        self.__showDataframe()


class ClosedPositionGUI:
    def __init__(self) -> None:
        """Structure used to show tables and filters related to Closed Positions."""
        self.__side_bar = ClosedPositionDBSideBar()
        self.__table = ClosedPositionsTableInfo()
        self.__setDataframes()

    def __setDataframes(self) -> None:
        self.__table.setDataframe(self.__side_bar.getFilteredFormattedDataframe())

    def setDataframe(self, dataframe: pd.DataFrame) -> None:
        self.__side_bar.updateDataframe(dataframe)
        self.__setDataframes()
        self.__table.showInfo()


closed_position_gui = ClosedPositionGUI()
closed_position_gui.setDataframe(st.session_state.extrato_from_excel)
