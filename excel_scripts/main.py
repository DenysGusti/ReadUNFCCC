from file_management import Files
from table_creation import Table
from auxiliary_functions import calculate_time


@calculate_time
def main():
    files = Files(folder_path=r'C:\Users\denys\PycharmProjects\ReadUNFCCC\data\2021')

    # non-default optional settings
    files.countriesDirList = 'aus-2021-crf-15apr21',  # , is needed!!!
    files.sheetsList = 'Table4',  # , is needed!!!
    # files.years = 1990,  # , is needed!!!

    countries_dict = files.createCountriesDict()
    sheets_list = files.sheetsList

    for country_dest, country_sources in countries_dict.items():
        table = Table(country_dest=country_dest, country_sources=country_sources, sheets_list=sheets_list)
        table.createFile()


if __name__ == "__main__":
    main()
