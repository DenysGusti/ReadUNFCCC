import pandas as pd
import logging
import math
from pathlib import Path
from auxiliary_functions import calculate_time


class Structuration:
    """
    makes structured table
    """

    def __init__(self, *, folder_path: str):
        self._folder_path = Path(folder_path)
        self._data_path = self._folder_path / 'extracted'
        self._result_path = self._folder_path / 'structured' / 'UNFCC_t.xlsx'

        # names without units and '. '! copy from extracted
        # sheet - sum of parameters: table - row and column categories
        self._parameters: dict[str, dict[str, list[str]]] = {
            'Deforestation': {
                'Table4.B': ['Forest land converted to', '', 'ACTIVITY DATA', 'Total area(2)', '', '(kha)'],
                'Table4.C': ['Forest land converted to', '', 'ACTIVITY DATA', 'Total area(2)', '', '(kha)'],
                'Table4.D': ['Forest land converted to', '', 'ACTIVITY DATA', 'Total area(2)', '', '(kha)'],
                'Table4.E': ['Forest land converted to', '', 'ACTIVITY DATA', 'Total area(2)', '', '(kha)'],
                'Table4.F': ['Forest land converted to', '', 'ACTIVITY DATA', 'Total area(2)', '', '(kha)']
            },
            'Net DW (t C per ha)': {  # '/', ':' invalid
                'Table4.A': ['1. Forest land remaining forest land', '', 'IMPLIED CARBON-STOCK-CHANGE FACTORS',
                             'Net carbon stock change in dead wood per area(4)', '', '(t C/ha)']
            },
            'Net DW (kt C)': {
                'Table4.A': ['1. Forest land remaining forest land', '',
                             'CHANGES IN CARBON STOCK AND NET CO2 EMISSIONS/REMOVALS FROM SOILS',
                             'Net carbon stock change in dead wood(4)', '', '(kt C)']
            }
        }

        self._countries_names: list[Path] = [x for x in self._data_path.iterdir() if x.is_file()]

    @property
    def parameters(self) -> dict[str, dict[str, list[str]]]:
        return self._parameters

    @parameters.setter
    def parameters(self, param: dict[str, dict[str, list[str]]]):
        self._parameters = param

    @property
    def countriesNames(self) -> list[Path]:
        return self._countries_names

    @countriesNames.setter
    def countriesNames(self, countries_names: tuple[str]):
        self._countries_names = [self._data_path / f'{x}.xlsx' for x in countries_names]

    @calculate_time
    def makeCountriesData(self) -> dict[str, pd.DataFrame]:
        result_dict: dict[str, pd.DataFrame] = dict()

        # only for Table4.Alpha
        for sheet, tables in self._parameters.items():
            new_data: dict[str | int, list] = dict()
            new_data['Country_ISO'] = [x.name[:3] for x in self._countries_names]

            for i, k in enumerate(['Category', 'Subcategory', 'Column_0', 'Column_1', 'Column_2', 'Units']):
                new_data[k] = [''.join(t[0] for t in zip(*[v[i] for v in tables.values()])
                                       if t.count(t[0]) == len(t)).rstrip() for _ in range(len(self._countries_names))]

            for year in range(1990, 2020):
                new_data[year] = [0 for _ in range(len(self._countries_names))]

            for num, country in enumerate(self._countries_names):

                for table, list_of_parameters in tables.items():
                    country_data: dict = pd.read_excel(country, sheet_name=table, engine='openpyxl').to_dict()

                    rows: list[int] = []
                    for i in range(len(list(country_data.values())[0])):
                        if all((type(country_data[list(country_data.keys())[:5][j]][i]) == str and
                                list_of_parameters[j] in country_data[list(country_data.keys())[:5][j]][i]) or
                               (type(country_data[list(country_data.keys())[:5][j]][i]) == float and
                                math.isnan(country_data[list(country_data.keys())[:5][j]][i]) and
                                list_of_parameters[j] == '') for j in range(5)):  # nan == ''
                            rows.append(i)

                    for year in list(country_data.keys())[6:]:
                        new_data[year][num] += sum(
                            country_data[year][row] if type(country_data[year][row]) == float and not math.isnan(
                                country_data[year][row]) else 0 for row in rows)

            result_dict[sheet] = pd.DataFrame(data=new_data)

        return result_dict

    def writeFile(self, sheet_df_dict: dict[str, pd.DataFrame]):
        try:
            with pd.ExcelWriter(self._result_path, engine='openpyxl') as writer:
                for sheet, df in sheet_df_dict.items():
                    df.to_excel(writer, sheet_name=sheet, index=False)

        except PermissionError:
            logging.exception("\n\nClose destination xlsx files!\n\n")
