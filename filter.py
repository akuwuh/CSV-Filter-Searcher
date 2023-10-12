import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

breaker = False

filter_condition = defaultdict(set)
path = "" # path for CSV
data = pd.read_csv(path)


while (not breaker):

    print("Available Columns: \n")
    print()

    for cols in data.columns:
        print(cols)
    print()

    # Getting Column to Filter

    try:
        col = input("Enter Column to Filter: \n")

        # invalid entry 
        if col not in data.columns:
            raise ValueError(f"Error: '{col}' is not a valid column name. Please try again. \n")
        
    except ValueError as e:
        print(e)
        continue

    # Getting Property Type to Filter

    col_type = set(data[col])
    print()

    print("Available \'" + col + "\' Properties: \n")
    print()
    for prop in col_type:
        print(prop)
    try:
        type_chosen = input("\nEnter Column Property: \n")

        # invalid entry 
        if type_chosen not in col_type:
            raise ValueError(f"Error: '{type_chosen}' is not a valid property. Please try again. \n")
        
    except ValueError as e:
        print(e)
        continue
    
    
    filter_condition[col].add(type_chosen)
    print(f"Successfully added '{col}' : '{type_chosen}' to filter conditions \n")

    add_more = False
    while True:
        try:
            more_input = input("Would you like to add more? (Y/N): \n")
            if more_input == "Y":
                add_more = True
                break
            elif more_input == "N":
                break
            else:
                raise ValueError(f"Please choose either 'Y' or 'N'.")
                
        except ValueError as e:
            print(e)
            continue
            
    if add_more == False: breaker = False  


print()
print("Conditions Applied: \n")
print(dict(filter_condition))


df = pd.DataFrame(data)
filtered_df = df

for column,value in filter_condition.items():
    filtered_df = filtered_df[filtered_df[column].isin(value)]

export_path = "" # path to export filtered result (CSV)
filtered_df.to_csv(export_path, index=False)

txt_path = "" # path to export specific column results to use as search terms (TXT)
with open(txt_path, 'w') as f:
    column_to_export = "" 
    f.write(filtered_df[column_to_export].str.cat(sep='\n'))



