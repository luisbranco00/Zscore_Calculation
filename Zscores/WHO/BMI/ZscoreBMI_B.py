import pandas as pd
import csv
from scipy.stats import norm
import numpy as np


# Read the CSV file with the specified encoding and delimiter
data = pd.read_csv(r'Path_to_csv_file', encoding='utf-8', delimiter=';')
# Get the column names from the DataFrame
variable_names = data.columns.tolist()



# Calculate BMI and Zscore for each row and add them as new columns
data_with_zscore = []
for _, row in data.iterrows():
    if pd.isnull(row[['Height_B', 'Weight_without_clothes_B', 'Gender', 'Age_months_B']]).any():
        continue  # Skip row if any of the required columns contain null values

    height_str = row[variable_names.index('Height_B')]
    if not height_str.strip():  # Check if the string is empty or contains only whitespace
        continue  # Skip row if the height value is empty

    height = float(height_str.replace(',', '.'))  # Replace comma with dot and convert to float

    weight_str = row[variable_names.index('Weight_without_clothes_B')]
    if not weight_str.strip():  # Check if the string is empty or contains only whitespace
        continue  # Skip row if the weight value is empty

    weight = float(weight_str.replace(',', '.'))  # Replace comma with dot and convert to float
    gender = row[variable_names.index('Gender')]
    age = int(row[variable_names.index('Age_months_B')])
    bmi = weight / ((height / 100) ** 2)  # Calculate BMI
    
    if gender == 0:
        bmi_file = pd.read_csv(r"\Zscores\WHO\BMI\bmi-girls-z-who-2007-exp.csv", encoding='utf-8', delimiter=';')
    elif gender == 1:
        bmi_file = pd.read_csv(r"\Zscores\WHO\BMI\bmi-boys-z-who-2007-exp.csv", encoding='utf-8', delimiter=';')
    matched_rows=[]
    for _, bmi_row in bmi_file.iterrows():
        if int(bmi_row['Month']) == age:
            matched_rows.append(bmi_row)

    if matched_rows:
        matched_row = matched_rows[0]
        # Consider only the first match if multiple matches found
        L_value = float(matched_row['L'].replace(',', '.'))
        M_value = float(matched_row['M'].replace(',', '.'))
        S_value = float(matched_row['S'].replace(',', '.'))
        SD2=float(matched_row['SD2'].replace(',', '.'))
        SD2neg=float(matched_row['SD2neg'].replace(',', '.'))
        SD3=float(matched_row['SD3'].replace(',', '.'))
        SD3neg = float(matched_row['SD3neg'].replace(',', '.'))
        SD23 = SD3-SD2
        SD23neg = SD2neg - SD3neg
        zscore = (((bmi / M_value) ** L_value) - 1) / (S_value * L_value)
        zscore1 = (zscore + (0.5 * np.sign(zscore))) / (1 + (0.25 * zscore**2))
        
        if zscore > 3:
            zscore_f= 3 + ((bmi - SD3)/SD23)  
            
        elif zscore < -3:
            zscore_f = -3 + ((bmi - SD3neg)/SD23neg)
        else:
            zscore_f=zscore
    else:
        zscore = ''
    print(zscore1, zscore_f)


    # Add the calculated BMI and Zscore to the row
    row['bmi'] = bmi
    row['Zscore'] = zscore
    row['ZscoreF'] = zscore_f
    
    data_with_zscore.append(row)
    

# Create a new DataFrame with the updated data
data_with_zscore = pd.DataFrame(data_with_zscore)

# Write the updated data with BMI and Zscore to a new CSV file
output_file = r'\data_with_BMI_zscoreF_B.csv'
data_with_zscore.to_csv(output_file, index=False)

print("Zscore calculation and column addition completed.")
