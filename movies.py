from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field, validator
from typin import Optional, List

app = FastAPI()
movies_db: List[Moies] = []

class Movie(BaseModel):
    id: int
    title: str = Field(..., min_lenght = 2)
    genre: Optional[str] = 'Unknown'
    year: int
    rating: float = Field(..., ge = 0.0, le = 10.0)

    @validator('year')
    def validate_year(cls, v):
        if v <= 1888:
            raise ValueError('Year must be greater than 1888')
        return v

@app.post('/movies/', response_model = Movie)
def add_movie(movie: Movie):
    movies_db.append(movie)
    return movie

@app.get('/movies/',response_model = List[Movie])
def list_movies(
    genre: Optional[str] = None,
    min_rating: Optional[int] = None,
    from_year: Optional[int] = None,
    to_year: Optional[int] = None,
):
    result = movies_db
    if genre:
        result = [m for m in result if m.genre.lower() == genre.lower()]
    if min_rating:
        result = [m for m in result if m.rating >= min_rating]
    if from_year:
        result = [m for m in result if m.year >= from_year]
    if to_year:
        result = [m for m in result if m.year <= to_year]
    return result

@app.get('/movies/',response_model = List[Movie])
def list_movies(
    skip: int = 0,
    limit: int = 0,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = 'asc'
):
    result = movies_db[skip: skip + limit]
    if sort_by in {'title', 'year', 'rating'}:
        reverse = sort_order == 'desc'
        result.sort(key = lambda m: getattr(m, sort_by), reverse = reverse)
    return result

@app.get('/movies/{movie_id}', response_model = Movie) 
def get_movie(movie_id:int):
    for movie in movies_db:
        if movie.id == movie_id:
            return movie
    raise HTTPException(status_code = 404, detail = 'Movie not found')

@app.put('/movies/{movie_id}', response_model = Movie)
def update_movie(movie_id: int, updated: Movie):
    for i, movie in enumerate(movies_db):
        if movie.id == movie_id:
            movies_db[i] = updated
            return updated
    raise HTTPException(status_code = 404, detail = 'Movie not found')

@app.delete('/movies/{movie_id}')    
def delete_movie(movie_id:int):
    for i, movie in enumerate(movies_db):
        if movie.id == movie_id:
            del movies_db[i]
            return {'message': 'Movie deleted'}
    raise HTTPException(status_code = 404, detail = 'Movie not found')

@app.post('/movies/bulk', response_model = List[Movie])
def add_movies_bulk(movies: List[Movie]):
    movies_db.extend(movies)
    return movies

@app.delete('/movies/bulk/')
def delete_movies_bulk(ids:List[int]):
    global movies_db
    movies_db = [m for m in movies.db if m.id not in ids]
    return {'message': 'Movies deleted'}

@app.get('/movies/search/', response_model = List[Movie])
def search_movies(q: str):
    return [m for m in movies_db if q.lower() in m.title.lower]







































































































