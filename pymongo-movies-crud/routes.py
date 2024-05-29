from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from  fastapi.encoders import jsonable_encoder
from typing import List

from models import Movie, MovieUpdate
#added
from neo4j import GraphDatabase
from neo4j_functions import get_common_movie_count, get_users_who_rated_movie, get_user_ratings


router = APIRouter()
collectionName = "movies" #to change the mongodb database


#On affiche une liste de tous les films de la base de données
@router.get("/",response_description="List all movies",response_model=List[Movie])
def list_movies(request: Request):
    #on indique une limite à 150 pour qu'il n'y ait pas trop de films affichés d'un coup
    movies = list(request.app.database[collectionName].find(limit=150)) #here's where we change the database
    for movie in movies:
        movie["_id"] = str(movie["_id"])  
    return jsonable_encoder(movies)



#on obtient un film en focntion de son titre ou du nom d'un de ses acteurs
@router.get("/{parameter}", response_description="Get a movie by title or actor's name", response_model=List[Movie])
def find_movie(parameter: str, request: Request):
    movies_by_title = list(request.app.database[collectionName].find({"title": parameter}))#films par titres
    print(f"Movies found by title '{parameter}': {movies_by_title}")  # Debugging line
    #movies_by_actor = list(request.app.database[collectionName].find({"actors": parameter}))#films par acteurs
    movies_by_actor = list(request.app.database[collectionName].find({"cast": {"$in": [parameter]}}))
    print(f"Movies found by actor '{parameter}': {movies_by_actor}")  # Debugging line


    #on fait un lien
    for movie in movies_by_title + movies_by_actor: 
        movie["_id"] = str(movie["_id"])

    #on retourne ou un film en fonction de son titre ou en fonction du nom d'un acteur
    if movies_by_title:
        return jsonable_encoder(movies_by_title)
    elif movies_by_actor:
        return jsonable_encoder(movies_by_actor)

    raise HTTPException(status_code=404, detail=f"No movies found with parameter '{parameter}'")


#on met � jour les informations d'un film en fonction de son titre
@router.put("/{title}", response_description="Update a movie by title", response_model=Movie)
def update_movie_by_title(title: str, request: Request, movie_update: MovieUpdate):
    movie = request.app.database[collectionName].find_one({"title": title})
    
    if not movie:
        raise HTTPException(status_code=404, detail=f"No movie found with title '{title}'")
    
    #movie_update.dict(exclude_unset=True): This method generates a dictionary of the update fields excluding those that are unset.
    movie_data = movie_update.dict(exclude_unset=True)
    updated_movie = request.app.database[collectionName].find_one_and_update(
        {"title": title}, 
        #{"$set": jsonable_encoder(movie_data)}: The update operation, using $set to update only the specified fields.
        # jsonable_encoder(movie_data): Encodes the movie_data to a format suitable for MongoDB.
        {"$set": jsonable_encoder(movie_data)}, 
        return_document=True
    )
    #Converts the _id field of the updated movie document to a string for consistency in the response format.
    updated_movie["_id"] = str(updated_movie["_id"])
    updated_movie["released"] = str(updated_movie["released"]) #added #it work, don't know why

    return updated_movie

#return the number of movies common between mongoDB database &neo4j database (mongoDB & neo4j)
@router.get("/common/movies/count", response_description="Get number of common movies between MongoDB and Neo4j")
def common_movies_count(request: Request):
    mongo_movies = list(request.app.database[collectionName].find({}, {"title": 1}))
    mongo_titles = [movie["title"] for movie in mongo_movies]

    # Get common movie count and common titles from Neo4j
    common_count, common_titles = get_common_movie_count(mongo_titles, request.app.neo4j_driver)

    # Print common movie titles
    print("Common Movie Titles:")
    for title in common_titles:
        print(title)
    return {"common_movies_count": common_count}

#list users who rated a movie - the name of the movie is given inparameter (neo4j)
@router.get("/movie/{title}/users", response_description="List users who rated a movie")
def users_who_rated_movie(title: str, request: Request):
    users = get_users_who_rated_movie(title, request.app.neo4j_driver)
    if not users:
        raise HTTPException(status_code=404, detail=f"No users found who rated movie '{title}'")
    return users

#return a user with the number of movies he has rated and the list of rated movies - the name of the user is given in parameter (neo4j)
@router.get("/user/{name}/ratings", response_description="Get a user with the number of movies he has rated and the list of rated movies")
def user_ratings(name: str, request: Request):
    user_ratings = get_user_ratings(name, request.app.neo4j_driver)
    if not user_ratings["rated_movies"]:
        raise HTTPException(status_code=404, detail=f"No ratings found for user '{name}'")
    return user_ratings
