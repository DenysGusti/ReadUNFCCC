from pathlib import Path

EXTRACT_DATA: bool = True

DATA_PATH: Path = Path(r'C:\Users\denys\PycharmProjects\ReadUNFCCC\data\2021')

SHEETS_LIST: list[str] = ['Table4', 'Table4.1', 'Table4.A', 'Table4.B', 'Table4.C', 'Table4.D', 'Table4.E', 'Table4.F']
# SHEETS_LIST: list[str] = ['Table4']

YEARS: list[int] = list(range(1990, 2020))
# YEARS: list[int] = [1990]

COUNTRIES_LIST: list[Path] = [x for x in (DATA_PATH / 'original').iterdir() if x.is_dir()]
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
#
CREATE_TIME_SERIES: bool = True

PARAMETERS: dict[str, dict[str, list[str | float]]] = {  # if field is empty, fill it with float('nan')
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

COUNTRIES_NAMES: list[Path] = [x for x in (DATA_PATH / 'extracted').iterdir() if x.is_file()]
# COUNTRIES_NAMES: list[Path] = [x for x in COUNTRIES_NAMES if x.name[:3] in ['bel', 'fra', 'isl']]

YEARS_LIST: list[int] = list(range(1990, 2020))
# YEARS_LIST: list[int] = [1990]

RESULT_PATH: Path = DATA_PATH / 'structured' / 'UNFCCC_2021_timeseries.xlsx'
