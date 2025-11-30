import pandas as pd
import sys
import os

# 1. Get the input file path from n8n
if len(sys.argv) > 1:
    input_file_path = sys.argv[1]
else:
    print("Error: No file path provided.")
    sys.exit(1)

# 2. Load the Data
try:
    df = pd.read_csv(input_file_path)
except Exception:
    # If it fails, try reading with different encoding or as excel if needed
    sys.exit(1)

# 3. The Cleaning Logic
# A. Standardize Headers
df.columns = [c.strip().title() for c in df.columns]

# B. Drop rows missing crucial info (Order ID)
df.dropna(subset=['Order Id'], inplace=True)

# C. Fix Names (Title Case)
if 'Customer Name' in df.columns:
    df['Customer Name'] = df['Customer Name'].str.title()

# D. Fix Dates (Standardize to YYYY-MM-DD)
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

# 4. Save to 'clean_output' folder
# This constructs the path: D:\...\clean_output\clean_sales_data.csv
output_dir = os.path.join(os.path.dirname(os.path.dirname(input_file_path)), "clean_output")
filename = "clean_" + os.path.basename(input_file_path)
output_path = os.path.join(output_dir, filename)

df.to_csv(output_path, index=False)

# Print the new path so n8n can read it later
print(output_path)