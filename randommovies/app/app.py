from flask import Flask, jsonify, request
from flask_cors import CORS
from movies import MovieManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
movie_manager = MovieManager()

@app.route('/')
def home():
    """Home endpoint with API information"""
    all_ids = movie_manager.get_all_movie_ids()
    return jsonify({
        "message": "Movie API",
        "endpoints": {
            "/random-movie": "GET - Get a random movie",
            "/random-movies/<int:n>": "GET - Get N random movies",
            "/top-movies/<int:n>": "GET - Get top N movies by rating",
            "/random-movies": "GET - Get random movies with query parameter ?n=5",
            "/movie/<int:movie_id>": "GET - Get a specific movie by ID",
            "/movies": "GET - Get all available movie IDs"
        },
        "total_movies": movie_manager.get_movie_count(),
        "available_movie_ids": all_ids
    })

@app.route('/random-movie', methods=['GET'])
def random_movie():
    """Get a single random movie"""
    try:
        movie = movie_manager.get_random_movie()
        if not movie:
            return jsonify({"error": "No movies available"}), 404
        
        logger.info(f"Returning random movie: {movie.get('title', 'Unknown')}")
        return jsonify(movie)
    
    except Exception as e:
        logger.error(f"Error in random_movie: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/random-movies', methods=['GET'])
@app.route('/random-movies/<int:n>', methods=['GET'])
def random_n_movies(n=None):
    """Get N random movies"""
    try:
        # Get n from query parameter or route parameter
        if n is None:
            n = request.args.get('n', default=5, type=int)
        
        if n <= 0:
            return jsonify({"error": "Parameter 'n' must be positive"}), 400
        
        movies = movie_manager.get_random_movies(n)
        
        logger.info(f"Returning {len(movies)} random movies")
        return jsonify({
            "count": len(movies),
            "movies": movies
        })
    
    except Exception as e:
        logger.error(f"Error in random_n_movies: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/top-movies', methods=['GET'])
@app.route('/top-movies/<int:n>', methods=['GET'])
def top_n_movies(n=None):
    """Get top N movies by rating"""
    try:
        # Get n from query parameter or route parameter
        if n is None:
            n = request.args.get('n', default=5, type=int)
        
        if n <= 0:
            return jsonify({"error": "Parameter 'n' must be positive"}), 400
        
        movies = movie_manager.get_top_movies(n)
        
        logger.info(f"Returning top {len(movies)} movies by rating")
        return jsonify({
            "count": len(movies),
            "movies": movies
        })
    
    except Exception as e:
        logger.error(f"Error in top_n_movies: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/movies', methods=['GET'])
def get_all_movie_ids():
    """Get all available movie IDs"""
    try:
        movie_ids = movie_manager.get_all_movie_ids()
        logger.info(f"Returning {len(movie_ids)} movie IDs")
        return jsonify({
            "total_movie_ids": len(movie_ids),
            "movie_ids": movie_ids
        })
    
    except Exception as e:
        logger.error(f"Error in get_all_movie_ids: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/movie/<movie_id>', methods=['GET'])
def get_movie_by_id(movie_id=None):
    """Get a specific movie by ID"""
    try:
        logger.info(f"Request for movie with ID: {movie_id}")
        
        movie = movie_manager.get_movie_by_id(movie_id)
        
        if not movie:
            return jsonify({
                "error": f"Movie with ID {movie_id} not found",
                "available_ids": movie_manager.get_all_movie_ids()
            }), 404
        
        logger.info(f"Returning movie: {movie.get('title', 'Unknown')} (ID: {movie_id})")
        return jsonify(movie)
    
    except Exception as e:
        logger.error(f"Error in get_movie_by_id: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)