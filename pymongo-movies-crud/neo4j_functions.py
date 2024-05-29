from neo4j import GraphDatabase
from typing import List, Dict

def get_common_movie_count(mongo_movies: List[str], neo4j_driver: GraphDatabase) -> int:
    common_titles = [] #added
    
    with neo4j_driver.session() as session:
        result = session.run(
            """
            MATCH (m:Movie)
            WHERE m.title IN $titles
            RETURN m.title as title
            """,
            titles=mongo_movies
        )
        common_titles = [record["title"] for record in result]

    common_count = len(common_titles)
    return common_count, common_titles

def get_users_who_rated_movie(movie_title: str, neo4j_driver: GraphDatabase) -> List[str]:
    with neo4j_driver.session() as session:
        result = session.run(
            """
            MATCH (a:Person)-[rel]->(m:Movie {title: $title})
            WHERE rel.rating IS NOT NULL
            RETURN a.name as name
            """, {"title": movie_title}
        )

        # Extract and print user names
        user_names = [record["name"] for record in result]
        print("Users who rated the movie:")
        for name in user_names:
            print(name)
        
        return user_names
        #older verion
        #return [record["name"] for record in result]

#return a user with the number of movies he has rated and the list of rated movies - the name of the user is given in parameter (neo4j)
def get_user_ratings(user_name: str, neo4j_driver: GraphDatabase) -> Dict[str, List[str]]:

     with neo4j_driver.session() as session:
        result = session.run(
            """
            MATCH (a:Person {name: $name})-[rel]->(m:Movie)
            WHERE rel.rating IS NOT NULL
            RETURN count(m) as rated_count, collect(m.title) as rated_movies
            """, {"name": user_name}
        )
        
        # Extract the results
        record = result.single()
        rated_count = record["rated_count"]
        rated_movies = record["rated_movies"]
        
        # Debugging output
        print(f"User {user_name} has rated {rated_count} movies:")
        for title in rated_movies:
            print(title)
        
        return {"name": user_name, "rated_count": rated_count, "rated_movies": rated_movies}
