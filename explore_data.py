# 1_explore_data.py
import pandas as pd
import os

# Point to the correct folder
data_folder = "./uber_trip_data"  

# List all files in that folder to see exact names
print("Files in uber_trip_data folder:")
try:
    all_files = os.listdir(data_folder)
    for f in all_files:
        print(f"  - {f}")
except FileNotFoundError:
    print(f"Folder '{data_folder}' not found!")
    print("Current directory:", os.getcwd())
    print("Available folders:", [d for d in os.listdir('.') if os.path.isdir(d)])
    exit()

# Now try to read each file
sample_dfs = []
for file_name in all_files:
    path = os.path.join(data_folder, file_name)
    
    # Skip non-data files
    if file_name.startswith('.') or 'taxi' in file_name.lower():
        print(f"\nSkipping {file_name} (not a raw data file)")
        continue
        
    try:
        print(f"\n--- Reading {file_name} ---")
        df_sample = pd.read_csv(path, nrows=5)
        print(f"Columns: {list(df_sample.columns)}")
        print(f"First row:\n{df_sample.iloc[0]}")
        sample_dfs.append(df_sample)
    except Exception as e:
        print(f"Error reading {file_name}: {e}")
        # Try to see first line as raw text
        try:
            with open(path, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                print(f"Raw first line: {repr(first_line[:200])}")
        except:
            pass

# Analyze combined data
if sample_dfs:
    combined = pd.concat(sample_dfs, ignore_index=True)
    print("\n" + "="*50)
    print("COMBINED SAMPLE STATS")
    print("="*50)
    print(f"Total rows sampled: {len(combined)}")
    print(f"Columns found: {list(combined.columns)}")
    
    # Detect coordinates
    lat_cols = [c for c in combined.columns if 'lat' in c.lower()]
    lon_cols = [c for c in combined.columns if 'lon' in c.lower()]
    
    if lat_cols and lon_cols:
        print(f"\nLatitude column: {lat_cols[0]}")
        print(f"Longitude column: {lon_cols[0]}")
        print(f"Latitude range: {combined[lat_cols[0]].min():.4f} to {combined[lat_cols[0]].max():.4f}")
        print(f"Longitude range: {combined[lon_cols[0]].min():.4f} to {combined[lon_cols[0]].max():.4f}")
    else:
        print("\nWARNING: Could not find latitude/longitude columns")
        print("Please check column names above")