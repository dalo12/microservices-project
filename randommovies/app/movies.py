import json
import random
from typing import List, Dict, Any, Optional
import os
import requests

apiUrl = os.environ.get('MOVIES_URL') or "http://127.0.0.1:4000/graphql"
ALL_FIELDS = """
    _id
    plot
    genres
    runtime
    cast
    poster
    title
    fullplot
    languages
    released
    directors
    rated
    awards {
        wins
        nominations
        text
    } 
    year
    imdb {
        id
        rating
        votes
    }
    countries
    type
    tomatoes {
        lastUpdated
        viewer {
            rating
            numReviews
            meter
        } 
        critic {
            rating
            numReviews
            meter
        }
    }
    num_mflix_comments
"""

class MovieManager:
    def _fetch_movies_from_api(self, limit: int = 100, skip: int = 0) -> List[Dict[str, Any]]:
        """Fetch movies from GraphQL API with pagination"""
        if not apiUrl:
            print("Warning: MOVIES_URL environment variable not set.")
            return []
        
        query = """
        query($limit: Int!, $skip: Int!) {
            films(limit: $limit, skip: $skip) {
                ALL_FIELDS
            }
        }
        """.replace("ALL_FIELDS", ALL_FIELDS)
        
        try:
            response = requests.post(apiUrl, json={
                "query": query,
                "variables": {"limit": limit, "skip": skip}
            })
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                print(f"GraphQL Error: {data['errors']}")
                return []
            
            return data.get("data", {}).get("films", [])
        except requests.RequestException as e:
            print(f"Error fetching movies from API: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error loading movies: {e}")
            return []
    
    def _get_total_movie_count(self) -> int:
        """Get total count of movies in database"""
        if not apiUrl:
            return 0
        
        query = """
        query {
            films(limit: 100){
                ALL_FIELDS
            }
        }
        """.replace("ALL_FIELDS", ALL_FIELDS)
        
        try:
            response = requests.post(apiUrl, json={"query": query})
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                print(f"GraphQL Error: {data['errors']}")
                return 0
            
            films = data.get("data", {}).get("films", [])
            
            return len(films)
        except Exception as e:
            print(f"Error fetching movie count: {e}")
            return 0
    
    def _fetch_all_movies(self) -> List[Dict[str, Any]]:
        """Fetch all movies from database with pagination"""
        all_movies = []
        total_count = self._get_total_movie_count()
        
        if total_count == 0:
            return []
        
        batch_size = 100
        skip = 0
        
        while skip < total_count:
            movies = self._fetch_movies_from_api(limit=batch_size, skip=skip)
            if not movies:
                break
            all_movies.extend(movies)
            skip += batch_size
        
        return all_movies
    
    def get_random_movies(self, n: int = 5) -> List[Dict[str, Any]]:
        """Get N random movies"""
        if n <= 0:
            return []
        
        movies = self._fetch_all_movies()
        n = min(n, len(movies))
        return random.sample(movies, n) if movies else []
    
    def get_random_movie(self) -> Dict[str, Any]:
        """Get a single random movie"""
        movies = self._fetch_all_movies()
        return random.choice(movies) if movies else {}
    
    def get_top_movies(self, n: int = 5) -> List[Dict[str, Any]]:
        """Get top N movies based on rating"""
        if n <= 0:
            return []
        
        movies = self._fetch_all_movies()
        
        # Filter out movies without a rating
        movies_with_rating = [
            movie for movie in movies 
            if movie.get('imdb', {}).get('rating') is not None
        ]
        
        # Sort by rating in descending order
        sorted_movies = sorted(
            movies_with_rating, 
            key=lambda x: x.get('imdb', {}).get('rating', 0), 
            reverse=True
        )
        
        n = min(n, len(sorted_movies))
        return sorted_movies[:n]
    
    def get_movie_count(self) -> int:
        """Get total number of movies in database"""
        return self._get_total_movie_count()
    
    def get_movie_by_id(self, movie_id: str) -> Optional[Dict[str, Any]]:
        """Get a movie by its MongoDB _id"""
        if not apiUrl:
            return None
        
        query = """
        query($id: String!) {
            film(id: $id) {
                ALL_FIELDS
            }
        }
        """.replace("ALL_FIELDS", ALL_FIELDS)
        
        try:
            response = requests.post(apiUrl, json={
                "query": query,
                "variables": {"id": movie_id}
            })
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                print(f"GraphQL Error: {data['errors']}")
                return None
            
            return data.get("data", {}).get("movieById", None)
        except Exception as e:
            print(f"Error fetching movie by ID: {e}")
            return None
    
    def get_all_movie_ids(self) -> List[str]:
        """Get list of all available movie IDs"""
        movies = self._fetch_all_movies()
        return [movie.get('_id') for movie in movies if movie.get('_id') is not None]