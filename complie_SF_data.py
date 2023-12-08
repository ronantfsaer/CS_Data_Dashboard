import pandas as pd

def merge_datasets(subscriptions_file, cases_file, output_file, encoding='utf-8'):
    try:
        # Load the subscription and cases data with specified encoding
        subscriptions = pd.read_csv(subscriptions_file, encoding=encoding)
        cases = pd.read_csv(cases_file, encoding=encoding)

        # Perform a left join on the key 'Subscription'
        merged_data = pd.merge(subscriptions, cases, on='Subscription', how='left')

        # Handle missing values (optional, modify as needed)
        # Example: Replace NaN in specific columns with a default value
        # merged_data.fillna({'column_name': 'default_value'}, inplace=True)

        # Export the merged data to a new CSV file
        merged_data.to_csv(output_file, index=False)
        print(f"Merged data saved to {output_file}")

    except UnicodeDecodeError as e:
        print(f"Error reading files: {e}")
        print("Trying with a different encoding...")

        # Retry with a different encoding if UTF-8 fails
        merge_datasets(subscriptions_file, cases_file, output_file, encoding='ISO-8859-1')

# Replace with your actual file paths
subscriptions_file = 'contract export test 1.csv'
cases_file = 'cases report test 1.csv'
output_file = 'DEVELOPMENT_SF_merge.csv'

# Run the merge function
merge_datasets(subscriptions_file, cases_file, output_file)


#TODO: chenge name of subscrition number column in contract data
# remove account owner from cases column
# cases product column blank, look into this
# fix uni code error
#  columns coming back with _x or _y in name ; remove redundant duplicates in the column name

