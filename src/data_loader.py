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

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv)>1 else RAW_PATH

    if not os.path.exists(path):
        print(f"\n ERROT, FILE not Found{path}")
        sys.exit(1)

    
    