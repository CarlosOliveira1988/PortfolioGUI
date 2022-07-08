import os

from dotenv import load_dotenv


class FileManager:
    def __init__(self):
        """Structure used to manage the 'Extrato' User file."""
        self.__loadDotEnvFile()
        if not self.__dotEnvFileExists():
            self.__saveDotEnvFile(self.__getDefaultExtratoFile())
        self.__extrato_file = self.__getExtratoFile()

    def __loadDotEnvFile(self):
        load_dotenv(encoding="iso-8859-1")

    def __saveDotEnvFile(self, filename):
        with open(".env", "w") as file:
            file.write("EXTRATO_PATH=" + filename)

    def __dotEnvFileExists(self):
        # When the .ENV file does not exist; or
        # When the parameter does not exist inside the .ENV file;
        # Then the 'dotenv' API returns 'None'
        return self.__getUserExtratoFile() is not None

    def __getDefaultExtratoFile(self):
        DEFAULT_DIRECTORY = os.path.join(os.getcwd(), "templates")
        FILE_NAME = "EXTRATO_TEMPLATE_EMPTY.xlsx"
        return os.path.join(DEFAULT_DIRECTORY, FILE_NAME)

    def __getUserExtratoFile(self):
        return os.getenv("EXTRATO_PATH")

    def __isValidExtratoFile(self, file):
        try:
            return os.path.isfile(file)
        except TypeError:
            return False

    def __getExtratoFile(self):
        user_file = self.__getUserExtratoFile()
        if self.__isValidExtratoFile(user_file):
            return user_file
        else:
            return self.__getDefaultExtratoFile()

    def getExtratoFile(self):
        """Return the Extrato spreadsheet file.

        When the user file is not found, then returns the default file.
        """
        return self.__extrato_file

    def setExtratoFile(self, file):
        """Set the path related to the Extrato spreadsheet in the .ENV file."""
        self.__saveDotEnvFile(file)
        self.__extrato_file = file
