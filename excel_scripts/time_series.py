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


        for sheet, tables in self._parameters.items():
            new_data: dict[str | int, list] = {'Country_ISO': [x.name[:3] for x in self._countries_names]}
#------------------------------
            if isinstance(tables[list(tables.keys())[0]][0], list): #Table4.1
                #print('new variant', tables[list(tables.keys())[0]], len(tables[list(tables.keys())[0]]))
                #print('new variant1', tables[list(tables.keys())[0]][1], len(tables[list(tables.keys())[0]][0]),{0:list(tables.values())[0][1]}.values())

                # common name
                category_number: int = len(list(tables.values())[0][0])
                category_list3: str[3] = ['Category', 'Subcategory', 'Units']
                category_list5: str[5] = ['Category', 'Subcategory', 'Column_0', 'Column_1', 'Units']
                category_list6: str[6] = ['Category', 'Subcategory', 'Column_0', 'Column_1', 'Column_2', 'Units']
                category_list = category_list6 if category_number > 5 else (
                    category_list3 if category_number < 5 else category_list5)
                # for i, category in enumerate(['Category', 'Subcategory', 'Column_0', 'Column_1', 'Column_2', 'Units']):
                #for k in range(len(tables[list(tables.keys())[0]])):
                for k in range(1):
                    tmpDict = {0: list(tables.values())[0][k]}
                    #print("tmpDict= ",tmpDict)
                    #print("category_list",category_list)
                    for i, category in enumerate(category_list):
                        new_data[category] = [''.join(l[0] for l in zip(*[v[i] for v in tmpDict.values()])
                                                          if l.count(l[0]) == len(l)).rstrip()
                                                  if all(isinstance(v[0], str) for v in tmpDict.values()) else nan
                                                  for _ in self._countries_names]

                    #print(new_data)

                    for year in self._years_list:
                        new_data[year] = [0] * len(self._countries_names)

                    for idx, country in enumerate(self._countries_names):
                        for table, list_of_parameters in tables.items():
                            country_data: dict = pd.read_excel(country, sheet_name=table, engine='openpyxl').to_dict()
                            #columns: list[str] = list(country_data.keys())[:5]
                            columns: list[str] = list(country_data.keys())[:category_number+1]
                            #print(list(country_data.values())[0].keys())
                            #print("columns all= ", list(country_data.keys()))
                            #print("columns= ", columns)
                            #print(list(country_data.values())[0].keys())
                            rows: list[int] = [i for i in list(country_data.values())[0].keys() if all(  # indexes
                                any(list_of_parameters[m][j] in cell
                                if (isinstance(cell := country_data[columns[j]][i], str) and (isinstance(
                                    list_of_parameters[m][j], str)) )  else True for m in range(len(tables[list(tables.keys())[0]]))) for j in range(category_number) )
                                               ]
                            #print(list_of_parameters[k][0])
                            #print("rows=", rows)

                            for y in self._years_list:
                                new_data[y][idx] += sum(
                                    cell if isinstance(cell := country_data[y][r], float) and not isnan(cell) else 0 for r
                                    in
                                    rows)
                #print(type(new_data),new_data)
                result_dict[sheet] = pd.DataFrame(data=new_data)

#----------------------------------------------
            else: # Table4.Alpha

                # common name
                category_number: int = len(list(tables.values())[0])
                category_list3: str[3] = ['Category', 'Subcategory', 'Units']
                category_list5: str[5] = ['Category', 'Subcategory', 'Column_0', 'Column_1', 'Units']
                category_list6: str[6] = ['Category', 'Subcategory', 'Column_0', 'Column_1', 'Column_2', 'Units']
                category_list = category_list6 if category_number > 5 else (
                    category_list3 if category_number < 5 else category_list5)
                # for i, category in enumerate(['Category', 'Subcategory', 'Column_0', 'Column_1', 'Column_2', 'Units']):
                for i, category in enumerate(category_list):
                    new_data[category] = [''.join(t[0] for t in zip(*[v[i] for v in tables.values()])
                                                  if t.count(t[0]) == len(t)).rstrip()
                                          if all(isinstance(v[i], str) for v in tables.values()) else nan
                                          for _ in self._countries_names]
                    #print(i, category, new_data[category])


                #print('--------')
                for year in self._years_list:
                    new_data[year] = [0] * len(self._countries_names)

                for idx, country in enumerate(self._countries_names):
                    for table, list_of_parameters in tables.items():
                        country_data: dict = pd.read_excel(country, sheet_name=table, engine='openpyxl').to_dict()
                        # columns: list[str] = list(country_data.keys())[:5]
                        columns: list[str] = list(country_data.keys())[:category_number]
                        #print("columns all= ", list(country_data.keys()))
                        #print("columns= ", columns)
                        rows: list[int] = [i for i in list(country_data.values())[0].keys() if all(  # indexes
                            list_of_parameters[j] in cell
                            if isinstance(cell := country_data[columns[j]][i], str) and isinstance(
                                # list_of_parameters[j], str) else True for j in range(5))]
                                list_of_parameters[j], str) else True for j in range(category_number))
                                           ]

                        for y in self._years_list:
                            new_data[y][idx] += sum(
                                cell if isinstance(cell := country_data[y][r], float) and not isnan(cell) else 0 for r
                                in
                                rows)

                result_dict[sheet] = pd.DataFrame(data=new_data)

        return result_dict

pd.Series