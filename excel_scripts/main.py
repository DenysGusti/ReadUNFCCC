from file_management import Files
from table_creation import Table
from auxiliary_functions import calculate_time
from parameter_structuration import Structuration


@calculate_time
def main():
    files = Files(folder_path=r'C:\Users\denys\PycharmProjects\ReadUNFCCC\data\2021')

    # non-default optional settings
    # files.countriesDirList = 'aut-2021-crf-15apr21',  # , is needed!!!
    # files.sheetsList = 'Table4.A',  # , is needed!!!
    # files.years = 1990,  # , is needed!!!

    countries_dict = files.createCountriesDict()
    sheets_list = files.sheetsList

    for country_dest, country_sources in countries_dict.items():
        county_table = Table(country_dest=country_dest, country_sources=country_sources, sheets_list=sheets_list)
        county_table.writeFile()

    structured_data_table = Structuration(folder_path=r'C:\Users\denys\PycharmProjects\ReadUNFCCC\data\2021')

    # structured_data_table.parameters = {
    #     'Deforestation': {  # in not ==
    #         'Table4.B': ['Forest land converted to', '', 'ACTIVITY DATA', 'Total area(2)', '', '(kha)'],
    #         'Table4.C': ['Forest land converted to', '', 'ACTIVITY DATA', 'Total area(2)', '', '(kha)'],
    #         'Table4.D': ['Forest land converted to', '', 'ACTIVITY DATA', 'Total area(2)', '', '(kha)'],
    #         'Table4.E': ['Forest land converted to', '', 'ACTIVITY DATA', 'Total area(2)', '', '(kha)'],
    #         'Table4.F': ['Forest land converted to', '', 'ACTIVITY DATA', 'Total area(2)', '', '(kha)']
    #     }
    # }
    # structured_data_table.countriesNames = 'aus_2021', 'aut_2021', 'bel_2021'  # , is needed!!!
    result_dict = structured_data_table.makeCountriesData()
    structured_data_table.writeFile(result_dict)


if __name__ == "__main__":
    main()
