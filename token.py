"""
Functions related to token for get/post requests.
"""
import secrets
import json
import requests
import python_ta
import webscrapping

relevant_genres = ["Mystery", "Psychological", "Supernatural", "Seinen", "Action", "Comedy",
                   "School", "Sci-Fi", "Drama", "Mecha", "Adventure", "Fantasy",
                   "Romance", "Sports", "Slice of Life", "Ecchi", "Horror"]

client_id = "ae9e9340ffb8d7aeffbd2140bb599d24"
secret_client_id = "392f86054d5bc6a8342e7fecd3fda8d4d91acad00ad1638ddc7da9a3d147ef69"


def generate_code_challenge() -> str:
    """Creates a 128 random character string for the code_challenge
    parameter for Access Token generation

    Preconditions:
        - None
    """
    token = secrets.token_urlsafe(100)
    return token[:128]


def generate_authorization_url(code_challenge: str) -> str:
    """Generate an authorization link for user to obtain Access Token

    Preconditions:
        - generate_code_challenge() has already been run
    """
    url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={client_id}' \
          f'&code_challenge={code_challenge}'
    return url


def get_code() -> str:
    """Gets Authorization Code from myapp.py

    Preconditions:
        - myapp.py is running successfully
        - token.generate_authorization_url has been opened and
        the authorization procedure has been completed
    """
    file1 = open('code.txt', 'r')
    authorization_code = file1.read()
    return authorization_code


def generate_new_token(authorization_code: str, code_verifier: str) -> str:
    """Function for generating the Access Token to get user data from MAL

    Preconditions:
        - myapp.py is running successfully
        - token.generate_authorization_url has been opened and
        the authorization procedure has been completed
    """
    url = 'https://myanimelist.net/v1/oauth2/token'
    data = {
        'client_id': client_id,
        'client_secret': secret_client_id,
        'code': authorization_code,
        'code_verifier': code_verifier,
        'grant_type': 'authorization_code'
    }

    response = requests.post(url, data)
    response.raise_for_status()
    token = response.json()
    response.close()

    at = token['access_token']
    return at


def generate_top_100(access_token: str) -> list:
    """Gets the top 100 animes on my anime list

    Preconditions:
        - access_token has been generated successfully
    """
    url = 'https://api.myanimelist.net/v2/users/@me'
    response = requests.get(url, headers={'Authorization': f'Bearer {access_token}'})

    response.raise_for_status()
    response.close()

    request = requests.get(f"https://api.myanimelist.net/v2/anime/ranking?"
                           "ranking_type=all&limit=100'",
                           headers={'Authorization': f'Bearer {access_token}'})
    hundo = request.json()

    ids = []
    for elem in hundo['data']:
        ids.append(elem['node']['id'])

    return ids


def generate_500_anime_dict(access_token: str) -> None:
    """Gets the top 100 animes on my anime list

    Preconditions:
        - access_token has been ran successfully
        - path to id_data.json is valid
        - path to five_hundo.json is valid
    """

    def helper(anime: list, content: dict) -> None:
        """... """
        for show in anime:
            anime_request = requests.get(f"https://api.myanimelist.net/v2/anime/{show}?fields"
                                         f"=alternative_titles,synopsis,mean,rank,popularity,"
                                         f"genres,num_episodes,related_anime",
                                         headers={'Authorization': f'Bearer {access_token}'})

            if anime_request.status_code != 200:
                missed.append(show)
            else:
                anime_request_json = anime_request.json()

                genres = []
                for item in anime_request_json['genres']:
                    if item["name"] in relevant_genres:
                        if item["name"] == "School":
                            genres.append("Slice of Life")
                        elif item["name"] == "Supernatural":
                            genres.append("Sci-Fi")
                        else:
                            genres.append(item["name"])

                if anime_request_json['num_episodes'] == 1:
                    length = 'movie'
                elif 2 < anime_request_json['num_episodes'] <= 12:
                    length = 'mini-series (~12 eps)'
                elif 13 < anime_request_json['num_episodes'] <= 26:
                    length = 'short series (~26 eps)'
                elif 27 < anime_request_json['num_episodes'] <= 50:
                    length = 'average series (~50+ eps)'
                else:
                    length = 'long series (~100+ eps)'

                content[anime_request_json['id']] = [anime_request_json['title'],
                                                     anime_request_json['main_picture']['large'],
                                                     length,
                                                     anime_request_json['synopsis'],
                                                     genres]

    url = 'https://api.myanimelist.net/v2/users/@me'
    response = requests.get(url, headers={'Authorization': f'Bearer {access_token}'})

    response.raise_for_status()
    response.close()

    with open('id_data.json') as f:
        anime = json.load(f)

    missed = []
    content = {}
    helper(anime[:len(anime) // 2], content)
    helper(anime[len(anime) // 2:], content)
    print(missed)
    helper(missed, content)

    with open('five_hundo.json', 'w') as fp:
        json.dump(content, fp, sort_keys=True, indent=1)


def generate_user_json(access_token: str, mal: dict) -> None:
    """Generates current user's json file with small info given a dictionary.

    Preconditions:
        - access_token has been ran successfully
    """

    url = 'https://api.myanimelist.net/v2/users/@me'
    response = requests.get(url, headers={'Authorization': f'Bearer {access_token}'})

    response.raise_for_status()
    response.close()

    user_request = requests.get(f"https://api.myanimelist.net/v2/users/@me/"
                                "animelist?fields=completed,list_status&limit=500'",
                                headers={'Authorization': f'Bearer {access_token}'})
    user_data = user_request.json()

    content2 = []
    if "error" in user_data:
        pass
    else:
        if "data" in user_data:
            for item in user_data["data"]:
                if len(item['node']) > 2:
                    id1 = str(item['node']['id'])
                    status = item['list_status']['status']
                    score = item['list_status']['score']
                    if status != 'plan_to_watch' and score != 0:
                        content2.append((id1, score))
        else:
            pass
        if len(content2) > 5:
            mal['user'] = content2


def generate_user2_json(access_token: str, user_name: str, mal: dict) -> None:
    """Generates current user's json file with small info given a dictionary.

        Preconditions:
            - access_token has been ran successfully
        """
    url = 'https://api.myanimelist.net/v2/users/@me'
    response = requests.get(url, headers={'Authorization': f'Bearer {access_token}'})

    response.raise_for_status()
    response.close()

    user_request = requests.get(f"https://api.myanimelist.net/v2/users/{user_name}/"
                                "animelist?fields=completed,list_status&limit=500'",
                                headers={'Authorization': f'Bearer {access_token}'})
    user_data = user_request.json()

    content2 = []
    if "error" in user_data:
        pass
    else:
        if "data" in user_data:
            for item in user_data["data"]:
                if len(item['node']) > 2:
                    id1 = str(item['node']['id'])
                    status = item['list_status']['status']
                    score = item['list_status']['score']
                    if status != 'plan_to_watch' and score != 0:
                        content2.append((id1, score))
        else:
            pass
        if len(content2) > 5:
            mal['user'] = content2


def generate_user_json_full(access_token: str, mal: dict) -> None:
    """Generates current user's json with no skipped content from API calls.

    Preconditions:
        - access_token has been ran successfully
    """
    url = 'https://api.myanimelist.net/v2/users/@me'
    response = requests.get(url, headers={'Authorization': f'Bearer {access_token}'})

    response.raise_for_status()
    user = response.json()
    response.close()

    user_request = requests.get(f"https://api.myanimelist.net/v2/users/@me/"
                                "animelist?fields=completed,list_status&limit=500'",
                                headers={'Authorization': f'Bearer {access_token}'})
    user_data = user_request.json()

    completed = []
    plan2watch = []

    for a in user_data["data"]:
        status = a['list_status']['status']
        title = a['node']['title']
        picture = a['node']['main_picture']['large']
        score = a['list_status']['score']
        eps_watched = a['list_status']['num_episodes_watched']
        id1 = a['node']['id']

        anime_request = requests.get(f"https://api.myanimelist.net/v2/anime/{id1}?fields"
                                     f"=alternative_titles,synopsis,mean,rank,popularity,genres,"
                                     f"num_episodes,related_anime",
                                     headers={'Authorization': f'Bearer {access_token}'})
        anime_request_json = anime_request.json()

        alt_names = [anime_request_json["alternative_titles"]["en"]]
        for name in anime_request_json["alternative_titles"]["synonyms"]:
            alt_names.append(name)

        total_eps = anime_request_json["num_episodes"]
        mean_score = anime_request_json["mean"]
        mal_popularity = anime_request_json["popularity"]
        mal_rank = anime_request_json["rank"]
        synopsis = anime_request_json["synopsis"]

        genres = []
        for element in anime_request_json["genres"]:
            if element["name"] in relevant_genres:
                if element["name"] == "School":
                    genres.append("Slice of Life")
                elif element["name"] == "Supernatural":
                    genres.append("Sci-Fi")
                else:
                    genres.append(element["name"])

        if status == "completed" or "dropped" and score > 0:
            completed.append({title: [
                {'user_data': [score, eps_watched]},
                {'mal_data': [total_eps, mean_score, mal_popularity, mal_rank]},
                {'anime_data': [picture, synopsis, alt_names, genres]}
            ]})
        elif status == "plan_to_watch":
            plan2watch.append({title: [
                {'user_data': [score, eps_watched]},
                {'mal_data': [total_eps, mean_score, mal_popularity, mal_rank]},
                {'anime_data': [picture, synopsis, alt_names, genres]}
            ]})

        mal[user["name"]] = [{'completed': completed},
                             {'plan to watch': plan2watch}]


def generate_userbase_json(access_token: str, user_names: list, data: dict) -> None:
    """Generates a json file with data based on a list of usernames (from user_scrape)

    Preconditions:
        - all usernames in user_names are valid users
        - access token generated successfully
    """

    for username in user_names:
        lookup = requests.get(f"https://api.myanimelist.net/v2/users/{username}/"
                              "animelist?fields=completed,list_status&limit=500'",
                              headers={'Authorization': f'Bearer {access_token}'})
        lookup_json = lookup.json()

        completed2 = []
        plan2watch2 = []
        if "error" in lookup_json:
            pass
        else:
            if "data" in lookup_json:
                # ^ Checks if the request was faulty or not
                for item in lookup_json["data"]:
                    if len(item['node']) > 2:
                        title2 = item['node']['title']
                        picture2 = item['node']['main_picture']['large']
                        status2 = item['list_status']['status']
                        score2 = item['list_status']['score']
                        eps_watched2 = item['list_status']['num_episodes_watched']
                        id2 = item['node']['id']

                        anime_request2 = requests.get(
                            f"https://api.myanimelist.net/v2/anime/{id2}?fields"
                            f"=alternative_titles,synopsis,mean,rank,popularity,genres,"
                            f"num_episodes,related_anime",
                            headers={'Authorization': f'Bearer {access_token}'})
                        anime_request_json2 = anime_request2.json()

                        alt_names2 = [anime_request_json2["alternative_titles"]["en"]]
                        for name2 in anime_request_json2["alternative_titles"]["synonyms"]:
                            alt_names2.append(name2)

                        if len(anime_request_json2) > 10:
                            mean_score2 = anime_request_json2["mean"]
                            mal_rank2 = anime_request_json2["rank"]
                            mal_popularity2 = anime_request_json2["popularity"]
                            total_eps2 = anime_request_json2["num_episodes"]
                            synopsis2 = anime_request_json2["synopsis"]
                        else:
                            mean_score2 = 0
                            mal_rank2 = 0
                            mal_popularity2 = anime_request_json2["popularity"]
                            total_eps2 = anime_request_json2["num_episodes"]
                            synopsis2 = anime_request_json2["synopsis"]

                        genres2 = []
                        for element2 in anime_request_json2["genres"]:
                            if element2["name"] in relevant_genres:
                                if element2["name"] == "School":
                                    genres2.append("Slice of Life")
                                elif element2["name"] == "Supernatural":
                                    genres2.append("Sci-Fi")
                                else:
                                    genres2.append(element2["name"])

                        if status2 == "completed" or "dropped" and score2 > 0:
                            completed2.append({title2: [
                                {'user_data': [score2, eps_watched2]},
                                {'mal_data': [total_eps2, mean_score2, mal_popularity2, mal_rank2]},
                                {'anime_data': [picture2, synopsis2, alt_names2, genres2]}
                            ]})
                        elif status2 == "plan_to_watch":
                            plan2watch2.append({title2: [
                                {'user_data': [score2, eps_watched2]},
                                {'mal_data': [total_eps2, mean_score2, mal_popularity2, mal_rank2]},
                                {'anime_data': [picture2, synopsis2, alt_names2, genres2]}
                            ]})
            else:
                pass
            data[username] = [{'completed': completed2},
                              {'plan to watch': plan2watch2}]


user_base = []
webscrapping.scrape(user_base)

file = open("code.txt", "r+")
file.truncate(0)
file.close()

x = generate_code_challenge()
y = generate_authorization_url(x)
print(y)

# python_ta.check_all(config={
#     'extra-imports': [],  # the names (strs) of imported modules
#     'allowed-io': [],  # the names (strs) of functions that call print/open/input
#     'max-line-length': 100,
#     'disable': ['E1136']
# })
