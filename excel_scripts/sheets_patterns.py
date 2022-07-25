import math


class Patterns:
    """
    Different processing for every xlsx sheet type
    """

    def __init__(self, year_df_dict: dict[int, dict[str, dict]]):
        self._year_df_dict: dict[int, dict[str, dict]] = year_df_dict
        self._structure, self._name, self._last_row = self.getInfo()

    def getInfo(self) -> tuple[dict[str, dict], str, int]:
        first_year: int = min(self._year_df_dict.keys())
        old_structure: dict[str, dict] = self._year_df_dict[first_year]
        name: str = list(old_structure.keys())[0]

        # cutting
        min_row, max_row = 1, 10000
        prev_cell: float = -1
        for row, cell in old_structure[name].items():
            if math.isnan(prev_cell) and type(cell) == str and min_row == 1:
                min_row = row
            else:
                prev_cell = cell if type(cell) == float else -1

            if str(cell)[:3] == '(1)':  # Gs2 additional info!
                max_row = row - 2
                break

        new_structure: dict[str, dict] = dict()
        for key, value in old_structure.items():
            tmp_dict = dict()
            for row, data in value.items():
                if min_row <= row <= max_row:
                    tmp_dict[row] = data
            new_structure[key] = tmp_dict

        return new_structure, name, max_row

    def Table4Digit(self) -> dict[str | int, list]:
        new_data: dict[str | int, list] = dict()

        match self._name:
            case 'TABLE 4 SECTORAL REPORT FOR LAND USE, LAND-USE CHANGE AND FORESTRY':
                table_name: str = f'{self._name}     {list(self._structure[self._name].values())[0]}'

            case 'Table 4.1  LAND TRANSITION MATRIX':
                table_name: str = f'{self._name}     {list(self._structure[self._name].values())[1]} ' \
                                  f'{list(self._structure[self._name].values())[0]}'

            case _:
                table_name = ''
                print("Unexpected name")

        new_data[table_name] = list(self._structure[self._name].values())[2:]
        first_row: int = list(self._structure[self._name].keys())[0]
        new_data['Columns'] = [v[first_row] for v in list(self._structure.values())[1:]]

        tmp_list = []
        for el in new_data[table_name]:
            tmp_list.append(el)
            tmp_list += ['' for _ in range(len(new_data['Columns']) - 1)]

        units: str = self._structure[list(self._structure.keys())[1]][first_row + 1]
        new_data['Columns'] *= len(new_data[table_name])
        new_data['Units'] = [units] * len(new_data['Columns'])
        new_data[table_name] = tmp_list

        data_start_row: int = 5
        for year, data in self._year_df_dict.items():
            new_data[year] = []

            for i in range(data_start_row, self._last_row + 1):
                for cells in list(data.values())[1:]:
                    if (type(cells[i]) == float and not math.isnan(cells[i])) or type(cells[i]) == str:
                        new_data[year].append(cells[i])
                    else:
                        new_data[year].append('NA')

        return new_data

    def Table4Alpha(self) -> dict[str | int, list]:
        new_data: dict[str | int, list] = dict()

        table_name: str = f'{self._name}     {list(self._structure[self._name].values())[0]}     ' \
                          f'{list(self._structure[self._name].values())[1]}'
        new_data[table_name] = list(self._structure[self._name].values())[5:]

        sub_name: str = list(self._structure.keys())[1]
        sub_table_name: str = f'Subcategory     {list(self._structure[sub_name].values())[1]}'
        new_data[sub_table_name] = list(self._structure[sub_name].values())[5:]

        first_row: int = list(self._structure[self._name].keys())[0]

        for i in range(first_row, first_row + 4):
            new_data[f'Columns_{min(i - first_row, 2)}'] = [v[i] if type(v[i]) == str else ''
                                                            for v in list(self._structure.values())[2:]]

        new_data['Units'] = [v[first_row + 4] if type(v[first_row + 4]) == str else ''
                             for v in list(self._structure.values())[2:]]
        for i in range(3):
            new_data['Columns_1'][i], new_data['Units'][i] = new_data['Columns_1'][i].split('\n')

        prev_el = ''
        tmp_list = []
        for el in new_data['Units']:
            if el == '':
                el = prev_el
            prev_el = el
            tmp_list.append(el)
        new_data['Units'] = tmp_list

        tmp_list0, tmp_list1 = [], []
        for el in new_data[table_name]:
            tmp_list0.append(el)
            tmp_list0 += ['' for _ in range(len(new_data['Columns_1']) - 1)]
        for el in new_data[sub_table_name]:
            tmp_list1.append(el)
            tmp_list1 += ['' for _ in range(len(new_data['Columns_1']) - 1)]

        for i in range(3):
            new_data[f'Columns_{i}'] *= len(new_data[table_name])

        new_data['Units'] *= len(new_data[table_name])
        new_data[table_name], new_data[sub_table_name] = tmp_list0, tmp_list1

        data_start_row: int = 8
        for year, data in self._year_df_dict.items():
            new_data[year] = []

            for i in range(data_start_row, self._last_row + 1):
                for cells in list(data.values())[2:]:
                    if (type(cells[i]) == float and not math.isnan(cells[i])) or type(cells[i]) == str:
                        new_data[year].append(cells[i])
                    else:
                        new_data[year].append('NA')

        return new_data
