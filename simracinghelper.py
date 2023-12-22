import requests, json
import csv
import pandas as pd

def get_results_by_url(url: str):
    splitted = url.split("/results/")
    full_url = f"{splitted[0]}/results/download/{splitted[1]}.json"

    response = requests.get(full_url)

    if response.status_code == 200:
        print(f"File downloaded successfully")
        return json.loads(response.content)
    else:
        print(f"Failed to download the file. Status Code: {response.status_code}")


# file_path = 'race2a.json'
# with open(file_path, 'r') as file:
#     # Load the JSON content into a Python dictionary
#     data = json.load(file)


SERVER = 'Mid'
RACE = '1A'

POINTS_FILE_PATH = 'pointsbook.xlsx'
df = pd.read_excel(POINTS_FILE_PATH, sheet_name=SERVER, skiprows=[0,1,2])


URL = 'https://fs-server-2.emperorservers.com/results/2023_11_11_19_36_RACE'

data = get_results_by_url(URL)

results = data['Result']


for pos, result in enumerate(results):
    driver = result['DriverName']
    position = pos+1

    if driver not in df['Driver'].values:
        new_row = pd.DataFrame({'Driver': [driver]})
        
        # Concatenate the new row DataFrame with the original DataFrame
        df = pd.concat([df, new_row], ignore_index=True)

    row_index = df.index[df['Driver'] == driver].tolist()[0]
    df.loc[row_index, 'R'+RACE] = position

df_sorted = df.sort_values(by='Driver')

df_sorted.to_excel(f'{SERVER}{RACE}results.xlsx', index=False, sheet_name=SERVER)
print(f"Updated DataFrame written back to '{POINTS_FILE_PATH}' in sheet '{SERVER}'.")




