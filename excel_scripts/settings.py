from pathlib import Path

### If you want to extract data from the original CRF tables submitted to the UNFCCC set this parameter to TRUE
EXTRACT_DATA: bool = True

# Specify the path where do you keep the downloaded CRF tables (the files for every country should be in a separate folder named as the country ISO3 code is, e.g. aus, aut...)    
DATA_PATH: Path = Path(r'C:\Users\denys\PycharmProjects\ReadUNFCCC\data\2021')

### Specify the CRF tables you want to extract    
SHEETS_LIST: list[str] = ['Table4', 'Table4.1', 'Table4.A', 'Table4.B', 'Table4.C', 'Table4.D', 'Table4.E', 'Table4.F']
# SHEETS_LIST: list[str] = ['Table4']

### Specify a range of years or single years for which you want to extract the data
YEARS: list[int] = list(range(1990, 2020))
# YEARS: list[int] = [1990]

### Specify the folder name where you out the original CRF tables extracted from the archives
COUNTRIES_LIST: list[Path] = [x for x in (DATA_PATH / 'original').iterdir() if x.is_dir()]

### If you want to extract data only for some countries then uncomment the line below and specify the ISO3 codes of the countries (see example in the second line)
# COUNTRIES_LIST: list[Path] = [x for x in COUNTRIES_LIST if x.name[:3] in ['bel', 'fra', 'isl']]

COUNTRIES_DICT: dict[Path, list[Path]] = {
    DATA_PATH / 'extracted' / f"{country.name[:8].replace('-', '_')}.xlsx":
        [x for x in country.glob('**/*.xlsx') if '~$' not in x.name and int(x.name[9:13]) in YEARS]
    for country in COUNTRIES_LIST
}
#
#
#
#
###--------------------------------------------------------------------------------------------------------------------------
### If you want to create a timeseries of one or a few parameters from the extracted data then set CREATE_TIME_SERIES to TRUE 
CREATE_TIME_SERIES: bool = True

### Specify the parameter (user) names and CRF table categories from which the parameters will be taken, starting from user name of the parameter, 
### then following the CRF table name, category, subcategory,... unit to uniquely identify the data (see examples below)
PARAMETERS: dict[str, dict[str, list[str | float]]] = {  # if the field is empty, fill it with float('nan')
    'Deforestation': {
        'Table4.B': ['Forest land converted to', float('nan'), 'ACTIVITY DATA', 'Total area(2)', float('nan'), '(kha)'],
        'Table4.C': ['Forest land converted to', float('nan'), 'ACTIVITY DATA', 'Total area(2)', float('nan'), '(kha)'],
        'Table4.D': ['Forest land converted to', float('nan'), 'ACTIVITY DATA', 'Total area(2)', float('nan'), '(kha)'],
        'Table4.E': ['Forest land converted to', float('nan'), 'ACTIVITY DATA', 'Total area(2)', float('nan'), '(kha)'],
        'Table4.F': ['Forest land converted to', float('nan'), 'ACTIVITY DATA', 'Total area(2)', float('nan'), '(kha)']
    },
    'Net DW (t C per ha)': {  # '/', ':' invalid
        'Table4.A': ['1. Forest land remaining forest land', float('nan'), 'IMPLIED CARBON-STOCK-CHANGE FACTORS',
                     'Net carbon stock change in dead wood per area(4)', '', '(t C/ha)']
    },
    'Net DW (kt C)': {
        'Table4.A': ['1. Forest land remaining forest land', float('nan'),
                     'CHANGES IN CARBON STOCK AND NET CO2 EMISSIONS/REMOVALS FROM SOILS',
                     'Net carbon stock change in dead wood(4)', float('nan'), '(kt C)']
    }
}


### If you want to create the timeseries only for some countries specify the ISO3 codes of the countries (see example on the second line below)    
COUNTRIES_NAMES: list[Path] = [x for x in (DATA_PATH / 'extracted').iterdir() if x.is_file()]
# COUNTRIES_NAMES: list[Path] = [x for x in COUNTRIES_NAMES if x.name[:3] in ['bel', 'fra', 'isl']]

### Specify a range of years or single years for which you want to create the timeseries
YEARS_LIST: list[int] = list(range(1990, 2020))
# YEARS_LIST: list[int] = [1990]

### Specify a name of the file with the timeseries
RESULT_PATH: Path = DATA_PATH / 'structured' / 'UNFCCC_2021_timeseries.xlsx'
