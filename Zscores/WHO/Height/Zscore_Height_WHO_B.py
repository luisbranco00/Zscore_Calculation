import pandas as pd
import csv
from scipy.stats import norm
import numpy as np


# Read the CSV file with the specified encoding and delimiter
data = pd.read_csv(r'Path_to_csv_file', encoding='utf-8', delimiter=';')
# Get the column names from the DataFrame
variable_names = data.columns.tolist()



# Calculate Weight and Zscore for each row and add them as new columns
data_with_zscore = []
for _, row in data.iterrows():
    if pd.isnull(row[[ 'Height_B', 'Gender', 'Age_months_B']]).any():
        continue  # Skip row if any of the required columns contain null values

    height_str = row[variable_names.index('Height_B')]
    if not height_str.strip():  # Check if the string is empty or contains only whitespace
        continue  # Skip row if the weight value is empty

    height = float(height_str.replace(',', '.'))  # Replace comma with dot and convert to float
    gender = row[variable_names.index('Gender')]
    age = int(row[variable_names.index('Age_months_B')])
    if gender == 0:
        height_file = pd.read_csv(r"\Zscores\WHO\Height\Height_Table_Girls.csv", encoding='utf-8', delimiter=';')
    elif gender == 1:
        height_file = pd.read_csv(r"\Zscores\WHO\Height\Height_Table_Boys.csv", encoding='utf-8', delimiter=';')
    matched_rows=[]
    for _, height_row in height_file.iterrows():
        if int(height_row['Month']) == age:
            matched_rows.append(height_row)

    if matched_rows:
        matched_row = matched_rows[0]  # Consider only the first match if multiple matches found
        L_value = 1
        M_value = float(matched_row['M'].replace(',', '.'))
        S_value = float(matched_row['S'].replace(',', '.'))
        SD2=float(matched_row['SD2'].replace(',', '.'))
        SD2neg=float(matched_row['SD2neg'].replace(',', '.'))
        SD3=float(matched_row['SD3'].replace(',', '.'))
        SD3neg = float(matched_row['SD3neg'].replace(',', '.'))
        SD23 = SD3-SD2
        SD23neg = SD2neg - SD3neg
        zscore = (((height / M_value) ** L_value) - 1) / (S_value * L_value)
        
        if zscore > 3:
            zscore_f= 3 + ((height - SD3)/SD23)  
            
        elif zscore < -3:
            zscore_f = -3 + ((height - SD3neg)/SD23neg)
        else:
            zscore_f=zscore
    else:
        zscore = ''
        zscore_f= ''
    print(zscore, zscore_f)


    # Add the calculated BMI and Zscore to the row
    row['Zscore_Height_WHO_B'] = zscore
    row['ZscoreF_Height_WHO_B'] = zscore_f
    
    data_with_zscore.append(row)
    

# Create a new DataFrame with the updated data
data_with_zscore = pd.DataFrame(data_with_zscore)

# Write the updated data with Zscore to a new CSV file
output_file = r'\data_with_zscoreF_height_B.csv'
data_with_zscore.to_csv(output_file, index=False)

print("Zscore calculation and column addition completed.")
