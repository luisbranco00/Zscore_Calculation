import csv
import pandas as pd
import numpy as np
from scipy.stats import norm


# Read the CSV file with the specified encoding and delimiter
data = pd.read_csv(r'Path_to_csv_file', encoding='utf-8', delimiter=';')
# Get the column names from the DataFrame
variable_names = data.columns.tolist()

def zscore_to_percentile(z_score):
    # Calculate the cumulative distribution function (CDF) value for the given Z-score
    cdf_value = norm.cdf(z_score)
    # Convert CDF value to percentile
    percentile = cdf_value * 100
    return percentile


# Calculate Zscore for each row and add them as new columns
data_with_spp = []
data['Zscore Blood Pressure'] = 999  # Initialize the new column with the value 999 for all rows

for _, row in data.iterrows():
    
    
    
    if pd.isnull(row[['Height_A', 'Gender', 'Age_years_A','Age_months_A' ]]).any():
        continue  # Skip row if any of the required columns contain null values

    height_str = row[variable_names.index('Height_A')]
    if not height_str.strip():  # Check if the string is empty or contains only whitespace
        continue  # Skip row if the height value is empty

    height = float(height_str.replace(',', '.'))  # Replace comma with dot and convert to float
    
    
    ps_str = row[variable_names.index('min_dbp_A')]
    if not ps_str.strip():  # Check if the string is empty or contains only whitespace
        continue  # Skip row if the height value is empty

    ps = float(ps_str.replace(',', '.'))
    
        
        
    
   
    gender = int(row[variable_names.index('Gender')])
    age = int(row[variable_names.index('Age_years_A')])
    age_months = int(row[variable_names.index('Age_months_A')])
    height_inch = height
    id1 =str(row[variable_names.index('ID')])
    height_percentile_file = pd.read_csv(r"\CDC\statage.csv", encoding='utf-8', delimiter=';')
    if gender == 0:
        gender1 = 2
    else:
        gender1=gender
    # Find the rows in the height percentile file that are closest to the age in months
    height_percentile_rows = height_percentile_file[(height_percentile_file['Sex'] == gender1) & (height_percentile_file['Agemos'] > age_months)].head(2)

    # Check if there are two rows returned
    # Get the L, M, and S values for both rows
    l_value = height_percentile_rows['L'].values[0].astype(float)
    m_value = height_percentile_rows['M'].values[0].astype(float)
    s_value = height_percentile_rows['S'].values[0].astype(float)

    # Calculate the height percentile using the estimated L, M, and S values
    
    zscore_height= (((height / m_value) ** l_value) - 1) / (l_value * s_value)
    if zscore_height > 3:
        z_score_height_F = 3 + ((height-(m_value*((1+l_value*s_value*3)**(1/l_value))))/(((m_value*((1+l_value*s_value*3)**(1/l_value))))-(m_value*((1+l_value*s_value*2)**(1/l_value)))))
    elif zscore_height < -3:
        z_score_height_F = -3 + ((height-(m_value*((1+l_value*s_value*(-3))**(1/l_value))))/(((m_value*((1+l_value*s_value*(-2))**(1/l_value))))-(m_value*((1+l_value*s_value*(-3))**(1/l_value)))))
    else:
        z_score_height_F=zscore_height
    
    percentileH=zscore_to_percentile(z_score_height_F)
    
    if gender == 0:
        a=60.50510
        b1=1.01301
        b2=0.001157
        b3=-0.000424
        b4=-0.00137
        Zht1=1.16641
        Zht2=0.12795
        Zht3=-0.03869
        Zht4=-0.00079
        sd=10.9573

    elif gender == 1:
        a=61.01217
        b1=0.68314
        b2=-0.09835
        b3=0.01711
        b4=0.00045
        Zht1=1.46993
        Zht2=-0.07849
        Zht3=-0.03144
        Zht4=0.00967
        sd=11.6032
    
    y = a + (age-10)*b1 + (((age-10)**2)*b2) + (((age-10)**3)*b3) + (((age-10)**4)*b4) + (zscore_height)*Zht1 + (((zscore_height)**2)*Zht2) + (((zscore_height)**3)*Zht3) + (((zscore_height)**4)*Zht4)
    Zbp = ((ps-y)/sd)
    row['Zscore Diastolic Blood Pressure A'] = Zbp
    Zscore_Percentil = zscore_to_percentile(Zbp) 
    print(Zscore_Percentil,percentileH, z_score_height_F, zscore_height)
    # Append the row to the data_with_spp list
    data_with_spp.append({'Zscore Diastolic Blood Pressure A': Zbp,
        'Percentile Diastolic Blood Pressure A': Zscore_Percentil,
        'Id': id1,  # Assuming you want to use the row index as the ID
        'Gender': gender
    })

# Create a new DataFrame from the data_with_spp list
data_with_spp_df = pd.DataFrame(data_with_spp)

# Save the new DataFrame to a CSV file
data_with_spp_df.to_csv(r'\Zscore_DBP_A.csv', index=False, encoding='utf-8', sep=';')
