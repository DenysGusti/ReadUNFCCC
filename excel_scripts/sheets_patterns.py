import pandas as pd


class SheetsPatterns:
    """
    Different processing for every xlsx sheet type
    """

    @staticmethod
    def Table4(file_dir):
        df: pd.DataFrame = pd.read_excel(file_dir, sheet_name='Table4', engine='openpyxl')

# TODO Table4 обробка
# test
