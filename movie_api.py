import requests
import time
import aiohttp
import asyncio
from config.config import API_KEY


def get_movie_details(movie_id, max_retries=3, retry_delay=2):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
    }
    
    retries = 0

    while retries < max_retries:
        response = requests.get(url, params=params)
        
        # Cas de succès (status code 200)
        if response.status_code == 200:
            data = response.json()
            movie_info = {
                "titre": data.get("title"),
                "date de sortie": data.get("release_date"),
                "genre": [genre['name'] for genre in data.get("genres", [])],
                "popularité": data.get("popularity"),
                "pays": data.get("origin_country")
            }
            return movie_info

        # Gestion des erreurs spécifiques
        elif response.status_code == 429:  # Too Many Requests
            print("Trop de requêtes - pause de 10 secondes")
            time.sleep(10)  # Pause de 10 secondes avant retry
        
        elif response.status_code in [500, 503]:  # Erreurs serveur
            print(f"Erreur serveur {response.status_code} - nouvelle tentative après {retry_delay} secondes")
            time.sleep(retry_delay)  # Pause avant la prochaine tentative
            retries += 1
            retry_delay *= 2  # Augmentation du délai (exponential backoff)
        
        elif response.status_code == 400:  # Bad Request
            return f"Erreur {response.status_code}: Mauvaise requête - vérifiez les paramètres."

        elif response.status_code == 401:  # Unauthorized
            return f"Erreur {response.status_code}: Clé API invalide ou manquante."

        elif response.status_code == 403:  # Forbidden
            return f"Erreur {response.status_code}: Accès interdit - permissions insuffisantes."

        elif response.status_code == 404:  # Not Found
            return f"Erreur {response.status_code}: Film non trouvé pour l'ID {movie_id}."

        else:  # Autres erreurs non gérées spécifiquement
            return f"Erreur {response.status_code}: Une erreur est survenue."

    # Si on dépasse le nombre de retries autorisé
    return f"Échec après {max_retries} tentatives : le serveur ne répond pas."

# ==========================================================
#  création de la fonction qui permet de gérer des millions de requêtes de manière efficace et simulez à l’aide d’un script une charge très élevée de call vers plusieurs rootes
# Fonction asynchrone pour envoyer une requête HTTP
async def fetch(session, url):
    try:
        async with session.get(url) as response:
            status = response.status
            data = await response.text()
            print(f"Requête à {url} - Status: {status}")
            return data
    except Exception as e:
        print(f"Erreur lors de l'accès à {url}: {e}")
        return None

# Fonction pour gérer plusieurs requêtes en parallèle
async def handle_requests(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]  # Création de tâches pour chaque URL
        results = await asyncio.gather(*tasks)  # Exécuter toutes les requêtes en parallèle
        return results

# Simuler une charge élevée avec plusieurs requêtes
def simulate_high_load(urls, num_requests):
    start_time = time.time()

    # Créer une liste d'URLs à requêter
    all_urls = urls * num_requests  # Par exemple, multiplier chaque URL par num_requests fois

    # Lancer la boucle asyncio
    asyncio.run(handle_requests(all_urls))

    end_time = time.time()
    print(f"Requêtes terminées en {end_time - start_time:.2f} secondes.")

# Liste des routes à tester
urls = [
    "https://api.themoviedb.org/3/configuration",
    "http://127.0.0.1:5000/movie/550",
    " https://api.themoviedb.org/3/movie/popular"
]

# Simuler 1000 requêtes pour chaque URL
# simulate_high_load(urls, num_requests=1000)
