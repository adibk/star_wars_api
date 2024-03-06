import requests
import pandas as pd

def data(ressources):
    next_page = f"https://swapi.dev/api/{ressources}/"
    all_results = []

    while next_page:
        response = requests.get(next_page)
        if response.status_code == 200:
            data = response.json()

            all_results.extend(data['results'])

            next_page = data['next']
        else:
            print("Erreur lors de la récupération des données.")
            return None

    df = pd.DataFrame(all_results)
    return df

ressources_df = data("vehicles")
if ressources_df is not None:
    display(ressources_df)
