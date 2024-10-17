from flask import Flask, jsonify
from movie_api import get_movie_details
from movie_api import simulate_high_load

app = Flask(__name__)

# enpoint pour récupérer les informations d'un film en fonction de son id
@app.route('/movie/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
    movie_info = get_movie_details(movie_id)
    return jsonify(movie_info)

# Endpoint pour déclencher la simulation de charge élevée
@app.route('/simulate-load', methods=['GET'])
def simulate_load():
    urls = [
        "https://api.themoviedb.org/3/configuration",
        "http://127.0.0.1:5000/movie/550",
        "https://api.themoviedb.org/3/movie/popular"
    ]
    
    # Simuler 1000 requêtes pour chaque URL
    simulate_high_load(urls, num_requests=1000)
    
    return jsonify({"message": "Simulation de charge élevée terminée"})


if __name__ == '__main__':
    app.run(debug=True)