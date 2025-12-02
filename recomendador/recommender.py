"""[TADW 2025] - Sistemas de recomendación"""

import pandas as pd
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
import warnings

warnings.filterwarnings('ignore')

class Recommender:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.client = None
        self.movies = None
        self.cosine_sim = None
        self.indices = None
        self.id_to_title = None # Map _id to title for quick lookup

    def connect_to_mongodb(self):
        """Connect to MongoDB and return database client."""
        try:
            self.client = MongoClient(self.connection_string)
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
            return True
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
            return False

    def load_mflix_data(self, database_name="sample_mflix"):
        """Load movies data from MFlix database."""
        if not self.client:
            print("MongoDB client not connected.")
            return pd.DataFrame()
        
        db = self.client[database_name]
        movies_collection = db.movies
        
        movies_data = list(movies_collection.find(
            {
                "title": {"$exists": True},
                "imdb.rating": {"$exists": True, "$ne": ""},
                "imdb.votes": {"$exists": True, "$ne": ""},
                "genres": {"$exists": True, "$ne": []},
                "cast": {"$exists": True, "$ne": []}
            },
            {
                "_id": 1, # Include _id
                "title": 1,
                "year": 1,
                "genres": 1,
                "cast": 1,
                "directors": 1,
                "writers": 1,
                "plot": 1,
                "fullplot": 1,
                "imdb.rating": 1,
                "imdb.votes": 1,
                "tomatoes.viewer.rating": 1,
                "tomatoes.viewer.numReviews": 1,
                "awards": 1,
                "languages": 1,
                "countries": 1,
                "type": 1,
                "runtime": 1,
                "poster": 1,
            }
        ))
        
        return pd.DataFrame(movies_data)

    def clean_mflix_data(self, df):
        """Clean and prepare MFlix movies data."""
        df_clean = df.copy()
        
        # Flatten imdb fields
        df_clean['imdb_rating'] = df_clean['imdb'].apply(lambda x: x.get('rating') if isinstance(x, dict) else None)
        df_clean['imdb_votes'] = df_clean['imdb'].apply(lambda x: x.get('votes') if isinstance(x, dict) else None)
        
        # Process ratings
        df_clean['average_rating'] = pd.to_numeric(df_clean['imdb_rating'], errors='coerce').fillna(0)
        df_clean['ratings_count'] = pd.to_numeric(df_clean['imdb_votes'], errors='coerce').fillna(0)
        
        if 'tomatoes.viewer.rating' in df_clean.columns:
            df_clean['tomato_rating'] = pd.to_numeric(df_clean['tomatoes.viewer.rating'], errors='coerce')
            df_clean['tomato_count'] = pd.to_numeric(df_clean['tomatoes.viewer.numReviews'], errors='coerce')
        
        # Process list fields
        df_clean['genres_str'] = df_clean['genres'].apply(
            lambda x: ', '.join(x) if isinstance(x, list) else ''
        )
        df_clean['cast_str'] = df_clean['cast'].apply(
            lambda x: ', '.join(x[:5]) if isinstance(x, list) and len(x) > 0 else ''
        )
        df_clean['directors_clean'] = df_clean['directors'].apply(
            lambda x: ', '.join(str.lower(i.replace(" ", "")) for i in x) if isinstance(x, list) else ''
        )
        df_clean['title_clean'] = df_clean['title'].astype(str)
        
        # Filter valid movies
        df_clean = df_clean[df_clean['ratings_count'] > 0]
        df_clean = df_clean[df_clean['genres_str'].str.strip() != '']
        
        return df_clean

    def calculate_weighted_ratings(self, movies, percentile=0.95):
        """Calculate weighted ratings for all movies."""
        v = movies['ratings_count']
        m = movies['ratings_count'].quantile(percentile)
        R = movies['average_rating']
        C = movies['average_rating'].mean()
        movies['weighted_rating'] = (R * v + C * m) / (v + m)
        return movies

    def create_soup(self, movies):
        """Create soup combining title, directors, and genres."""
        movies['soup'] = movies.apply(
            lambda x: ' '.join([str(x['title_clean']), str(x['directors_clean'] or ''), str(x['genres_str'] or '')]),
            axis=1
        )
        return movies

    def build_similarity_matrix(self, movies):
        """Build cosine similarity matrix."""
        count = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0.0, stop_words='english')
        count_matrix = count.fit_transform(movies['soup'])
        return cosine_similarity(count_matrix, count_matrix)

    def train(self):
        """Initialize the recommender system (load data, build matrices)."""
        if not self.connect_to_mongodb():
            raise Exception("Failed to connect to MongoDB")

        print("Loading data...")
        movies_df = self.load_mflix_data()
        if movies_df.empty:
            raise Exception("No movies loaded from MongoDB.")
        print(f"Loaded {len(movies_df)} movies from MongoDB")
        
        print("Cleaning data...")
        self.movies = self.clean_mflix_data(movies_df)
        print(f"Cleaned to {len(self.movies)} movies")
        
        print("Calculating weighted ratings...")
        self.movies = self.calculate_weighted_ratings(self.movies)
        
        print("Building similarity matrix...")
        self.movies = self.create_soup(self.movies)
        self.cosine_sim = self.build_similarity_matrix(self.movies)
        
        self.indices = pd.Series(self.movies.index, index=self.movies['title'])
        # Create a map from _id to title for easy lookup
        self.id_to_title = {str(row['_id']): row['title'] for _, row in self.movies.iterrows()}
        
        print("Recommender training complete.")

    def get_movie_index(self, title):
        """Get movie index by title or find most similar."""
        try:
            return self.indices[title]
        except KeyError:
            # If exact title not found, try to find a close match or handle gracefully
            # For simplicity, returning None for now. A more robust solution would involve fuzzy matching.
            print(f"Movie title '{title}' not found in index.")
            return None

    def get_recommendations(self, title, n=10, self_exclude=True):
        """Get hybrid recommendations combining similarity and rating."""
        idx = self.get_movie_index(title)
        if idx is None:
            return pd.DataFrame() # Return empty if title not found
        
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:n+1] if self_exclude else sim_scores[0:n+1]
        
        movie_indices = [i[0] for i in sim_scores]
        cosine_similarities = [i[1] for i in sim_scores]
        
        # Ensure 'average_rating' is numeric before multiplication
        ratings = pd.to_numeric(self.movies['average_rating'].iloc[movie_indices], errors='coerce').fillna(0).values
        
        hybrid_scores = [cos_sim * rating for cos_sim, rating in zip(cosine_similarities, ratings)]
        
        recommended_movies = self.movies.iloc[movie_indices].copy()
        recommended_movies['sim_score'] = cosine_similarities
        recommended_movies['hybrid_score'] = hybrid_scores
        
        return recommended_movies.sort_values('hybrid_score', ascending=False)

    def get_movie_title_by_id(self, movie_id):
        """Helper to get movie title by its MongoDB _id."""
        return self.id_to_title.get(str(movie_id))

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    DATABASE_CONN_STRING = os.environ.get("DATABASE_CONN_STRING") or "mongodb://admin:12345@localhost:27017/sample_mflix?authSource=admin"
    
    recommender = Recommender(DATABASE_CONN_STRING)
    try:
        recommender.train()
    except Exception as e:
        print(f"Error during recommender initialization: {e}")
        exit(1)
    
    # Display top movies (using the trained data)
    top_movies = recommender.movies.sort_values('weighted_rating', ascending=False).head(15)
    print("\nTop 15 movies by weighted rating:")
    print(top_movies[['title_clean', 'directors_clean', 'average_rating', 'ratings_count', 'weighted_rating']])
    
    # Get recommendations
    print("\nRecommendations for 'The Godfather':")
    recommendations = recommender.get_recommendations("The Godfather")
    if not recommendations.empty:
        print(recommendations[['title', 'average_rating', 'sim_score', 'hybrid_score']].head(10))
    else:
        print("No recommendations found for 'The Godfather'.")

    jaws_recommendations = recommender.get_recommendations("Jaws")
    if not jaws_recommendations.empty:
        print(f"\n Recommendations for 'Jaws':\n {jaws_recommendations[['title', 'average_rating', 'sim_score', 'hybrid_score']].head(10)}")
    else:
        print("No recommendations found for 'Jaws'.")

    # Example of using get_movie_title_by_id
    if not recommender.movies.empty:
        first_movie_id = recommender.movies.iloc[0]['_id']
        first_movie_title = recommender.get_movie_title_by_id(first_movie_id)
        print(f"\nTitle for movie ID {first_movie_id}: {first_movie_title}")