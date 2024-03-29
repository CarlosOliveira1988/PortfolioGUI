import os

from dotenv import load_dotenv


class FileManager:
    def __init__(self) -> None:
        """Structure used to manage the 'Extrato' User file."""
        self.__loadDotEnvFile()
        if not self.__dotEnvFileExists():
            self.__saveDotEnvFile(self.__getDefaultExtratoFile())
        self.__extrato_file = self.__getExtratoFile()

    def __loadDotEnvFile(self) -> None:
        load_dotenv(encoding="iso-8859-1")

    def __saveDotEnvFile(self, filename: str) -> None:
        with open(".env", "w") as file:
            file.write("EXTRATO_PATH=" + filename)

    def __dotEnvFileExists(self) -> str:
        # When the .ENV file does not exist; or
        # When the parameter does not exist inside the .ENV file;
        # Then the 'dotenv' API returns 'None'
        return self.__getUserExtratoFile() is not None

    def __getDefaultExtratoFile(self) -> str:
        DEFAULT_DIRECTORY = os.path.join(os.getcwd(), "templates")
        FILE_NAME = "EXTRATO_TEMPLATE_EMPTY.xlsx"
        return os.path.join(DEFAULT_DIRECTORY, FILE_NAME)

    def __getUserExtratoFile(self) -> str:
        return os.getenv("EXTRATO_PATH")

    def __isValidExtratoFile(self, file: str) -> bool:
        try:
            return os.path.isfile(file)
        except TypeError:
            return False

    def __getExtratoFile(self) -> str:
        user_file = self.__getUserExtratoFile()
        if self.__isValidExtratoFile(user_file):
            return user_file
        else:
            return self.__getDefaultExtratoFile()

    def getExtratoFile(self) -> str:
        """Return the Extrato spreadsheet file.

        When the user file is not found, then returns the default file.
        """
        return self.__extrato_file

    def setExtratoFile(self, file) -> None:
        """Set the path related to the Extrato spreadsheet in the .ENV file."""
        self.__saveDotEnvFile(file)
        self.__extrato_file = file
