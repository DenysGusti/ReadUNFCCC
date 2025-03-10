from pathlib import Path
from math import nan


'''
Unzip the UNFCCC data into folder 'original'
If the files are already unzipped don't do it again, it takes time!
'''
UNZIP_DATA: bool = False

'''
Specify the path where do you keep the downloaded (zipped or unzipped) CRT tables. 
The unzipped files for every country should be in a separate
folder named as the country ISO3 code is, e.g. aus, aut...)
UNZIP_DATA does it itself if applied.
'''
#DATA_PATH: Path = Path(r'D:\MGusti\CurrentWork\UNFCCC_script\data\2023')
DATA_PATH: Path = Path(r'D:\MGusti\CurrentWork\UNFCCC_script\data\2025')
#DATA_PATH: Path = Path(r'I:\jia\UNFCCC2024')


# Set the working directory
Path(DATA_PATH).mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

# Create folder 'original' if it doesn't exist
folder_name_original = DATA_PATH / 'original'
folder_name_original.mkdir(exist_ok=True)

# Create folder 'extracted' if it doesn't exist
folder_name_extracted = DATA_PATH / 'extracted'
folder_name_extracted.mkdir(exist_ok=True)

'''
If you want to extract data from the original CRT tables submitted to the UNFCCC set this parameter to TRUE
'''
EXTRACT_DATA: bool = True


'''
Specify the CRT tables you want to extract
'''
SHEETS_LIST: list[str] = ['Table3','Table3.A', 'Table3.B(a)','Table4', 'Table4.1', 'Table4.A', 'Table4.B', 'Table4.C', 'Table4.D', 'Table4.E', 'Table4.F','Table4(II)']
#SHEETS_LIST: list[str] = ['Table4', 'Table4.1']
#SHEETS_LIST: list[str] = ['Table4.A', 'Table4.B', 'Table4.C', 'Table4.D', 'Table4.E', 'Table4.F']
#SHEETS_LIST: list[str] = ['Table4(II)']
#SHEETS_LIST: list[str] = ['Table3']
#SHEETS_LIST: list[str] = ['Table3.A']
#SHEETS_LIST: list[str] = ['Table3.B(a)']
'''
Specify a range of years or single years for which you want to extract the data
'''
YEARS: list[int] = list(range(1990, 2024))
#YEARS: list[int] = [1990, 1991, 1992]
#YEARS: list[int] = [2013,2017]
'''
Specify the folder name where you out the original CRF tables extracted from the archives
'''
COUNTRIES_LIST: list[Path] = [x for x in (DATA_PATH / 'original').iterdir() if x.is_dir()]
'''
If you want to extract data only for some countries then uncomment the line below and specify the ISO3 codes of the
countries (see example in the second line)
'''
# COUNTRIES_LIST: list[Path] = [x for x in COUNTRIES_LIST if x.name[:3].lower() in ['svk' or 'svn' or 'swe' or 'tur' or 'ukr' or 'usa']]
#COUNTRIES_LIST: list[Path] = [x for x in COUNTRIES_LIST if x.name[:3].lower() in ['deu']]
#COUNTRIES_LIST: list[Path] = [x for x in COUNTRIES_LIST if x.name[:3].lower() in ['pol','rou']]

COUNTRIES_DICT: dict[Path, list[Path]] = {
    DATA_PATH / 'extracted' / f"{country.name[:8].replace('-', '_')}.xlsx":
        [x for x in country.glob('**/*.xlsx') if '~$' not in x.name and int(x.name[18:22]) in YEARS]
    for country in COUNTRIES_LIST
}

# ---------------------------------------------------------------------------------------------------------------------

'''
If you want to create a timeseries of one or a few parameters from the extracted data then set CREATE_TIME_SERIES to
TRUE
'''
CREATE_TIME_SERIES: bool = True


# Create folder 'extracted' if it doesn't exist
folder_name_structured = DATA_PATH / 'structured'
folder_name_structured.mkdir(exist_ok=True)

'''
Specify the parameter (user) names (e.g. Deforestation) and CRF table categories from which the parameters will be 
taken, starting from user name of the parameter, then following the CRF table name, category, subcategory,... 
unit to uniquely identify the data. If one of the subcategory in the CRF table is empty specify "nan" 
(see examples below).
'''

PARAMETERS: dict[str, dict[str, list[str | float]]] = {  # if the field is empty, fill it with nan

    'Total_LULUCF_emissions_kt': { #(1) For the purposes of reporting, the signs for removals are always negative (–) for removals and positive (+) for emissions.
        'Table4': ['Total LULUCF', 'Total GHG', '(kt)']
    },

    'Total_Forest_land_emissions_kt': { #(1) For the purposes of reporting, the signs for removals are always negative (–) for removals and positive (+) for emissions.
        'Table4': ['A. Forest land', 'Total GHG', '(kt)']
    },
    'Total_FF_LFL_emissions_kt': { #(1) For the purposes of reporting, the signs for removals are always negative (–) for removals and positive (+) for emissions.
        'Table4': ['A.1. Forest land remaining forest land', 'Total GHG', '(kt)']
    },
    'Total_Forest_land_area': {
        'Table4.A': ['A. Total forest land', nan, 'ACTIVITY DATA', 'Total area', nan, '(kha)']
    },

     'Forest_land_area': {
         'Table4.A': ['1. Forest land remaining forest land', nan, 'ACTIVITY DATA', 'Total area', nan, '(kha)']
     }
    ,

      'Afforestation_area_20y': {
          'Table4.A': ['2. Land converted to forest land', nan, 'ACTIVITY DATA', 'Total area', nan, '(kha)']
      },
      'Afforestation_area_annual': {
          'Table4.1': [['Cropland', 'Forest land ', '(kha)'],
           ['Grassland ', 'Forest land ', '(kha)'],
           ['Wetlands ', 'Forest land ', '(kha)'],
           ['Settlements', 'Forest land ', '(kha)'],
           ['Other land', 'Forest land ', '(kha)']]
      },
      'Deforestation_area_20y': {
          'Table4.B': ['Forest land converted to', nan, 'ACTIVITY DATA', 'Total area', nan, '(kha)'],
          'Table4.C': ['Forest land converted to', nan, 'ACTIVITY DATA', 'Total area', nan, '(kha)'],
          'Table4.D': ['Forest land converted to', nan, 'ACTIVITY DATA', 'Total area', nan, '(kha)'],
          'Table4.E': ['Forest land converted to', nan, 'ACTIVITY DATA', 'Total area', nan, '(kha)'],
          'Table4.F': ['Forest land converted to', nan, 'ACTIVITY DATA', 'Total area', nan, '(kha)']
      },
      'Deforestation_area_annual': {
          'Table4.1': [['Forest land ', 'Cropland', '(kha)'],
          ['Forest land ', 'Grassland ', '(kha)'],
          ['Forest land ', 'Wetlands ', '(kha)'],
          ['Forest land ', 'Settlements', '(kha)'],
          ['Forest land ', 'Other land','(kha)']]
      }

     ,
     'Net Bm (t C per ha)_FLFL': {  # '/', ':' invalid
         'Table4.A': ['1. Forest land remaining forest land', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Carbon stock change in living biomass per area', 'Net change', '(t C/ha)']
     },
     'Net Bm (kt C)_FLFL': {
         'Table4.A': ['1. Forest land remaining forest land', nan,'CARBON STOCK CHANGES',
                        'Carbon stock change in living biomass', 'Net change', '(kt C)']
     },

     'Net Bm (t C per ha)_LFL': {  # '/', ':' invalid
         'Table4.A': ['2. Land converted to forest land', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Carbon stock change in living biomass per area', 'Net change', '(t C/ha)']
     },
     'Net Bm (kt C)_LFL': {
         'Table4.A': ['2. Land converted to forest land', nan,
                      'CARBON STOCK CHANGES',
                      'Carbon stock change in living biomass', 'Net change', '(kt C)']
     },

     'Net BM_(t C per ha)_FL-L': { # Not area-weighted ! Just an indication!
         'Table4.B': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS', 'Carbon stock change in living biomass per area', 'Net change', '(t C/ha)'],
         'Table4.C': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS', 'Carbon stock change in living biomass per area', 'Net change', '(t C/ha)'],
         'Table4.D': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS', 'Carbon stock change in living biomass per area', 'Net change', '(t C/ha)'],
         'Table4.E': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS', 'Carbon stock change in living biomass per area', 'Net change', '(t C/ha)'],
         'Table4.F': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS', 'Carbon stock change in living biomass per area', 'Net change', '(t C/ha)']
     },
     'Net BM_(kt C)_FL-L': {
         'Table4.B': ['Forest land converted to', nan, 'CARBON STOCK CHANGES',
                      'Carbon stock change in living biomass', 'Net change', '(kt C)'],
         'Table4.C': ['Forest land converted to', nan, 'CARBON STOCK CHANGES',
                      'Carbon stock change in living biomass', 'Net change', '(kt C)'],
         'Table4.D': ['Forest land converted to', nan, 'CARBON STOCK CHANGES',
                      'Carbon stock change in living biomass', 'Net change', '(kt C)'],
         'Table4.E': ['Forest land converted to', nan, 'CARBON STOCK CHANGES',
                      'Carbon stock change in living biomass', 'Net change', '(kt C)'],
         'Table4.F': ['Forest land converted to', nan, 'CARBON STOCK CHANGES',
                      'Carbon stock change in living biomass', 'Net change', '(kt C)']
     },

     'Net DW (t C per ha)_FLFL': {  # '/', ':' invalid
         'Table4.A': ['1. Forest land remaining forest land', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in dead wood per area', nan, '(t C/ha)']
     },
     'Net DW (kt C)_FLFL': {
         'Table4.A': ['1. Forest land remaining forest land', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in dead wood', nan, '(kt C)']
     },

     'Net DW (t C per ha)_LFL': {  # '/', ':' invalid
         'Table4.A': ['2. Land converted to forest land', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in dead wood per area', nan, '(t C/ha)']
     },
     'Net DW (kt C)_LFL': {
         'Table4.A': ['2. Land converted to forest land', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in dead wood', nan, '(kt C)']
     },

     'Net DW_(t C per ha)_FL-L': { # Not area-weighted ! Just an indication!
         'Table4.B': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in dead organic matter per area', 'Net change', '(t C/ha)'],
         'Table4.C': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in dead organic matter per area', 'Net change', '(t C/ha)'],
         'Table4.D': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in dead organic matter per area', 'Net change', '(t C/ha)'],
         'Table4.E': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in dead organic matter per area', 'Net change', '(t C/ha)'],
         'Table4.F': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in dead organic matter per area', 'Net change', '(t C/ha)']
     },
     'Net DW_(kt C)_FL-L': {
         'Table4.B': ['Forest land converted to', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in dead organic matter', nan, '(kt C)'],
         'Table4.C': ['Forest land converted to', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in dead organic matter', nan, '(kt C)'],
         'Table4.D': ['Forest land converted to', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in dead organic matter', nan, '(kt C)'],
         'Table4.E': ['Forest land converted to', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in dead organic matter', nan, '(kt C)'],
         'Table4.F': ['Forest land converted to', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in dead organic matter', nan, '(kt C)']
     },

     'Net Litter (t C per ha)_FLFL': {  # '/', ':' invalid
         'Table4.A': ['1. Forest land remaining forest land', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in litter  per area', nan, '(t C/ha)']
     },
     'Net Litter (kt C)_FLFL': {
         'Table4.A': ['1. Forest land remaining forest land', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in litter', nan, '(kt C)']
     },

     'Net Litter (t C per ha)_LFL': {  # '/', ':' invalid
         'Table4.A': ['2. Land converted to forest land', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in litter  per area', nan, '(t C/ha)']
     },
     'Net Litter (kt C)_LFL': {
         'Table4.A': ['2. Land converted to forest land', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in litter', nan, '(kt C)']
     },

     'Soil_mineral (t C per ha)_FLFL': {  # '/', ':' invalid
         'Table4.A': ['1. Forest land remaining forest land', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in soils per area', 'Mineral soils', '(t C/ha)']
     },
     'Soil_organic (t C per ha)_FLFL': {  # '/', ':' invalid
         'Table4.A': ['1. Forest land remaining forest land', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in soils per area', 'Organic soils', '(t C/ha)']
     },

     'Soil (kt C)_mineral_FLFL': {
         'Table4.A': ['1. Forest land remaining forest land', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in soils', 'Mineral soils', '(kt C)']
     },
     'Soil (kt C)_organic_FLFL': {
         'Table4.A': ['1. Forest land remaining forest land', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in soils', 'Organic soils', '(kt C)']
     },
     'Soil_mineral (t C per ha)_LFL': {  # '/', ':' invalid
         'Table4.A': ['2. Land converted to forest land', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in soils per area', 'Mineral soils', '(t C/ha)']
     },
     'Soil_organic (t C per ha)_LFL': {  # '/', ':' invalid
         'Table4.A': ['2. Land converted to forest land', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in soils per area', 'Organic soils', '(t C/ha)']
     },
     'Soil_mineral (kt C)_LFL': {
         'Table4.A': ['2. Land converted to forest land', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in soils','Mineral soils' , '(kt C)']
     },
     'Soil_organic (kt C)_LFL': {
         'Table4.A': ['2. Land converted to forest land', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in soils', 'Organic soils', '(kt C)']
     },
     'Soil_mineral(t C per ha)_FL-L': { # Not area-weighted ! Just an indication!
         'Table4.B': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in soils per area', 'Mineral soils', '(t C/ha)'],
         'Table4.C': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in soils per area', 'Mineral soils', '(t C/ha)'],
         'Table4.D': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in soils per area', 'Mineral soils', '(t C/ha)'],
         'Table4.E': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in soils per area', 'Mineral soils', '(t C/ha)'],
         'Table4.F': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in soils per area', 'Mineral soils', '(t C/ha)']
     },
     'Soil_organic(t C per ha)_FL-L': { # Not area-weighted ! Just an indication!
         'Table4.B': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in soils per area', 'Organic soils', '(t C/ha)'],
         'Table4.C': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in soils per area', 'Organic soils', '(t C/ha)'],
         'Table4.D': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in soils per area', 'Organic soils', '(t C/ha)'],
         'Table4.E': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in soils per area', 'Organic soils', '(t C/ha)'],
         'Table4.F': ['Forest land converted to', nan, 'IMPLIED CARBON STOCK CHANGE FACTORS',
                      'Net carbon stock change in soils per area', 'Organic soils', '(t C/ha)']
     },
     'Soil_organic(kt C)_FL-L': {
         'Table4.B': ['Forest land converted to', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in soils', 'Organic soils', '(kt C)'],
         'Table4.C': ['Forest land converted to', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in soils', 'Organic soils', '(kt C)'],
         'Table4.D': ['Forest land converted to', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in soils', 'Organic soils', '(kt C)'],
         'Table4.E': ['Forest land converted to', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in soils', 'Organic soils', '(kt C)'],
         'Table4.F': ['Forest land converted to', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in soils', 'Organic soils', '(kt C)']
     },
     'Soil_mineral(kt C)_FL-L': {
         'Table4.B': ['Forest land converted to', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in soils', 'Mineral soils', '(kt C)'],
         'Table4.C': ['Forest land converted to', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in soils', 'Mineral soils', '(kt C)'],
         'Table4.D': ['Forest land converted to', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in soils', 'Mineral soils', '(kt C)'],
         'Table4.E': ['Forest land converted to', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in soils', 'Mineral soils', '(kt C)'],
         'Table4.F': ['Forest land converted to', nan,
                      'CARBON STOCK CHANGES',
                      'Net carbon stock change in soils', 'Mineral soils', '(kt C)']
     },

     'organicSoils_allLand_CO2': {
         'Table4(II)': ['Total for all land use categories', nan, 'EMISSIONS', 'CO2', '(kt)']
     },
     'organicSoils_allLand_N2O': {
     'Table4(II)': ['Total for all land use categories', nan, 'EMISSIONS', 'N2O', '(kt)']
     },
     'organicSoils_allLand_CH4': {
     'Table4(II)': ['Total for all land use categories', nan, 'EMISSIONS', 'CH4', '(kt)']
     },
     'organicSoils_forest_CO2': {
         'Table4(II)': ['A. Forest land', nan, 'EMISSIONS', 'CO2', '(kt)']
     },
     'organicSoils_forest_N2O': {
         'Table4(II)': ['A. Forest land', nan, 'EMISSIONS', 'N2O', '(kt)']
     },
     'organicSoils_forest_CH4': {
         'Table4(II)': ['A. Forest land', nan, 'EMISSIONS', 'CH4', '(kt)']
     }

}


'''
If you want to create the timeseries only for some countries specify the ISO3 codes of the countries (see example on the
second line below)
'''
COUNTRIES_NAMES: list[Path] = [x for x in (DATA_PATH / 'extracted').iterdir() if x.is_file()]

#COUNTRIES_NAMES: list[Path] = [x for x in COUNTRIES_NAMES if (x.name[:3].lower() in ['deu'] or x.name[:3].lower() in ['aut']) and (not 'Copy' in x.name)]
#COUNTRIES_NAMES: list[Path] = [x for x in COUNTRIES_NAMES if x.name[:3].lower() in ['pol']]

COUNTRIES_NAMES: list[Path] = [x for x in COUNTRIES_NAMES if (not 'Copy' in x.name)]
'''
Specify a range of years or single years for which you want to create the timeseries
'''
YEARS_LIST: list[int] = list(range(1990, 2024))
#YEARS_LIST: list[int] = [2013,2017]

'''
Specify a name of the file with the timeseries
'''
RESULT_PATH: Path = DATA_PATH / 'structured' / 'UNFCCC_2025_LULUCF_timeseries_preliminary_updated.xlsx'
#RESULT_PATH: Path = DATA_PATH / 'structured' / 'UNFCCC_2025_LULUCF_timeseries_preliminary_POL.xlsx'
