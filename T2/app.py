from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de dados com filmes do IMDb Top 250
MOVIES = [
    {'id': 1, 'title': 'The Shawshank Redemption', 'rating': 9.3, 'year': 1994},
    {'id': 2, 'title': 'The Godfather', 'rating': 9.2, 'year': 1972},
    {'id': 3, 'title': 'The Dark Knight', 'rating': 9.0, 'year': 2008},
]

# Variável global para manter índice único
max_id = len(MOVIES)


# Retorna lista com todos os filmes
@app.route("/movies", methods=['GET'])
def get_movies():
    return jsonify(MOVIES)

# Busca por um filme com um ID específico
@app.route("/movie/<int:id>", methods=['GET'])
def get_movie(id):
    for movie in MOVIES:
        if movie['id'] == id:
            return jsonify(movie), 200
    return {"error": "Filme não encontrado"}, 404

# Adiciona um novo filme
@app.route("/movie", methods=['POST'])
def add_movie():
    global max_id
    if request.is_json:
        movie_data = request.get_json()
        max_id += 1
        movie_data['id'] = max_id
        MOVIES.append(movie_data)
        return {'id': max_id}, 201
    return {"error": "Formato deve ser JSON"}, 415

# Atualiza um filme existente
@app.route("/movie/<int:id>", methods=['PUT'])
def update_movie(id):
    if request.is_json:
        movie_data = request.get_json()
        for movie in MOVIES:
            if movie['id'] == id:
                movie.update(movie_data)
                return jsonify(movie), 200
        return {"error": "Filme não encontrado"}, 404
    return {"error": "Formato deve ser JSON"}, 415

# Remove um filme pelo ID
@app.route("/movie/<int:id>", methods=['DELETE'])
def delete_movie(id):
    for movie in MOVIES:
        if movie['id'] == id:
            MOVIES.remove(movie)
            return "Filme removido", 200
    return {"error": "Filme não encontrado"}, 404

if __name__ == "__main__":
    app.run(debug=True)
