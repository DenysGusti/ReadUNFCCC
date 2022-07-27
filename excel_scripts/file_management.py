from pathlib import Path


class Files:
    """
    File logic, from to
    """

    def __init__(self, *, folder_path: str):
        self._folder_path = Path(folder_path)
        self._data_path = self._folder_path / 'original'
        self._result_path = self._folder_path / 'extracted'

        self._countries_dir_list: list[Path] = [x for x in self._data_path.iterdir() if x.is_dir()]

        # List of worksheets (CRF tables) to be processed
        self._sheets_list: list[str] = ['Table4', 'Table4.1', 'Table4.A', 'Table4.B', 'Table4.C', 'Table4.D',
                                        'Table4.E', 'Table4.F']
            
        # Range of years CRF tables of which to be processed
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

    def createCountriesDict(self) -> dict[Path, list[Path]]:
        """
        dictionary - destination: list of countries
        """
        countries_dict: dict[Path, list[Path]] = {}
        for country_dir in self._countries_dir_list:
            result_file_path: Path = self._result_path / f"{country_dir.name[:8].replace('-', '_')}.xlsx"
            files_dir_list: list[Path] = [x for x in country_dir.glob('**/*.xlsx')
                                          if "~$" not in str(x) and x.name[9:13] in self._years]

            countries_dict[result_file_path] = files_dir_list

        return countries_dict
