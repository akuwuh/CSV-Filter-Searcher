import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

breaker = False

filter_condition = defaultdict(set)

data = pd.read_csv("vfc/vfc.csv")


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

filter_condition = {
    'SCHOOL_EDUCATION_LEVEL': {'MIDDLE SCHOOL'}, 
    'PUBLIC_OR_INDEPENDENT': {'Public School'}
}


print()
print("Conditions Applied: \n")
print(dict(filter_condition))


df = pd.DataFrame(data)
filtered_df = df

for column,value in filter_condition.items():
    filtered_df = filtered_df[filtered_df[column].isin(value)]


filtered_df.to_csv('vfc/results.csv', index=False)

with open('vfc/search_terms.txt', 'w') as f:
    f.write(filtered_df['SCHOOL_NAME'].str.cat(sep='\n'))



