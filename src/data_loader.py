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
    print("Reading Excel File")
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

    ## Standardizing Date Column
    if 'DATEPRD' in df.columns:
        df['DATEPRD'] = pd.to_datetime(df['DATEPRD'], errors='coerce')
        df = df.sort_values('DATEPRD').reset_index(drop=True)
        print(f"Date range: {df['DATEPRD'].min().date()} → {df['DATEPRD'].max().date()}")

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv)>1 else RAW_PATH

    if not os.path.exists(path):
        print(f"\n ERROT, FILE not Found{path}")
        sys.exit(1)

    
    check_excel(path)

    df = load(path)