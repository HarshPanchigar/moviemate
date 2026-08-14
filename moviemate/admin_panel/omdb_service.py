import urllib.request
import urllib.parse
import json

OMDB_API_KEYS = ['6a4dd6af', 'f6363176', '72bc447a', '3506e780']

def get_keys_list():
    if isinstance(OMDB_API_KEYS, str):
        return [OMDB_API_KEYS]
    return list(OMDB_API_KEYS)

def search_movies_omdb(query):
    if not query:
        return []
    
    encoded_query = urllib.parse.quote(query.strip())
    
    for api_key in get_keys_list():
        try:
            url = f"https://www.omdbapi.com/?s={encoded_query}&type=movie&apikey={api_key}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=6) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    if data.get('Response') == 'True':
                        return data.get('Search', [])
                    elif data.get('Error') and 'limit' not in data.get('Error', '').lower():
                        # Valid response from OMDb but no movies found
                        return []
        except Exception as e:
            print(f"OMDb Search Error with key {api_key}: {e}")
            continue

    return []

def get_movie_details_omdb(imdb_id):
    if not imdb_id:
        return None
    
    encoded_id = urllib.parse.quote(imdb_id.strip())
    
    for api_key in get_keys_list():
        try:
            url = f"https://www.omdbapi.com/?i={encoded_id}&plot=full&apikey={api_key}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=6) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    if data.get('Response') == 'True':
                        return data
        except Exception as e:
            print(f"OMDb Details Error with key {api_key}: {e}")
            continue

    return None
