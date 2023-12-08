import pandas as pd
import numpy as np
import os

from pydantic import BaseModel, ValidationError
from typing import Optional, Any

# File paths
origin_simulations_file_path = r'C:\Users\RonanFriedlander\OneDrive - Aurora Energy Research\production\Origin\scenarios.csv'
amun_simulations_file_path = r'C:\Users\RonanFriedlander\OneDrive - Aurora Energy Research\production\Amun\amun_stats.csv'
chronos_simulations_file_path = r'C:\Users\RonanFriedlander\OneDrive - Aurora Energy Research\production\Chronos\simulation_projects.csv'

# Load raw product usage data
origin_simulations_df_raw = pd.read_csv(origin_simulations_file_path)
amun_simulations_df_raw = pd.read_csv(amun_simulations_file_path)
chronos_simulations_df_raw = pd.read_csv(chronos_simulations_file_path)

#define mapping from each product's raw data columns to product universal column headers:

Product_mapping_excel_file_path = 'column_mappings.xlsx'

# Read each sheet into a DataFrame
origin_mapping_df = pd.read_excel(Product_mapping_excel_file_path, sheet_name='Origin')
chronos_mapping_df = pd.read_excel(Product_mapping_excel_file_path, sheet_name='Chronos')
amun_mapping_df = pd.read_excel(Product_mapping_excel_file_path, sheet_name='Amun')

# Convert the Product DataFrames to dictionaries
origin_data_mapping = dict(zip(origin_mapping_df['Original Column'], origin_mapping_df['Universal Product Column']))
chronos_data_mapping = dict(zip(chronos_mapping_df['Original Column'], chronos_mapping_df['Universal Product Column']))
amun_data_mapping = dict(zip(amun_mapping_df['Original Column'], amun_mapping_df['Universal Product Column']))

#import list of unified column names:
unified_columns_df = pd.read_excel(Product_mapping_excel_file_path, sheet_name='Unified Column Names')
unified_data_column_names = unified_columns_df['Unified Column Names'].tolist()

# Function to map and rename columns
def map_and_rename_dataframe(df, mapping):

    # Rename existing columns based on mapping
    df = df.rename(columns=mapping)

    # Add any missing new columns as NaN
    cols_not_in_unified_data_cols = set(unified_data_column_names) - set(df.columns)

    for col in cols_not_in_unified_data_cols:
        df[col] = np.nan
    return df

#map each product data to product universal column names and order
origin_product_data_universally_mapped = map_and_rename_dataframe(origin_simulations_df_raw,origin_data_mapping)
origin_product_data_universally_mapped = origin_product_data_universally_mapped[unified_data_column_names]

chronos_product_data_universally_mapped = map_and_rename_dataframe(chronos_simulations_df_raw, chronos_data_mapping)
chronos_product_data_universally_mapped = chronos_product_data_universally_mapped[unified_data_column_names]

amun_product_data_universally_mapped = map_and_rename_dataframe(amun_simulations_df_raw, amun_data_mapping)
amun_product_data_universally_mapped = amun_product_data_universally_mapped[unified_data_column_names]

#specify explictly which software product:
origin_product_data_universally_mapped['Product'] = 'Origin'
chronos_product_data_universally_mapped['Product'] = 'Chronos'
amun_product_data_universally_mapped['Product'] = 'Aumn'

#Data Validation for unfied product data:
# define functions to process data for validation
def replace_nan_with_none(df):
    '''Pandas NaN -> python None

        1) Optional Fields in Pydantic:
        e.g. Optional[str]: -> Pydantic expects the input for that field to be either a string or None.
        Pandas, missing values == NaN (type float).

        2) Data Type Mismatch:
        If Pydantic gets a NaN (float) => validation error as expects a string or None

        -------

        'object' Type in Pandas: string or mixed types. For instance, a column with text data will have an object dtype.'''

    # Replace NaN with None for all columns in DataFrame
    for col in df.columns:
        df[col] = df[col].apply(lambda x: None if pd.isna(x) else x)

def set_deleted_values_to_int(df):
    '''' NOT_DELETED' -> 0 , 'DELETED' -> 1'''
    # Replace NaN with None for all columns in DataFrame
    df['Is_Deleted']  = df['Is_Deleted'].apply(lambda x: 1 if x == 'DELETED' else 0 if x == 'NOT_DELETED' else None)

#process dataframes for validation
replace_nan_with_none(origin_product_data_universally_mapped)
set_deleted_values_to_int(origin_product_data_universally_mapped)
replace_nan_with_none(chronos_product_data_universally_mapped)
replace_nan_with_none(amun_product_data_universally_mapped)

#define Base Model Instance for Data Validation
class ProductDataModel(BaseModel):

    #Define the accepted data types of each unifed column, optional used as can be blank
    Product: Optional[str]
    Project_ID: Optional[str]
    Project_Title: Optional[str]
    Project_Description: Optional[str]
    Is_Project_Deleted: Optional[int]
    Simulation_Identifier: Any
    Simulation_Name: Optional[str]
    Simulation_Description: Optional[str]
    Model_Version_Identifier: Optional[str]
    Inputs_Version_identifier: Optional[str]
    Market_Scenario: Optional[str] #TODO
    Region: Optional[str]
    Origin_Base_Scenario: Optional[str]
    Origin_Scenario_Type: Optional[str]
    Origin_Sensitivity: Optional[str]
    Origin_Published: Optional[str]
    Amun_Region_Wind_Data: Optional[str]
    Is_Deleted: Optional[int] #TODO function to transform to int for Origin
    Run_Status: Optional[str]
    Chronos_Model_Errors: Optional[str]
    Tenant_Domain: Any #TODO custom validation as email
    User_Created_Email: Any #TODO custom validation as email
    User_Updated_Email: Any #TODO custom validation as email
    #TODO: for time fields; determine the type of data this is or should be , date time? Will be slow. -> only add if powerBI needs
    Created_at_UTC: Any
    Last_Update_UTC: Any
    Launched_UTC: Any
    Run_Duration: Any

def validate_dataframe(df, model):
    '''function to validate a df using a Pydantic Base Model Instance'''
    validated_data = []
    for _, row in df.iterrows():
        try:
            validated_data.append(model(**row.to_dict()).dict())
        except ValidationError as e:
            # Handle or log the validation error
            print(f"Validation error: {e}")
    return pd.DataFrame(validated_data)

# validate data frames
validated_origin_data = validate_dataframe(origin_product_data_universally_mapped, ProductDataModel)
validated_chronos_data = validate_dataframe(chronos_product_data_universally_mapped, ProductDataModel)
validated_amun_data = validate_dataframe(amun_product_data_universally_mapped, ProductDataModel)

combined_product_df = pd.concat([validated_origin_data, validated_chronos_data, validated_amun_data], ignore_index=True)

#concat the validated data into single data frame:
#TODO

#combined_software_data.to_csv('combined.csv')
'''origin_product_data_universally_mapped.to_csv('origin.csv')
chronos_product_data_universally_mapped.to_csv('chronos.csv')
amun_product_data_universally_mapped.to_csv('amun.csv')'''


output_folder_path = 'output_csvs'

# Check if the folder exists
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# File path
file_path = os.path.join(output_folder_path, 'combined_product_data.csv')

# Save the DataFrame to CSV
combined_product_df.to_csv(file_path)
combined_product_df.to_csv('output_csvs\scombined product data.csv')

#TODO refine data formating