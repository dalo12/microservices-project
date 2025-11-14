import json
import random
from typing import List, Dict, Any
import os

class MovieManager:
    def __init__(self):
        self.movies = self._load_movies()
    
    def _load_movies(self) -> List[Dict[str, Any]]:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_file = os.path.join(current_dir, 'data', 'movies.json')
        """Load movies from JSON file"""
        try:
            with open(data_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Warning: {data_file} not found. Using empty movie list.")
            return []
        except json.JSONDecodeError:
            print(f"Error: {data_file} contains invalid JSON.")
            return []
    
    def get_random_movies(self, n: int = 5) -> List[Dict[str, Any]]:
        """Get N random movies"""
        if n <= 0:
            return []
        n = min(n, len(self.movies))
        return random.sample(self.movies, n)
    
    def get_random_movie(self) -> Dict[str, Any]:
        """Get a single random movie"""
        return random.choice(self.movies) if self.movies else {}
    
    def get_top_movies(self, n: int = 5) -> List[Dict[str, Any]]:
        """Get top N movies based on rating"""
        if n <= 0:
            return []
        sorted_movies = sorted(self.movies, key=lambda x: x.get('rating', 0), reverse=True)
        n = min(n, len(sorted_movies))
        return sorted_movies[:n]
    
    def get_movie_count(self) -> int:
        """Get total number of movies"""
        return len(self.movies)