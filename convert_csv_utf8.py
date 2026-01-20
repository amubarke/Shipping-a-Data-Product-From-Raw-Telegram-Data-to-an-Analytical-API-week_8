import pandas as pd
import glob
import os

input_folder = r"E:/Shipping-a-Data-Product-From-Raw-Telegram-Data-to-an-Analytical-API-week_8/data/csv/telegram_messages/2026-01-17"
output_folder = input_folder  # or choose another folder

csv_files = glob.glob(os.path.join(input_folder, "*.csv"))

for file in csv_files:
    print(f"Processing {file}")
    
    # Read file as bytes
    with open(file, 'rb') as f:
        content = f.read()
    
    # Decode bytes to string, replacing bad characters
    text = content.decode('cp1252', errors='replace')  # or 'ignore'
    
    # Convert string to pandas dataframe
    from io import StringIO
    df = pd.read_csv(StringIO(text))
    
    # Save as UTF-8 CSV
    output_file = os.path.join(output_folder, os.path.basename(file).replace(".csv", "_utf8.csv"))
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"Saved {output_file}")
