import math
from auxiliary_functions import calculate_time


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

    @calculate_time
    def Table4X(self) -> dict[str | int, list]:
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
        new_data['Rows'] = [v[first_row] for v in list(self._structure.values())[1:]]

        tmp_list = []
        for el in new_data[table_name]:
            tmp_list.append(el)
            tmp_list += ['' for _ in range(len(new_data['Rows']) - 1)]

        units: str = self._structure[list(self._structure.keys())[1]][first_row + 1]
        new_data['Rows'] *= len(new_data[table_name])
        new_data['Units'] = [units] * len(new_data['Rows'])
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


"""        prev_cell: float = -1
        add_flag: bool = False
        for row, cell in self._structure[self._name].items():
            if math.isnan(prev_cell) and type(cell) == str and not add_flag:
                add_flag = True
                data_start_row = row
            else:
                prev_cell = cell if type(cell) == float else -1

            if add_flag:
                new_data[table_name].append(cell)"""
