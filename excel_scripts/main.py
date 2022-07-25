from table_creation import TableCreation


def main():
    excel = TableCreation(folder_path=r'C:\Users\denys\PycharmProjects\ReadUNFCCC\data\2021')

    # non-default optional settings
    excel.countriesDirList = 'aus-2021-crf-15apr21',  # , is needed!!!
    excel.sheetsList = 'Table4',  # , is needed!!!
    excel.years = 1990,  # , is needed!!!

    excel.makeTables()


if __name__ == "__main__":
    main()
