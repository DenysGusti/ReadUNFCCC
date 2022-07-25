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

        print(self._country_dest, self._country_sources, self._sheets_list)

    def getYearTableDict(self, sheet_name: str) -> dict[int, dict]:
        return {int(file_path.name[9:13]): pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl').to_dict()
                for file_path in self._country_sources}

    @calculate_time
    def createFile(self) -> None:
        try:
            for sheet in self._sheets_list:
                match sheet:
                    case 'Table4':
                        print(f'TODO Table4')
                        year_df_dict: dict[int, dict[str, dict]] = self.getYearTableDict(sheet)
                        for k, v in year_df_dict.items():
                            print(f'\n\n{k}\n\n{v}\n\n')
                        table = Patterns(year_df_dict)
                        processed_data: dict[str, list] = table.Table4()
                        processed_df: pd.DataFrame = pd.DataFrame(data=processed_data)
                        processed_df.to_excel(self._country_dest, index=False)

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

        except PermissionError:
            logging.exception("\n\nClose destination xlsx files!\n\n")
