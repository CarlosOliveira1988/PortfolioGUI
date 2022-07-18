import pandas as pd

from extrato.lib.extrato_dataframes_kit import DataframesDBKitInterface, ExtratoDBKit
from extrato.lib.extrato_columns import InvestmentPositionType

from positions.lib.closed_columns import ClosedPositionDBColumns


class ClosedPositionDBKit(DataframesDBKitInterface):
    def __init__(self) -> None:
        """Structure to handle a Pandas dataframe to show Closed Positions."""
        self.__columns_object = ClosedPositionDBColumns()
        super().__init__(self.__columns_object)
        
        self.__postitions_type = InvestmentPositionType()
        self.__extrato_kit_object = ExtratoDBKit()
        self.__addValuesToCalculatedColumns()
        self.formatDataframes()

    def __getFilteredSliceExtrato(self, slice_index: int) -> pd.DataFrame:
        extrato_df = self.__extrato_kit_object.getNotNanDataframe()
        
        extrato_df_columns_object = self.__extrato_kit_object.getColumnsObject()
        extrato_df_slice_index_col = extrato_df_columns_object._slice_index_col.getName()
        
        return extrato_df.loc[extrato_df[extrato_df_slice_index_col].isin([slice_index])]

    def __isClosedPositionSliceType(self, slice_index: int) -> bool:
        extrato_df_filtered_by_slice = self.__getFilteredSliceExtrato(slice_index)
        
        extrato_df_columns_object = self.__extrato_kit_object.getColumnsObject()
        extrato_df_slice_type_col = extrato_df_columns_object._slice_type_col.getName()
        
        closed_position = self.__postitions_type.getClosedPosition()
        
        return not extrato_df_filtered_by_slice.loc[
            extrato_df_filtered_by_slice[extrato_df_slice_type_col].isin([closed_position])
        ].empty

    def __addValuesToCalculatedColumns(self) -> None:
        extrato_df_slice_list = self.__extrato_kit_object.getNonDuplicatedListFromColumn(
            self.__extrato_kit_object.getColumnsObject()._slice_index_col.getName()
        )

        for slice_index in extrato_df_slice_list:
            if self.__isClosedPositionSliceType(slice_index):
                
                # Only for testing purpose
                extrato_df = self.__extrato_kit_object.getNotNanDataframe()
                extrato_df_columns_object = self.__extrato_kit_object.getColumnsObject()
                extrato_df_slice_index_col = extrato_df_columns_object._slice_index_col.getName()
                print(extrato_df.loc[
                    extrato_df[extrato_df_slice_index_col].isin([slice_index])
                ])
                
        # for index, df_line in df.iterrows():

    def readExcelFile(self, file) -> None:
        """Method Overridden from 'DataframesDBKitInterface' class."""
        self.__extrato_kit_object.readExcelFile(file)
        self.__addValuesToCalculatedColumns()
        self.formatDataframes()
