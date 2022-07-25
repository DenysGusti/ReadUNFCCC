import pandas as pd
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

        print(self._country_dest, self._country_sources, self._sheets_list)

    @calculate_time
    def createFile(self) -> None:

        def getYearDfDict(sheet_name: str) -> dict[str, pd.DataFrame]:
            return {file_path.name[9:13]: pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
                    for file_path in self._country_sources}

        for sheet in self._sheets_list:
            match sheet:
                case 'Table4':
                    print(f'TODO Table4')
                    year_df_dict = getYearDfDict(sheet)
                    for k, v in year_df_dict.items():
                        print(f'\n\n{k}\n\n{v}\n\n')
                    # SheetsPatterns.Table4(file_dir)

                case 'Table4.1':
                    print(f'TODO Table4.1')

                case sheet if sheet[-1].isalpha() and sheet[-1].isupper():
                    print(f'TODO alpha {sheet}')

                case sheet if sheet[6] == '(' and sheet[-1] == ')':
                    print(f'roman {sheet} not planned yet')

                case 'Table4.Gs1' | 'Table4.Gs2':
                    print(f'new {sheet} not planned yet')

                case _:
                    print(f'Unexpected sheet name: {sheet}')
