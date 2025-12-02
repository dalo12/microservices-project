# -*- coding: utf-8 -*-
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

DATABASE_CONN_STRING = os.environ.get("DATABASE_CONN_STRING") or "mongodb://admin:12345@localhost:27017/sample_mflix?authSource=admin"

# ============================================================================
# DATABASE CONNECTION
# ============================================================================

def connect_to_mongodb():
    """Connect to MongoDB and return database client."""
    try:
        client = MongoClient(DATABASE_CONN_STRING)
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        return client
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
        return None

# ============================================================================
# DATA LOADING
# ============================================================================

def load_mflix_data(client, database_name="sample_mflix"):
    """Load movies data from MFlix database."""
    db = client[database_name]
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
            "_id": 0,
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
            "runtime": 1
        }
    ))
    
    return pd.DataFrame(movies_data)

# ============================================================================
# DATA CLEANING & TRANSFORMATION
# ============================================================================

def flatten_imdb_fields(df_clean):
    """Flatten nested imdb fields."""
    df_clean['imdb_rating'] = df_clean['imdb'].apply(lambda x: x.get('rating') if isinstance(x, dict) else None)
    df_clean['imdb_votes'] = df_clean['imdb'].apply(lambda x: x.get('votes') if isinstance(x, dict) else None)
    return df_clean

def process_ratings(df_clean):
    """Process and normalize ratings."""
    df_clean['average_rating'] = pd.to_numeric(df_clean['imdb_rating'], errors='coerce').fillna(0)
    df_clean['ratings_count'] = pd.to_numeric(df_clean['imdb_votes'], errors='coerce').fillna(0)
    
    if 'tomatoes.viewer.rating' in df_clean.columns:
        df_clean['tomato_rating'] = pd.to_numeric(df_clean['tomatoes.viewer.rating'], errors='coerce')
        df_clean['tomato_count'] = pd.to_numeric(df_clean['tomatoes.viewer.numReviews'], errors='coerce')
    
    return df_clean

def process_list_fields(df_clean):
    """Convert list fields to strings."""
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
    
    return df_clean

def filter_valid_movies(df_clean):
    """Remove movies without ratings or genres."""
    df_clean = df_clean[df_clean['ratings_count'] > 0]
    df_clean = df_clean[df_clean['genres_str'].str.strip() != '']
    return df_clean

def clean_mflix_data(df):
    """Clean and prepare MFlix movies data."""
    df_clean = df.copy()
    df_clean = flatten_imdb_fields(df_clean)
    df_clean = process_ratings(df_clean)
    df_clean = process_list_fields(df_clean)
    df_clean = filter_valid_movies(df_clean)
    return df_clean

# ============================================================================
# WEIGHTED RATING CALCULATION
# ============================================================================

def calculate_weighted_ratings(movies, percentile=0.95):
    """Calculate weighted ratings for all movies."""
    v = movies['ratings_count']
    m = movies['ratings_count'].quantile(percentile)
    R = movies['average_rating']
    C = movies['average_rating'].mean()
    movies['weighted_rating'] = (R * v + C * m) / (v + m)
    return movies

def get_top_movies(movies, n=250):
    """Get top N movies by weighted rating."""
    return movies.sort_values('weighted_rating', ascending=False).head(n)

# ============================================================================
# GENRE ANALYSIS
# ============================================================================

def get_genre_distribution(movies, top_n=15):
    """Analyze and get genre distribution."""
    genres_list = movies['genres'].str.split(', ')
    genres_list = genres_list.apply(lambda x: x if isinstance(x, list) else [])
    
    all_genres = sum(genres_list, [])
    genre_counts = pd.DataFrame(Counter(all_genres).items(), columns=['genre', 'count']).sort_values(by='count', ascending=False)
    
    top_genres = genre_counts.head(top_n)
    others_count = genre_counts['count'][top_n:].sum()
    others_df = pd.DataFrame({'genre': ['Others'], 'count': [others_count]})
    
    return pd.concat([top_genres, others_df], ignore_index=True)

def build_chart(data, genre, percentile=0.85):
    """Build weighted rating chart for a specific genre."""
    qualified = data[data['genres_str'].notna() & data['genres_str'].str.lower().str.contains(genre.lower())]
    
    if qualified.empty:
        return None
    
    v = qualified['ratings_count']
    m = qualified['ratings_count'].quantile(percentile)
    R = qualified['average_rating']
    C = qualified['average_rating'].mean()
    qualified['weighted_rating'] = (R * v + C * m) / (v + m)
    
    return qualified.sort_values('weighted_rating', ascending=False)

# ============================================================================
# SIMILARITY & RECOMMENDATIONS
# ============================================================================

def create_soup(movies):
    """Create soup combining title, directors, and genres."""
    movies['soup'] = movies.apply(
        lambda x: ' '.join([str(x['title_clean']), str(x['directors_clean'] or ''), str(x['genres_str'] or '')]),
        axis=1
    )
    return movies

def build_similarity_matrix(movies):
    """Build cosine similarity matrix."""
    count = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0.0, stop_words='english')
    count_matrix = count.fit_transform(movies['soup'])
    return cosine_similarity(count_matrix, count_matrix)

def create_title_index(movies):
    """Create index mapping for movie titles."""
    return pd.Series(movies.index, index=movies['title'])

def get_movie_index(title, indices, cosine_sim):
    """Get movie index by title or find most similar."""
    try:
        return indices[title]
    except KeyError:
        sim_scores = list(enumerate(cosine_sim))
        return max(sim_scores, key=lambda x: max(x[1]))[0]

def get_recommendations(title, indices, cosine_sim, movies, n=10, self_exclude=True):
    """Get content-based recommendations."""
    idx = get_movie_index(title, indices, cosine_sim)
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1] if self_exclude else sim_scores[0:n+1]
    
    movie_indices = [i[0] for i in sim_scores]
    scores = [i[1] for i in sim_scores]
    
    recommended_movies = movies.iloc[movie_indices].copy()
    recommended_movies['sim_score'] = scores
    
    return recommended_movies

def get_recommendations_hybrid(title, indices, cosine_sim, movies, n=10, self_exclude=True):
    """Get hybrid recommendations combining similarity and rating."""
    idx = get_movie_index(title, indices, cosine_sim)
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1] if self_exclude else sim_scores[0:n+1]
    
    movie_indices = [i[0] for i in sim_scores]
    cosine_similarities = [i[1] for i in sim_scores]
    
    rating = movies['average_rating'].iloc[movie_indices].values
    hybrid_scores = [cosine_sim * rating for cosine_sim, rating in zip(cosine_similarities, rating)]
    
    recommended_movies = movies.iloc[movie_indices].copy()
    recommended_movies['sim_score'] = [i[1] for i in sim_scores]
    recommended_movies['hybrid_score'] = hybrid_scores
    
    return recommended_movies.sort_values('hybrid_score', ascending=False)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Connect and load data
    client = connect_to_mongodb()
    if not client:
        exit(1)
    
    movies_df = load_mflix_data(client)
    print(f"Loaded {len(movies_df)} movies from MongoDB")
    
    # Clean and transform data
    movies = clean_mflix_data(movies_df)
    print(f"Cleaned to {len(movies)} movies")
    
    # Calculate weighted ratings
    movies = calculate_weighted_ratings(movies, percentile=0.95)
    
    # Display top movies
    top_movies = get_top_movies(movies, n=15)
    print("\nTop 15 movies by weighted rating:")
    print(top_movies[['title_clean', 'directors_clean', 'average_rating', 'ratings_count', 'weighted_rating']])
    
    # Analyze genres
    genre_distribution = get_genre_distribution(movies)
    print("\nGenre distribution:")
    print(genre_distribution)
    
    # Build biography chart
    biography_chart = build_chart(movies, 'Biography')
    if biography_chart is not None:
        print("\nTop Biography movies:")
        print(biography_chart.head(15)[['title_clean', 'directors_clean', 'genres_str', 'average_rating', 'weighted_rating']])
    
    # Build similarity matrix
    movies = create_soup(movies)
    cosine_sim = build_similarity_matrix(movies)
    indices = create_title_index(movies)
    
    # Get recommendations
    print("\nRecommendations for 'The Godfather':")
    recommendations = get_recommendations_hybrid("The Godfather", indices, cosine_sim, movies)
    print(recommendations[['title', 'average_rating', 'sim_score', 'hybrid_score']].head(10))

    jaws_recommendations = get_recommendations_hybrid("Jaws", indices, cosine_sim, movies)
    print(f"\n Recommendations for 'Jaws':\n {jaws_recommendations[['title', 'average_rating', 'sim_score', 'hybrid_score']].head(10)}")