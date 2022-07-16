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

    def setDataframe(self, file: str) -> None:
        self.__side_bar.updateDataframe(file)
        self.__setDataframes()
        self.__table.showInfo()


closed_position_gui = ClosedPositionGUI()
closed_position_gui.setDataframe(st.session_state.extrato_file)
