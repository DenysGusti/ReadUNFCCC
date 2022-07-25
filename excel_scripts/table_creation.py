import pandas as pd
import logging
from pathlib import Path
from sheets_patterns import Patterns
from auxiliary_functions import calculate_time


class Table:
    """
    making xlsx file
    """

    def __init__(self, *, country_dest: Path, country_sources: list[Path], sheets_list: list[str]):
        self._country_dest: Path = country_dest
        self._country_sources: list[Path] = country_sources
        self._sheets_list: list[str] = sheets_list
        self._sheet_df_dict: dict[str, pd.DataFrame] = self.createDataDict()

    def getYearTableDict(self, sheet_name: str) -> dict[int, dict]:
        return {int(file_path.name[9:13]): pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl').to_dict()
                for file_path in self._country_sources}

    @calculate_time
    def createDataDict(self) -> dict[str: pd.DataFrame]:
        sheet_df_dict: dict[str: pd.DataFrame] = dict()
        processed_data: dict[str, list] = dict()

        for sheet in self._sheets_list:
            year_df_dict: dict[int, dict[str, dict]] = self.getYearTableDict(sheet)
            table = Patterns(year_df_dict)
            flag: bool = True

            match sheet:
                case 'Table4' | 'Table4.1':
                    processed_data: dict[str, list] = table.Table4X()

                case sheet if sheet[-1].isalpha() and sheet[-1].isupper():
                    print(f'TODO alpha {sheet}')

                case sheet if sheet[6] == '(' and sheet[-1] == ')':
                    print(f'roman {sheet} not planned yet')

                case 'Table4.Gs1' | 'Table4.Gs2':
                    print(f'new {sheet} not planned yet')

                case _:
                    flag = False
                    print(f'Unexpected sheet name: {sheet}')

            if flag:
                sheet_df_dict[sheet] = pd.DataFrame(data=processed_data)

        return sheet_df_dict

    def writeFile(self):
        try:
            with pd.ExcelWriter(self._country_dest, engine='openpyxl') as writer:
                for sheet, df in self._sheet_df_dict.items():
                    df.to_excel(writer, sheet_name=sheet, index=False)

        except PermissionError:
            logging.exception("\n\nClose destination xlsx files!\n\n")
