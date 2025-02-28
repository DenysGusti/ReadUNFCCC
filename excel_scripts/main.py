from settings import *
#from settings_Table3 import *
from data_extraction import TableCreation
from time_series import TimeSeries
from auxiliary_functions import calculateTime
from zip_extract import unzip_files


@calculateTime
def main() -> None:
    if UNZIP_DATA:
        unzip_files(DATA_PATH)

    if EXTRACT_DATA:
        for destination, sources in COUNTRIES_DICT.items():
            TableCreation(country_destination=destination, country_sources=sources, sheets_list=SHEETS_LIST)

    if CREATE_TIME_SERIES:
        TimeSeries(parameters=PARAMETERS, years_list=YEARS_LIST, result_path=RESULT_PATH,
                   countries_names=COUNTRIES_NAMES)


if __name__ == '__main__':
    main()
