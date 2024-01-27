import pandas as pd
import csv
from scipy.stats import norm
import numpy as np


# Read the CSV file with the specified encoding and delimiter
data = pd.read_csv(r'C:\Users\luisb\Downloads\Be_24072023.csv', encoding='utf-8', delimiter=';')
# Get the column names from the DataFrame
variable_names = data.columns.tolist()



# Calculate Weight and Zscore for each row and add them as new columns
data_with_zscore = []
for _, row in data.iterrows():
    if pd.isnull(row[[ 'Weight_without_clothes_A', 'Gender', 'Age_months_A']]).any():
        continue  # Skip row if any of the required columns contain null values

    weight_str = row[variable_names.index('Weight_without_clothes_A')]
    if not weight_str.strip():  # Check if the string is empty or contains only whitespace
        continue  # Skip row if the weight value is empty

    weight = float(weight_str.replace(',', '.'))  # Replace comma with dot and convert to float
    gender = row[variable_names.index('Gender')]
    age = int(row[variable_names.index('Age_months_A')])
    if age > 120:
        pass
    
    if gender == 0:
        weight_file = pd.read_csv(r"C:\Users\luisb\OneDrive\Ambiente de Trabalho\Zscores\WHO\Weight\Weight_Table_Girls.csv", encoding='utf-8', delimiter=';')
    elif gender == 1:
        weight_file = pd.read_csv(r"C:\Users\luisb\OneDrive\Ambiente de Trabalho\Zscores\WHO\Weight\Weight_Table_Boys.csv", encoding='utf-8', delimiter=';')
    matched_rows=[]
    for _, weight_row in weight_file.iterrows():
        if int(weight_row['Month']) == age:
            matched_rows.append(weight_row)

    if matched_rows:
        matched_row = matched_rows[0]  # Consider only the first match if multiple matches found
        L_value = float(matched_row['L'].replace(',', '.'))
        M_value = float(matched_row['M'].replace(',', '.'))
        S_value = float(matched_row['S'].replace(',', '.'))
        SD2=float(matched_row['SD2'].replace(',', '.'))
        SD2neg=float(matched_row['SD2neg'].replace(',', '.'))
        SD3=float(matched_row['SD3'].replace(',', '.'))
        SD3neg = float(matched_row['SD3neg'].replace(',', '.'))
        SD23 = SD3-SD2
        SD23neg = SD2neg - SD3neg
        zscore = (((weight / M_value) ** L_value) - 1) / (S_value * L_value)
        
        if zscore > 3:
            zscore_f= 3 + ((weight - SD3)/SD23)  
            
        elif zscore < -3:
            zscore_f = -3 + ((weight - SD3neg)/SD23neg)
        else:
            zscore_f=zscore
    else:
        zscore = ''
        zscore_f= ''
    print(zscore, zscore_f)


    # Add the calculated BMI and Zscore to the row
    row['Zscore_Weight_WHO_A'] = zscore
    row['ZscoreF_Weight_WHO_A'] = zscore_f
    
    data_with_zscore.append(row)
    

# Create a new DataFrame with the updated data
data_with_zscore = pd.DataFrame(data_with_zscore)

# Write the updated data with Zscore to a new CSV file
output_file = r'C:\Users\luisb\Downloads\data_with_zscoreF_weight_A.csv'
data_with_zscore.to_csv(output_file, index=False)

print("Zscore calculation and column addition completed.")