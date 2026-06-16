import pandas as pd
import  numpy as np
import sys
import os
RAW_PATH = 'data/raw/data/Volve_production_data.xlsx'

# DATEPRD  = DAte of Production
# NPD_WELL_BORE_NAME = Well Identifier
# ON_STREAMER_HRS = how long(HOUR) well was producing oil for the day
# FLOW_KIND = Production / injection 
# BORE_OIL_VOL = oil volume for the day
# BORE_GAS_VOL = gas Vol for the day
EXPECTED_COLS = [
    'DATEPRD','NPD_WELL_BORE_NAME' , 'ON_STREAM_HRS', 'BORE_OIL_VOL', 'BORE_GAS_VOL' , 'BORE_WAT_VOL', 'FLOW_KIND' 
    ]
def check_excel(path:str) -> None:
    """Print all sheet name and preview each  """
    print(f"FILE : {path}")

    xl = pd.ExcelFile(path)
    print(f"\n Sheet found ({len(xl.sheet_names)}) : {xl.sheet_names}")

    for sheet in xl.sheet_names:
        preview = pd.read_excel(path,sheet_name=sheet,nrows=3)
        print(f"\n--- Sheet: '{sheet}' ---")
        print(f"  Columns ({len(preview.columns)}): {list(preview.columns)}")
        
        print(f"  First 3 rows:")
        print(preview.to_string(index=False))

### we load excel file and return dataframe
### path = path to excel file
### sheet_name = 0 unless we specify any.


def load(path : str = RAW_PATH,sheet_name : int =0) -> pd.DataFrame:
    print("STEP 1: Reading Excel File")
    df = pd.read_excel(path,sheet_name=sheet_name)
    # row and col, basiclly shape of data
    print(f"SHAPE OF DATE {df.shape[0]:,} rows {df.shape[1]} cols")
    
    # standardize col name by striping space.
    df.columns = [c.strip().upper() for c in df.columns]


    ## check if we are missing any of Expected coloumn
    missing = [c for c in EXPECTED_COLS if c not in df.columns]
    if missing:
        print(f"\nExpected Column not found: {missing}")
        print(f"\nColumns found : {df.columns}")
    else:
        print(f"\nALL EXPECTED COLUMNS ARE PRESENT")

    ## Step 2 Fix coloumn types -> Convert Date to datetime object, numeric values enforce them to be numeric..
    print(f"\n Step 2: Fix coloumn types -> Convert Date to datetime object, numeric values enforce them to be numeric..")
    ## Standardizing Date Column
    if 'DATEPRD' in df.columns:
        df['DATEPRD'] = pd.to_datetime(df['DATEPRD'], errors='coerce')
        df = df.sort_values('DATEPRD').reset_index(drop=True)
        print(f"Date range: {df['DATEPRD'].min().date()} → {df['DATEPRD'].max().date()}")

    ## force Numerical cols to float
    numeric_cols = [
        'ON_STREAM_HRS','AVG_DOWNHOLE_PRESSURE','AVG_DOWNHOLE_TEMPERATURE','AVG_DP_TUBING', 'AVG_ANNULUS_PRESS', 'AVG_CHOKE_SIZE_P',
        'AVG_WHP_P', 'AVG_WHT_P','DP_CHOKE_SIZE','BORE_OIL_VOL', 'BORE_GAS_VOL' , 'BORE_WAT_VOL','BORE_WI_VOL'
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col],errors='coerce')           ## 'coerce' means if invalid value means :NaN

    ## step 3: Filteing row
    print("\n Filter Production ROW")
    if 'FLOW_KIND' in df.columns:
        counts = df['FLOW_KIND'].value_counts()
        print(f"Flow Kind : \n{counts.to_string()}")
        df =df[df['FLOW_KIND'].str.upper().str.strip() == 'PRODUCTION'].copy()
        print(f"\n Production row count: {len(df):,} rows")
    else:
        print(f"\n FLOW_KIND column is missingg.")
    
    ## drop rows when well was off(means ON_STREAM_HRS =0)
    if 'ON_STREAM_HRS' in df.columns:
        before = len(df)
        df = df[df['ON_STREAM_HRS'] >0 ].copy()
        print(f" Dropped {before - len(df):,} rows where well was shut.")
    else:
        print(f"\n ON_STREAM_HRS column is missingg.")

    ## drop rows when well was off(means ON_STREAM_HRS =0)
    if 'BORE_OIL_VOL' in df.columns:
        before = len(df)
        df= df[df['BORE_OIL_VOL'].notna].copy()
        print(f"\n dropped {before - len(df):,} rows where BORE_OIL_VAL is null")
    else:
        print(f"\n BORE_OIL_VAL column is missingg.")

    ## Normalizing
    print(f"\n Normailizinf features.")
    print(f"normailizing oil Production to whole day.")
    
    if  'BORE_OIL_VOL' in df.columns and 'ON_STREM_HRS' in df.columns:
        df['OIL_RATE_NORM']= df['BORE_OIL_VOL'] / df['ON_STREM_HRS'] * 24
        print(f"OIL_RATE NORM = BORE_OIL_VOL / ON_STREM_HRS * 24")
    
    ## High GOR states depletion on reserviour

    if 'BORE_GAS_VOL' in df.columns and 'BORE_OIL_VOL' in df.columns:
        df['GOR'] = df['BORE_GAS_VOL'] / df['BORE_OIL_VOL'].replace(0, np.nan)
        print(f"\nGOR = BORE_GAS_VOL / BORE_OIL_VOL")


    ## Water
    if 'BORE_WAT_VOL' in df.columns and 'BORE_OIL_VOL' in df.columns:
        total_liq = df['BORE_OIL_VAL'] + df['BORE_WAT_VOL']
        df['WCT'] = df['BORE_WAT_VOL'] / total_liq.replace(0,np.nan)
        print(f"Water cut: BORE_WAT_VOL /(BORE_OIL_VOL + BORE_WAT_VOL)")
        

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv)>1 else RAW_PATH

    if not os.path.exists(path):
        print(f"\n ERROT, FILE not Found{path}")
        sys.exit(1)

    
    check_excel(path)

    df = load(path)