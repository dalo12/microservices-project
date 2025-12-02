from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from pymongo import MongoClient
from recommender import Recommender
import pandas as pd

app = FastAPI(title="Recommender Microservice")

# Environment variables
# Connection string for sample_mflix (movies data)
MOVIES_DB_CONN_STRING = os.environ.get("DATABASE_CONN_STRING") or "mongodb://admin:12345@localhost:27017/sample_mflix?authSource=admin"
# Connection string for ratings_db (user ratings) - defaulting to same cluster but different DB if not specified
RATINGS_DB_CONN_STRING = os.environ.get("RATINGS_DB_CONN_STRING") or "mongodb://admin:12345@localhost:27017/ratings_db?authSource=admin"

# Global recommender instance
recommender = Recommender(MOVIES_DB_CONN_STRING)

@app.on_event("startup")
def startup_event():
    print("Initializing Recommender System...")
    try:
        recommender.train()
        print("Recommender System Initialized.")
    except Exception as e:
        print(f"Failed to initialize Recommender: {e}")
        # We might want to exit here if recommender is critical, but for now let's just log it.

def get_user_ratings(email: str):
    try:
        client = MongoClient(RATINGS_DB_CONN_STRING)
        db = client.get_database("ratings_db") # Force database name if not in connection string
        ratings_collection = db.ratings
        # Find ratings by email, sort by rating (desc) and timestamp (desc)
        user_ratings = list(ratings_collection.find({"email": email}).sort([("rating", -1), ("timestamp", -1)]))
        return user_ratings
    except Exception as e:
        print(f"Error fetching user ratings: {e}")
        return []

@app.get("/recommend/{email}", response_model=List[Dict[str, Any]])
def recommend_movies(email: str):
    """
    Recommend movies for a user based on their ratings.
    """
    if not recommender.movies is not None and not recommender.movies.empty:
         raise HTTPException(status_code=503, detail="Recommender system not initialized or empty data.")

    user_ratings = get_user_ratings(email)
    
    if not user_ratings:
        # User has no ratings, return top movies
        print(f"No ratings found for {email}. Returning top movies.")
        top_movies = recommender.movies.sort_values('weighted_rating', ascending=False).head(10)
        recommendations = top_movies
    else:
        # User has ratings. Pick the best one to base recommendations on.
        # We'll try to find a movie ID that exists in our loaded movies dataset.
        seed_movie = None
        for rating in user_ratings:
            movie_id = rating.get("movieId")
            movie_title = recommender.get_movie_title_by_id(movie_id)
            if movie_title:
                seed_movie = movie_title
                print(f"Found seed movie for recommendation: {seed_movie} (ID: {movie_id})")
                break
        
        if seed_movie:
            recommendations = recommender.get_recommendations(seed_movie, n=10)
        else:
            # If we couldn't map any rated movie ID to a title, fallback to top movies
            print(f"Could not map any rated movies to titles for {email}. Returning top movies.")
            recommendations = recommender.movies.sort_values('weighted_rating', ascending=False).head(10)

    if recommendations.empty:
        return []

    # Format response
    results = []
    for _, row in recommendations.iterrows():
        item = row.to_dict()
        # Convert ObjectId to string
        if '_id' in item:
            item['_id'] = str(item['_id'])
        
        # Handle NaN values for JSON serialization
        clean_item = {}
        for k, v in item.items():
            if pd.isna(v):
                clean_item[k] = None
            else:
                clean_item[k] = v
        results.append(clean_item)
        
    return results

@app.get("/health")
def health_check():
    return {"status": "healthy", "recommender_initialized": recommender.movies is not None and not recommender.movies.empty}
