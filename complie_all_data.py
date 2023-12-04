import pandas as pd
import numpy as np

# File paths
origin_simulations_file_path = r'C:\Users\RonanFriedlander\OneDrive - Aurora Energy Research\production\Origin\scenarios.csv'
amun_simulations_file_path = r'C:\Users\RonanFriedlander\OneDrive - Aurora Energy Research\production\Amun\amun_stats.csv'
chronos_simulations_file_path = r'C:\Users\RonanFriedlander\OneDrive - Aurora Energy Research\production\Chronos\simulation_projects.csv'

# Load raw product usage data
origin_simulations_df_raw = pd.read_csv(origin_simulations_file_path)
amun_simulations_df_raw = pd.read_csv(amun_simulations_file_path)
chronos_simulations_df_raw = pd.read_csv(chronos_simulations_file_path)

#for each product, take key data and map to universal column labels:

# Define unified set of new column names:
unified_data_column_names = ['Product',
                             'Project ID',
                             'Project Title',
                             'Project Description',
                             'Is Project Deleted',
                             'Simulation Identifier',
                             'Simulation Name',
                             'Simulation Description',
                             'Model Version Identifier',
                             'Inputs Version identifier',
                             'Market Scenario',
                             'Region',
                             'Origin Base Sceanrio',
                             'Origin Sceanrio Type',
                             'Origin Sensitivity',
                             'Origin Published',
                             'Amun Region Wind Data',
                             'Is Deleted',
                             'Run Status',
                             'Chronos Model Errors',
                             'Tenant Domain',
                             'User Created Email',
                             'User Updated Email',
                             'Created at UTC',
                             'Last Update UTC',
                             'Launched UTC',
                             'Run Duration']

#define mapping from each product's raw data columns to product universal column headers:

origin_data_mapping = {
    'project_global_id':'Project ID',
    'scenario_global_id': 'Simulation Identifier',
    'region_group_code': 'Region',
    'base_scenario_global_id': 'Origin Base Sceanrio',
    'scenario_type': 'Origin Sceanrio Type',
    'sensitivity': 'Origin Sensitivity',
    'publish_type':'Origin Published',
    'is_deleted':'Is Deleted',
    'scenario_run_status':'Run Status',
    'tenant':'Tenant Domain',
    'created_by_email':'User Created Email',
    'updated_by': 'User Updated Email',
    'created_at_utc': 'Created at UTC',
    'last_updated': 'Last Update UTC',
    'launched_at_utc': 'Launched UTC'}
chronos_data_mapping = {'project_id':'Project ID',
                        'proj_title':'Project Title',
                        'proj_description':'Project Description',
                        'proj_is_deleted': 'Is Project Deleted',
                        'simulation_id':'Simulation Identifier',
                        'title':'Simulation Name',
                        'description':'Simulation Description',
                        'model_version':'Model Version Identifier',
                        'inputs_version': 'Inputs Version identifier',
                        'region': 'Region',
                        'is_deleted':'Is Deleted',
                        'execution_status':'Run Status',
                        'model_errors':'Chronos Model Errors',
                        'tenant_id':'Tenant Domain',
                        'created_by':'User Created Email',
                        'last_update_by':'User Updated Email',
                        'created_at':'Created at UTC',
                        'last_updated_at':'Last Update UTC',
                        'launch_time':'Launched UTC',
                        'duration_mins':'Run Duration'}


'''

'''
amun_data_mapping = {
                    'project_id': 'Project ID',
                    'project_title': 'Project Title',
                    'valuation_id':'Simulation Identifier',
                    'name': 'Simulation Name',
                    'description':'Simulation Description',
                    'scenario_group_name':'Market Scenario',
                    'region_pmf_region_code':'Region',
                    'region_default_wind_dataset':'Amun Region Wind Data',
                    'is_deleted':'Is Deleted',
                    'run_status':'Run Status',
    'tenant_id':'Tenant Domain',
    'created_by':'User Created Email',
    'created_date':'Created at UTC',
    'run_date':'Launched UTC'}

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


origin_product_data_universally_mapped.to_csv('origin.csv')
chronos_product_data_universally_mapped.to_csv('chronos.csv')
amun_product_data_universally_mapped.to_csv('amun.csv')

#amun_product_data_universally_mapped['Product'] = 'Amun'
#chronos_product_data_universally_mapped['Product'] = 'Chronos'


'''combined_software_data = pd.concat([origin_product_data_universally_mapped,
                         amun_product_data_universally_mapped,
                         chronos_product_data_universally_mapped], ignore_index=True)'''

print('x')