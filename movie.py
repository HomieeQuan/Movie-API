from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()

# Example external API endpoint for OMDB
OMDB_API_URL = 'http://www.omdbapi.com/'

@app.get("/api/movie/{title}")
def get_movie_info(title: str):
    try:
        api_key = os.getenv('KEY')  # Retrieving API key from environment variable
        params = {
            'apikey': api_key,
            't': title
        }
        
        response = requests.get(OMDB_API_URL, params=params)
        response.raise_for_status()  # Raise exception for 4xx and 5xx errors
        data = response.json()
        
        # Extracting specific fields
        movie_name = data.get('Title')
        movie_year = data.get('Year')
        
        if not movie_name or not movie_year:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        return {"title": movie_name, "year": movie_year}
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data: {str(e)}")





