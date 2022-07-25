from time import time
from pathlib import Path
from sheets_patterns import SheetsPatterns


def calculate_time(func):
    def wrapper(*args, **kwargs):
        t = time()
        returned_value = func(*args, **kwargs)
        print(f'time spent in {func.__name__}: {time() - t}s')
        return returned_value

    return wrapper


class TableCreation:
    """
    File logic
    """

    def __init__(self, *, folder_path: str):
        self._folder_path = Path(folder_path)
        self._data_path = self._folder_path / 'original'
        self._result_path = self._folder_path / 'extracted'

        self._countries_dir_list: list[Path] = [x for x in self._data_path.iterdir() if x.is_dir()]

        self._sheets_list: list[str] = ['Table4', 'Table4.1', 'Table4.A', 'Table4.B', 'Table4.C', 'Table4.D',
                                        'Table4.E', 'Table4.F']

        self._years: list[str] = [str(i) for i in range(1990, 2020)]

    @property
    def countriesDirList(self) -> list[Path]:
        return self._countries_dir_list

    @countriesDirList.setter
    def countriesDirList(self, country_folder_names: tuple[str]):
        self._countries_dir_list = [self._data_path / x for x in country_folder_names]

    @property
    def sheetsList(self) -> list[str]:
        return self._sheets_list

    @sheetsList.setter
    def sheetsList(self, new_sheets_list: tuple[str]):
        self._sheets_list = list(new_sheets_list)

    @property
    def years(self) -> list[str]:
        return self._years

    @years.setter
    def years(self, new_years: tuple[int]):
        self._years = [str(i) for i in new_years]

    @calculate_time
    def makeTables(self):
        for country_dir in self._countries_dir_list:
            print(country_dir)

            result_file_path: Path = self._result_path / f"{country_dir.name[:8].replace('-', '_')}.xlsx"
            files_dir_list: list[Path] = [x for x in country_dir.glob('**/*.xlsx')
                                          if "~$" not in str(x) and x.name[9:13] in self._years]
            print(f'{result_file_path = }\n{files_dir_list = }')

            for file_dir in files_dir_list:
                year: str = file_dir.name[9:13]
                print(f'{year = }')

                for sheet in self._sheets_list:
                    match sheet:
                        case 'Table4':
                            SheetsPatterns.Table4(file_dir)
                        case _:
                            print("TODO")
