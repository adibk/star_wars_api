import requests

#Récupère tous les nom de mes characters en une liste

def get_characters_names():
    next_page = "https://swapi.dev/api/people/"
    all_results = []

    while next_page:
        response = requests.get(next_page)
        if response.status_code == 200:
            data = response.json()

            all_results.extend(data['results'])

            next_page = data['next']
        else:
            print("Fail, essaye encore !")
            return None

    names = [result['name'] for result in all_results]
    return names

character_names = get_characters_names()

if character_names is not None:
    result_string = ", ".join(character_names)
    print("Personnages :", result_string)


###################################################################
#Récupères mes nom de personnages et leur apparition dans les films

def characters_and_films():
    characters_url = "https://swapi.dev/api/people/"
    response = requests.get(characters_url)

    if response.status_code == 200:
        characters_data = response.json()['results']
        for character in characters_data:
            films = [requests.get(film).json()['title'] for film in character['films']]
            print(f"Personnage : {character['name']}")
            print("Apparition dans les films :", films)
            print()
    else:
        print("Fail, essaye encore !")

characters_and_films()

###################################################################
#Récupère et tri uniquement les colonnes "name" & "classification"

def species_data():
    next_page = "https://swapi.dev/api/species/"
    all_results = []

    while next_page:
        response = requests.get(next_page)
        if response.status_code == 200:
            data = response.json()

            all_results.extend(data['results'])

            next_page = data['next']
        else:
            print("Fail, essaye encore !")
            return None

    df = pd.DataFrame(all_results)
    return df

species_df = species_data()

#Je tri par la classification

if species_df is not None:
    selected_columns = ['name', 'classification']
    species_df = species_df[selected_columns].sort_values(by='classification')
    display(species_df)

###################################################################
#Classification en fonction de la "classification" dans des dataframes dédiés

def species_data():
    url = "https://swapi.dev/api/species/"
    all_results = []

    while url:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            all_results.extend(data['results'])
            url = data['next']
        else:
            print("Fail, essaye encore !")
            return None

    return pd.DataFrame(all_results)

def species_by_classification(df):
    if not df.empty:
        df = df[['name', 'classification']].sort_values(by='name')
        for classification, group in df.groupby('classification'):
            print(f"Classification: {classification}")
            display(group)
            print()
    else:
        print("DataFrame vide")

species_df = species_data()

if species_df is not None:
    species_by_classification(species_df)
