import pandas as pd

from math import nan, isnan
from pathlib import Path

from auxiliary_functions import calculateTime, writeFile


class TimeSeries:
    """
    makes structured table
    """

    def __init__(self, parameters: dict[str, dict[str, list[str | float]]], years_list: list[int], result_path: Path,
                 countries_names: list[Path]):
        self._parameters: dict[str, dict[str, list[str]]] = parameters
        self._years_list: list[int] = years_list
        self._countries_names: list[Path] = countries_names

        writeFile(destination=result_path, sheet_df_dict=self.makeCountriesData())

    @calculateTime
    def makeCountriesData(self) -> dict[str, pd.DataFrame]:
        result_dict: dict[str, pd.DataFrame] = {}

        # only for Table4.Alpha
        for sheet, tables in self._parameters.items():
            new_data: dict[str | int, list] = {'Country_ISO': [x.name[:3] for x in self._countries_names]}

            # common name
            for i, category in enumerate(['Category', 'Subcategory', 'Column_0', 'Column_1', 'Column_2', 'Units']):
                new_data[category] = [''.join(t[0] for t in zip(*[v[i] for v in tables.values()])
                                              if t.count(t[0]) == len(t)).rstrip()
                                      if all(isinstance(v[i], str) for v in tables.values()) else nan
                                      for _ in self._countries_names]

            for year in self._years_list:
                new_data[year] = [0] * len(self._countries_names)

            for idx, country in enumerate(self._countries_names):
                for table, list_of_parameters in tables.items():
                    country_data: dict = pd.read_excel(country, sheet_name=table, engine='openpyxl').to_dict()
                    columns: list[str] = list(country_data.keys())[:5]

                    rows: list[int] = [i for i in list(country_data.values())[0].keys() if all(  # indexes
                        list_of_parameters[j] in cell
                        if isinstance(cell := country_data[columns[j]][i], str) and isinstance(
                            list_of_parameters[j], str) else True for j in range(5))]

                    for y in self._years_list:
                        new_data[y][idx] += sum(
                            cell if isinstance(cell := country_data[y][r], float) and not isnan(cell) else 0 for r in
                            rows)

            result_dict[sheet] = pd.DataFrame(data=new_data)

        return result_dict
