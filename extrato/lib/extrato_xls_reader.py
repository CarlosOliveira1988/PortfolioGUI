import pandas as pd

from extrato.lib.extrato_dataframes_kit import ExtratoKit


class ExtratoExcelReader(ExtratoKit):
    def __init__(self) -> None:
        """Structure used to read Excel files related to Extrato."""
        super().__init__()

    def readExcelFile(self, file: str) -> None:
        self._raw_df = self.addColumnIfNotExists(pd.read_excel(file))
        self.formatDataframes()
