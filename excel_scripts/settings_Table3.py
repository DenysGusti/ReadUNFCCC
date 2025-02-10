from pathlib import Path
from math import nan

'''
If you want to extract data from the original CRF tables submitted to the UNFCCC set this parameter to TRUE
'''
EXTRACT_DATA: bool = True

'''
Specify the path where do you keep the downloaded CRF tables (the files for every country should be in a separate
folder named as the country ISO3 code is, e.g. aus, aut...)
'''
DATA_PATH: Path = Path(r'D:\MGusti\CurrentWork\UNFCCC_script\data\2023')

'''
Specify the CRF tables you want to extract
'''
#SHEETS_LIST: list[str] = ['Table3s1', 'Table3.As1', 'Table3.B(a)s1', 'Table3.B(b)']
#SHEETS_LIST: list[str] = ['Table3s1']
#SHEETS_LIST: list[str] = ['Table3.As1']
SHEETS_LIST: list[str] = ['Table3.B(a)s1']
#SHEETS_LIST: list[str] = ['Table4']
#SHEETS_LIST: list[str] = ['Table4.A']

'''
Specify a range of years or single years for which you want to extract the data
'''
YEARS: list[int] = list(range(1990, 2022))
#YEARS: list[int] = [1990, 1991, 1992]

'''
Specify the folder name where you out the original CRF tables extracted from the archives
'''
COUNTRIES_LIST: list[Path] = [x for x in (DATA_PATH / 'original').iterdir() if x.is_dir()]
'''
If you want to extract data only for some countries then uncomment the line below and specify the ISO3 codes of the
countries (see example in the second line)
'''
#COUNTRIES_LIST: list[Path] = [x for x in COUNTRIES_LIST if x.name[:3] in ['svk' or 'svn' or 'swe' or 'tur' or 'ukr' or 'usa']]
#COUNTRIES_LIST: list[Path] = [x for x in COUNTRIES_LIST if x.name[:3] in ['aut']]

COUNTRIES_DICT: dict[Path, list[Path]] = {
    DATA_PATH / 'extracted_Table3' / f"{country.name[:8].replace('-', '_')}.xlsx":
        [x for x in country.glob('**/*.xlsx') if '~$' not in x.name and int(x.name[9:13]) in YEARS]
    for country in COUNTRIES_LIST
}

# ---------------------------------------------------------------------------------------------------------------------

'''
If you want to create a timeseries of one or a few parameters from the extracted data then set CREATE_TIME_SERIES to
TRUE
'''
CREATE_TIME_SERIES: bool = False

'''
Specify the parameter (user) names (e.g. Deforestation) and CRF table categories from which the parameters will be 
taken, starting from user name of the parameter, then following the CRF table name, category, subcategory,... 
unit to uniquely identify the data. If one of the subcategory in the CRF table is empty specify "nan" 
(see examples below).
'''

PARAMETERS: dict[str, dict[str, list[str | float]]] = {  # if the field is empty, fill it with nan
    'Dairy cattle': {
        'Table3.As1': ['Dairy cattle', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size', '(1000s)']
    },

     'Non-dairy cattle': {
         'Table3.As1': ['Non-dairy cattle', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size', '(1000s)']
     },

      'Sheep': {
          'Table3.As1': ['Sheep', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size', '(1000s)']
      },
      
      
      'Swine': {
          'Table3.As1': ['Swine', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size', '(1000s)']
      },
      
      
      
      'Deer': {
          'Table3.As1': ['Deer', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size', '(1000s)']
      },
      
      
      
      'Goats': {
          'Table3.As1': ['Goats', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size', '(1000s)']
      },
      
      
      'Horses': {
          'Table3.As1': ['Horses', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size', '(1000s)']
      },
      
      
      'Poultry': {
          'Table3.As1': ['Poultry', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size', '(1000s)']
      },
      
      
      'Dairy cattle EF': {
          'Table3.As1': ['Dairy cattle', 'EMISSIONS', 'CH4', '(kt)']
      },

       'Non-dairy cattle EF': {
           'Table3.As1': ['Non-dairy cattle', 'EMISSIONS', 'CH4', '(kt)']
       },

        'Sheep EF': {
            'Table3.As1': ['Sheep', 'EMISSIONS', 'CH4', '(kt)']
        },
        
        
        'Swine EF': {
            'Table3.As1': ['Swine', 'EMISSIONS', 'CH4', '(kt)']
        },
        
        
        
        'Deer EF': {
            'Table3.As1': ['Deer', 'EMISSIONS', 'CH4', '(kt)']
        },
        
        
        
        'Goats EF': {
            'Table3.As1': ['Goats', 'EMISSIONS', 'CH4', '(kt)']
        },
        
        
        'Horses EF': {
            'Table3.As1': ['Horses', 'EMISSIONS', 'CH4', '(kt)']
        },
        
        
        'Poultry EF': {
            'Table3.As1': ['Poultry', 'EMISSIONS', 'CH4', '(kt)']
        },
      
    'Dairy cattle MM': {
        'Table3.B(a)s1': ['Dairy cattle', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size',  nan, '(1000s)']
    },

     'Non-dairy cattle MM': {
         'Table3.B(a)s1': ['Non-dairy cattle', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size', nan, '(1000s)']
     },

      'Sheep MM': {
          'Table3.B(a)s1': ['Sheep', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size', nan, '(1000s)']
      },
      
      
      'Swine MM': {
          'Table3.B(a)s1': ['Swine', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size',  nan,'(1000s)']
      },
      
      
      
      'Deer MM': {
          'Table3.B(a)s1': ['Deer', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size',  nan,'(1000s)']
      },
      
      
      
      'Goats MM': {
          'Table3.B(a)s1': ['Goats', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size',  nan,'(1000s)']
      },
      
      
      'Horses MM': {
          'Table3.B(a)s1': ['Horses', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size',  nan,'(1000s)']
      },
      
      
      'Poultry MM': {
          'Table3.B(a)s1': ['Poultry', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size',  nan,'(1000s)']
      },
      
      
      'Dairy cattle CH4 MM': {
          'Table3.B(a)s1': ['Dairy cattle', 'EMISSIONS',  nan, 'CH4', '(kt)']
      },

       'Non-dairy cattle CH4 MM': {
           'Table3.B(a)s1': ['Non-dairy cattle', 'EMISSIONS',  nan,'CH4', '(kt)']
       },

        'Sheep CH4 MM': {
            'Table3.B(a)s1': ['Sheep', 'EMISSIONS', 'CH4',  nan, '(kt)']
        },
        
        
        'Swine CH4 MM': {
            'Table3.B(a)s1': ['Swine', 'EMISSIONS', 'CH4', nan, '(kt)']
        },
        
        
        
        'Deer CH4 MM': {
            'Table3.B(a)s1': ['Deer', 'EMISSIONS', 'CH4',  nan,'(kt)']
        },
        
        
        
        'Goats CH4 MM': {
            'Table3.B(a)s1': ['Goats', 'EMISSIONS', 'CH4', nan, '(kt)']
        },
        
        
        'Horses CH4 MM': {
            'Table3.B(a)s1': ['Horses', 'EMISSIONS', 'CH4', nan, '(kt)']
        },
        
        
        'Poultry CH4 MM': {
            'Table3.B(a)s1': ['Poultry', 'EMISSIONS', 'CH4',  nan,'(kt)']
        },
        
        
        'Dairy cattle N2O': {
            'Table3.B(b)': ['Dairy cattle', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size',  nan, '(1000s)', nan]
        },

         'Non-dairy cattle N2O': {
             'Table3.B(b)': ['Non-dairy cattle', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size',  nan,'(1000s)', nan]
         },

          'Sheep N2O': {
              'Table3.B(b)': ['Sheep', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size', nan, '(1000s)', nan]
          },
          
          
          'Swine N2O': {
              'Table3.B(b)': ['Swine', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size',  nan,'(1000s)', nan]
          },
          
          
          
          'Deer N2O': {
              'Table3.B(b)': ['Deer', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size',  nan,'(1000s)', nan]
          },
          
          
          
          'Goats N2O': {
              'Table3.B(b)': ['Goats', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size',  nan,'(1000s)', nan]
          },
          
          
          'Horses N2O': {
              'Table3.B(b)': ['Horses', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size',  nan,'(1000s)', nan]
          },
          
          
          'Poultry N2O': {
              'Table3.B(b)': ['Poultry', 'ACTIVITY  DATA  AND  OTHER  RELATED  INFORMATION', 'Population  size',  nan,'(1000s)', nan]
          },
          
          
          'Dairy cattle N2O MM ': {
              'Table3.B(b)': ['Dairy cattle', 'EMISSIONS', 'N2O', 'Direct', nan, '(kt)']
          },

           'Non-dairy cattle N2O MM': {
               'Table3.B(b)': ['Non-dairy cattle', 'EMISSIONS', 'N2O','Direct', nan,  '(kt)']
           },

            'Sheep N2O MM': {
                'Table3.B(b)': ['Sheep', 'EMISSIONS', 'N2O', 'Direct', nan, '(kt)']
            },
            
            
            'Swine N2O MM': {
                'Table3.B(b)': ['Swine', 'EMISSIONS', 'N2O', 'Direct', nan, '(kt)']
            },
            
            
            
            'Deer N2O MM': {
                'Table3.B(b)': ['Deer', 'EMISSIONS', 'N2O', 'Direct', nan, '(kt)']
            },
            
            
            
            'Goats N2O MM': {
                'Table3.B(b)': ['Goats', 'EMISSIONS', 'N2O', 'Direct', nan, '(kt)']
            },
            
            
            'Horses N2O MM': {
                'Table3.B(b)': ['Horses', 'EMISSIONS', 'N2O', 'Direct', nan, '(kt)']
            },
            
            
            'Poultry N2O MM': {
                'Table3.B(b)': ['Poultry', 'EMISSIONS', 'N2O','Direct', nan, '(kt)']
            },

}


'''
If you want to create the timeseries only for some countries specify the ISO3 codes of the countries (see example on the
second line below)
'''
COUNTRIES_NAMES: list[Path] = [x for x in (DATA_PATH / 'extracted').iterdir() if x.is_file()]
#COUNTRIES_NAMES: list[Path] = [x for x in COUNTRIES_NAMES if (x.name[:3] in ['deu'] or x.name[:3] in ['aut']) and (not 'Copy' in x.name)]
COUNTRIES_NAMES: list[Path] = [x for x in COUNTRIES_NAMES if (not 'Copy' in x.name)]
'''
Specify a range of years or single years for which you want to create the timeseries
'''
YEARS_LIST: list[int] = list(range(1990, 2022))
#YEARS_LIST: list[int] = [1990]

'''
Specify a name of the file with the timeseries
'''
RESULT_PATH: Path = DATA_PATH / 'structured' / 'UNFCCC_2023_Table3_timeseries.xlsx'
