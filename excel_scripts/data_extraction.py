import pandas as pd
from pathlib import Path
from auxiliary_functions import calculateTime, writeFile, clearStr


class Patterns:
    """
    Different processing for every xlsx sheet type (i.e. CRF table type)
    """

    def __init__(self, year_df_dict: dict[int, dict[str, dict]]):
        self._year_df_dict: dict[int, dict[str, dict]] = year_df_dict
        self._name, self._last_row, self._structure = self.getInfo()

    def getInfo(self) -> tuple[str, int, dict[str, dict]]:
        first_year: int = min(self._year_df_dict.keys())
        old_structure: dict[str, dict] = self._year_df_dict[first_year]
        name: str = list(old_structure.keys())[0]

        # cutting the rows over the table
        min_row: int = min(row for row, cell in old_structure[name].items()
                           if row > 0 and type(old_structure[name][row - 1]) == float and type(cell) == str)
        max_row: int = min(row - 2 for row, cell in old_structure[name].items() if str(cell)[:3] == '(1)')
        # in Gs2 there is additional info after (1)...!

        new_structure: dict[str, dict] = {k: {row: data for row, data in v.items() if min_row <= row <= max_row}
                                          for k, v in old_structure.items()}

        return name, max_row, new_structure

    def Table4Digit(self) -> dict[str | int, list]:
        new_data: dict[str | int, list] = {}

        orig_row_names = list(self._structure[self._name].values())
        match self._name:
            case 'TABLE 4 SECTORAL REPORT FOR LAND USE, LAND-USE CHANGE AND FORESTRY':
                table_name: str = f'{self._name}     {orig_row_names[0]}'

            case 'Table 4.1  LAND TRANSITION MATRIX':
                table_name: str = f'{self._name}     {orig_row_names[1]} {orig_row_names[0]}'

            case _:
                table_name = ''
                print('Unexpected name')

        new_data[table_name] = [clearStr(x) for x in orig_row_names[2:]]
        first_row: int = list(self._structure[self._name].keys())[0]
        new_data['Column'] = [clearStr(v[first_row]) for v in list(self._structure.values())[1:]]
        old_len = len(new_data[table_name])
        new_data[table_name] = [el for el in new_data[table_name] for _ in new_data['Column']]

        units: str = self._structure[list(self._structure.keys())[1]][first_row + 1]
        new_data['Column'] *= old_len
        new_data['Units'] = [units] * len(new_data['Column'])

        for year, data in self._year_df_dict.items():  # data start from 5th row
            new_data[year] = [cells[i] for i in range(5, self._last_row + 1) for cells in list(data.values())[1:]]

        return new_data

    def Table4Alpha(self) -> dict[str | int, list]:
        new_data: dict[str | int, list] = {}

        orig_row_names = list(self._structure[self._name].values())
        table_name: str = f'{self._name}     {orig_row_names[0]} {orig_row_names[1]}'
        new_data[table_name] = [clearStr(x) if type(x) == str else x for x in orig_row_names[5:]]

        sub_name: str = list(self._structure.keys())[1]
        orig_sub_names = list(self._structure[sub_name].values())
        sub_table_name: str = f'Subcategory     {orig_sub_names[1]}'
        new_data[sub_table_name] = [clearStr(x) if type(x) == str else x for x in orig_sub_names[5:]]

        first_row: int = list(self._structure[self._name].keys())[0]

        orig_col_names = list(self._structure.values())[2:]
        for i in range(first_row, first_row + 4):
            new_data[f'Column_{min(i - first_row, 2)}'] = [clearStr(v[i])
                                                           if type(v[i]) == str else v[i] for v in orig_col_names]

        new_data['Units']: list[str] = [''] * 3
        for i in range(3):
            new_data['Column_1'][i], new_data['Units'][i] = new_data['Column_1'][i][:-5], new_data['Column_1'][i][-5:]
        new_data['Units'] += [x[first_row + 4] for x in orig_col_names[3:]]

        for column in ['Units', 'Column_0', 'Column_1']:
            for i, el in enumerate(new_data[column]):
                if type(el) == float and (
                        column != 'Column_1' or column == 'Column_1' and type(new_data['Column_2'][i]) == str):
                    new_data[column][i] = new_data[column][i - 1]

        old_len = len(new_data[table_name])
        new_data[table_name] = [el for el in new_data[table_name] for _ in new_data['Units']]
        new_data[sub_table_name] = [el for el in new_data[sub_table_name] for _ in new_data['Units']]

        for i in range(3):
            new_data[f'Column_{i}'] *= old_len
        new_data['Units'] *= old_len

        for year, data in self._year_df_dict.items():  # data start from 8th row
            new_data[year] = [cells[i] for i in range(8, self._last_row + 1) for cells in list(data.values())[2:]]

        return new_data


class TableCreation:
    """
    making xlsx file
    """

    def __init__(self, *, country_destination: Path, country_sources: list[Path], sheets_list: list[str]):
        self._country_dest: Path = country_destination
        self._country_sources: list[Path] = country_sources
        self._sheets_list: list[str] = sheets_list

        writeFile(destination=country_destination, sheet_df_dict=self.createDataDict())

    def getYearTableDict(self, sheet_name: str) -> dict[int, dict]:
        return {int(file_path.name[9:13]): pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl').to_dict()
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
                case 'Table4' | 'Table4.1':
                    processed_data = table.Table4Digit()

                case sheet if sheet[-1].isalpha() and sheet[-1].isupper():
                    processed_data = table.Table4Alpha()

                case sheet if sheet[6] == '(' and sheet[-1] == ')':
                    print(f'roman {sheet} not planned yet')

                case 'Table4.Gs1' | 'Table4.Gs2':
                    print(f'new {sheet} not planned yet')

                case _:
                    successful = False
                    print(f'Unexpected sheet name: {sheet}')

            if successful:
                sheet_df_dict[sheet] = pd.DataFrame(data=processed_data)

        return sheet_df_dict
