import pandas as pd
import numpy as np
import copy

import openpyxl

from pathlib import Path

from auxiliary_functions import calculateTime, writeFile, clearStr


class Patterns:
    """
    Different processing for every xlsx sheet type (i.e. CRT table type)
    """

    def __init__(self, year_df_dict: dict[int, dict[str, dict]]):
        self._year_df_dict: dict[int, dict[str, dict]] = year_df_dict
        self._name, self._last_row, self._structure = self.getInfo()

    def getInfo(self) -> tuple[str, int, dict[str, dict]]:
        first_year: int = min(self._year_df_dict.keys())
        old_structure: dict[str, dict] = self._year_df_dict[first_year]
        name: str = list(old_structure.keys())[1]

        # cutting the rows over the table
        min_row: int = min(row for row, cell in old_structure[name].items()
                           if row > 0 and isinstance(old_structure[name][row - 1], float) and isinstance(cell, str))
        min_row = min_row+1 # remove 'Back to index'
#        print(old_structure[name].items())
#       for row, cell in old_structure[name].items():
#            #if str(cell)[:3] == '(1)':
#            print(str(cell)[:3])
#            print(f"Row: {row}, Cell: {cell}")
        max_row: int = min(row - 1 for row, cell in old_structure[name].items() if str(cell)[:3] == '(1)' or str(cell)[:5] == 'Note:')

        # in Gs2 there is additional info after (1)...!

        new_structure: dict[str, dict] = {k: {row: data for row, data in v.items() if min_row <= row <= max_row}
                                          for k, v in old_structure.items()}
        # Remove the first key-value pair
        first_key = next(iter(new_structure))  # Get the first key
        new_structure.pop(first_key)  # Remove it

        #print(new_structure)
        return name, max_row, new_structure

    def Table4Digit(self) -> dict[str | int, list]:
        new_data: dict[str | int, list] = {}

        #deep_copy = copy.deepcopy(new_structure)

        orig_row_names = list(self._structure[self._name].values())

        match self._name:
            case 'TABLE 4 SECTORAL REPORT FOR LAND USE, LAND-USE CHANGE AND FORESTRY':
                table_name: str = f'{self._name}     {orig_row_names[0]}'

            case 'Table 4.1  LAND TRANSITION MATRIX':
                table_name: str = f'{self._name}     {orig_row_names[1]} {orig_row_names[0]}'

            case 'TABLE 3 SECTORAL REPORT FOR AGRICULTURE':
                table_name: str = f'{self._name}     {orig_row_names[0]}'

            case _:
                table_name = ''
                print('Unexpected table name')

        new_data[table_name] = [clearStr(x) for x in orig_row_names[2:]]
        first_row: int = list(self._structure[self._name].keys())[0]

#        for el in new_data[table_name]:
#            for v in list(self._structure.values())[1:]:
#                print(v[first_row+1])
#                print(clearStr(v[first_row+]))
#                print("---")

        new_data['Column'] = [clearStr(v[first_row]) for v in list(self._structure.values())[1:]]
        old_len = len(new_data[table_name])
        new_data[table_name] = [el for el in new_data[table_name] for _ in new_data['Column']]

        units: str = self._structure[list(self._structure.keys())[1]][first_row + 1]
        new_data['Column'] *= old_len
        new_data['Units'] = [units] * len(new_data['Column'])

        for year, data in self._year_df_dict.items():  # data start from 8th row
            #new_data[year] = [cells[i] for i in range(5, self._last_row + 1) for cells in list(data.values())[1:]]
            new_data[year] = [cells[i] for i in range(8, self._last_row + 1) for cells in list(data.values())[2:]]

        return new_data

    def Table4Alpha(self) -> dict[str | int, list]:
        new_data: dict[str | int, list] = {}

        orig_row_names = list(self._structure[self._name].values())
        table_name: str = f'{self._name}     {orig_row_names[0]} {orig_row_names[1]}'
        new_data[table_name] = [clearStr(x) if isinstance(x, str) else x for x in orig_row_names[4:]]

        sub_name: str = list(self._structure.keys())[1]
        orig_sub_names = list(self._structure[sub_name].values())
        sub_table_name: str = f'Subcategory     {orig_sub_names[1]}'
        new_data[sub_table_name] = [clearStr(x) if isinstance(x, str) else x for x in orig_sub_names[4:]]

        first_row: int = list(self._structure[self._name].keys())[0]
        orig_col_names = list(self._structure.values())[2:]
        del orig_col_names[-2:]  # Deletes the last 2 elements / the empty column and the "Additional information"

        for i in range(first_row, first_row + 4):
        #for i in range(first_row, first_row + 3):
            new_data[f'Column_{min(i - first_row, 3)}'] = [clearStr(v[i])
                                                           if isinstance(v[i], str) else v[i] for v in orig_col_names]

        units_size: int = len(list(new_data['Column_3']))
        #new_data['Units']: list[str] = [''] * 3
        new_data['Units']: list[str] = [''] * units_size
        for i in range(units_size):
            #new_data['Column_1'][i], new_data['Units'][i] = new_data['Column_1'][i][:-5], new_data['Column_1'][i][-5:]
            new_data['Units'][i] = new_data['Column_3'][i]
        previous = None
        for i in range(units_size):
            if isinstance(new_data['Units'][i], float) and np.isnan(new_data['Units'][i]):  # Check if it's NaN
                new_data['Units'][i] = previous
            else:
                previous = new_data['Units'][i]  # Update previous non-NaN value

        del new_data['Column_3'] # it was a temporary column for selecting units

        for c in ['Units', 'Column_0', 'Column_1']:
            for i, el in enumerate(new_data[c]):
                if isinstance(el, float) and (
                        c != 'Column_1' or c == 'Column_1' and isinstance(new_data['Column_2'][i], str)):
                    new_data[c][i] = new_data[c][i - 1]

        old_len = len(new_data[table_name])
        for category in [table_name, sub_table_name]:
            new_data[category] = [el for el in new_data[category] for _ in new_data['Units']]

        for i in range(3):
            new_data[f'Column_{i}'] *= old_len
        new_data['Units'] *= old_len

        for year, data in self._year_df_dict.items():  # data start from 8th row
            #new_data[year] = [cells[i] for i in range(8, self._last_row + 1) for cells in list(data.values())[2:]]
            new_data[year] = [cells[i] for i in range(8, self._last_row + 1) for cells in list(data.values())[3:-2]] # #3:-2 to cut off additional information (ignoring at the moment)

        return new_data

    def Table4Brackets(self) -> dict[str | int, list]:
        new_data: dict[str | int, list] = {}

        orig_row_names = list(self._structure[self._name].values())
        table_name: str = f'{self._name}     {orig_row_names[0]} {orig_row_names[1]}'
        new_data[table_name] = [clearStr(x) if isinstance(x, str) else x for x in orig_row_names[3:]]

        sub_name: str = list(self._structure.keys())[1]
        orig_sub_names = list(self._structure[sub_name].values())
        sub_table_name: str = f'Subcategory     {orig_sub_names[1]}'
        new_data[sub_table_name] = [clearStr(x) if isinstance(x, str) else x for x in orig_sub_names[3:]]

        first_row: int = list(self._structure[self._name].keys())[0]
        orig_col_names = list(self._structure.values())[2:]

        for i in range(first_row, first_row + 3):
            new_data[f'Column_{min(i - first_row, 2)}'] = [clearStr(v[i])
                                                           if isinstance(v[i], str) else v[i] for v in orig_col_names]

        new_data['Units']: list[str] = [''] * 3
        for i in range(3):
            #new_data['Column_2'][i], new_data['Units'][i] = new_data['Column_2'][i][:-5], new_data['Column_2'][i][-5:]
            new_data['Units'][i] = new_data['Column_2'][i]
        new_data['Units'] += [x[first_row + 2] for x in orig_col_names[3:]]

        units_size: int = len(list(new_data['Column_2']))
        previous = None
        for i in range(units_size):
            if isinstance(new_data['Units'][i], float) and np.isnan(new_data['Units'][i]):  # Check if it's NaN
                new_data['Units'][i] = previous
            else:
                previous = new_data['Units'][i]  # Update previous non-NaN value

        for c in ['Units', 'Column_0', 'Column_1']:
            for i, el in enumerate(new_data[c]):
                if isinstance(el, float) and (
                        c != 'Column_1' or c == 'Column_1' and isinstance(new_data['Column_2'][i], str)):
                    new_data[c][i] = new_data[c][i - 1]

        del new_data['Column_2']

        old_len = len(new_data[table_name])
        for category in [table_name, sub_table_name]:
            new_data[category] = [el for el in new_data[category] for _ in new_data['Units']]

        for i in range(2):
            new_data[f'Column_{i}'] *= old_len
        new_data['Units'] *= old_len

        for year, data in self._year_df_dict.items():  # data start from 8th row
            new_data[year] = [cells[i] for i in range(8, self._last_row + 1) for cells in list(data.values())[3:]]

        return new_data


    def Table3Alpha(self) -> dict[str | int, list]:
        new_data: dict[str | int, list] = {}

        orig_row_names = list(self._structure[self._name].values())
        table_name: str = f'{self._name}     {orig_row_names[0]} {orig_row_names[1]}'
        #new_data[table_name] = [clearStr(x) if isinstance(x, str) else x for x in orig_row_names[5:]]
        new_data[table_name] = [clearStr(x) if isinstance(x, str) else x for x in orig_row_names[3:]]

        sub_name: str = list(self._structure.keys())[1]
        orig_sub_names = list(self._structure[sub_name].values())
        #sub_table_name: str = f'Subcategory     {orig_sub_names[1]}'
        #new_data[sub_table_name] = [clearStr(x) if isinstance(x, str) else x for x in orig_sub_names[5:]]

        first_row: int = list(self._structure[self._name].keys())[0]
        #orig_col_names = list(self._structure.values())[2:]
        #orig_col_names = list(self._structure.values())[1:]
        orig_col_names = list(self._structure.values())[1:6] # #1:6 to cut off additional information (ignoring at the moment)

        for i in range(first_row, first_row + 2):
            new_data[f'Column_{min(i - first_row, 2)}'] = [clearStr(v[i])
                                                           if isinstance(v[i], str) else v[i] for v in orig_col_names]

#        new_data['Units']: list[str] = [''] * 3
#        for i in range(3):
#            new_data['Column_1'][i], new_data['Units'][i] = new_data['Column_1'][i][:-5], new_data['Column_1'][i][-5:]
#            print(new_data['Column_1'][i])
#            print(new_data['Column_1'][i][:-5])
        #new_data['Units'] += [x[first_row + 2] for x in orig_col_names[3:]]
        new_data['Units'] = [x[first_row + 2] for x in orig_col_names[0:]]

        for c in ['Units', 'Column_0', 'Column_1']:
            for i, el in enumerate(new_data[c]):
                if isinstance(el, float) and (
                        c != 'Column_1' or c == 'Column_1' and isinstance(new_data['Column_2'][i], str)):
                    new_data[c][i] = new_data[c][i - 1]

        old_len = len(new_data[table_name])
#        for category in [table_name, sub_table_name]:
#            new_data[category] = [el for el in new_data[category] for _ in new_data['Units']]

        for i in range(2):
            new_data[f'Column_{i}'] *= old_len
        new_data['Units'] *= old_len

        for year, data in self._year_df_dict.items():  # data start from 8th row
            #new_data[year] = [cells[i] for i in range(8, self._last_row + 1) for cells in list(data.values())[2:]]
            new_data[year] = [cells[i] for i in range(8, self._last_row + 1) for cells in list(data.values())[2:7]] # 2:7 to cut off additional information (ignoring at the moment)

#        for k,v in new_data.items():
#            print(f"{k}\n{v}\n{len(v)}")
#        print(new_data)

        new_data[list(new_data.keys())[0]] = [x for x in new_data[list(new_data.keys())[0]] for _ in range(5)]

        return new_data


    def Table3Beta(self) -> dict[str | int, list]:
        new_data: dict[str | int, list] = {}

        orig_row_names = list(self._structure[self._name].values())
        table_name: str = f'{self._name}     {orig_row_names[0]} {orig_row_names[1]}'
        #new_data[table_name] = [clearStr(x) if isinstance(x, str) else x for x in orig_row_names[5:]]
        new_data[table_name] = [clearStr(x) if isinstance(x, str) else x for x in orig_row_names[4:]]

        first_row: int = list(self._structure[self._name].keys())[0]
        #orig_col_names = list(self._structure.values())[2:]
        orig_col_names = list(self._structure.values())[1:10] #1:10 to cut off additional information (ignoring at the moment)

        for i in range(first_row, first_row + 4):
            new_data[f'Column_{min(i - first_row, 3)}'] = [clearStr(v[i])
                                                           if isinstance(v[i], str) else v[i] for v in orig_col_names]


#        print(orig_col_names)
#        print(orig_col_names[0][3])
#        print(orig_col_names[0][6])
#        print(orig_col_names[1][3])
#        print(orig_col_names[1][4])

        new_data['Units'] = new_data.pop('Column_3')
        new_data['Units'][2] = new_data['Units'][1]
        new_data['Units'][3] = new_data['Units'][1]

        old_len = len(new_data[table_name])

        for i in range(3):
            new_data[f'Column_{i}'] *= old_len
        new_data['Units'] *= old_len

        for year, data in self._year_df_dict.items():  # data start from 8th row / 11th row - additional information (ignoring at the moment)
            new_data[year] = [cells[i] for i in range(8, self._last_row + 1) for cells in list(data.values())[2:11]]

           # for k,v in new_data.items():
           #     print(f"{k}\n{v}\n{len(v)}")
           # print(new_data)

        new_data[list(new_data.keys())[0]] = [x for x in new_data[list(new_data.keys())[0]] for _ in range(9)]

        return new_data


class TableCreation:
    """
    making xlsx file
    """

    def __init__(self, country_destination: Path, country_sources: list[Path], sheets_list: list[str]):
        self._country_dest: Path = country_destination
        self._country_sources: list[Path] = country_sources
        self._sheets_list: list[str] = sheets_list

        writeFile(destination=country_destination, sheet_df_dict=self.createDataDict())

    def getYearTableDict(self, sheet_name: str) -> dict[int, dict]:
        return {int(file_path.name[18:22]): pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl').to_dict()
                for file_path in self._country_sources}

    @calculateTime
    def createDataDict(self) -> dict[str: pd.DataFrame]:
        sheet_df_dict: dict[str: pd.DataFrame] = {}

        for sheet in self._sheets_list:
            year_df_dict: dict[int, dict[str, dict]] = self.getYearTableDict(sheet)
            processed_data: dict[str | int, list] = {}
            table = Patterns(year_df_dict)
            successful: bool = True

            match sheet:
                case 'Table4' | 'Table4.1' | 'Table3':
                    processed_data = table.Table4Digit()

                #case sheet if (sheet[-1].isalpha() and sheet[-1].isupper()):
                case sheet if (sheet[-3] =='4' and sheet[-1].isalpha() and sheet[-1].isupper()):
                    processed_data = table.Table4Alpha()

                case sheet if sheet[6] == '(' and sheet[-1] == ')':
                    #print(f'roman {sheet} not planned yet')
                    processed_data = table.Table4Brackets()

                case 'Table3.A':
                    processed_data = table.Table3Alpha()

                case 'Table3.B(a)':
                    processed_data = table.Table3Beta()

                case 'Table4.Gs1' | 'Table4.Gs2':
                    print(f'new {sheet} not planned yet')

                case _:
                    successful = False
                    print(f'Unexpected sheet name: {sheet}')

            if successful:
                sheet_df_dict[sheet] = pd.DataFrame(data=processed_data)

        return sheet_df_dict
