import uuid
from typing import Optional,Dict,List,Union
from pydantic import BaseModel, Field,validator
from datetime import datetime


class Movie(BaseModel):
    id: str = Field(..., alias="_id")    
    plot: Optional[str] = Field(None)
    fullplot: Optional[str] = Field(None)  
    genres: List[str] = Field(default_factory=list)  
    runtime: Optional[int] = Field(None)  
    cast: List[str] = Field(default_factory=list) 
    num_mflix_comments: Optional[int]=Field(None)

    poster: Optional[str] = Field(None)  
    title: str = Field(...)
    #On utilise le format "datetime" pour les dates
    lastupdated: Optional[datetime] = Field(None)  
    languages: List[str] = Field(default_factory=list)  
    
    released: Optional[str] = Field(None)  #modified to optional and also None 
    directors: List[str] = Field(default_factory=list) 
    writers: List[str] = Field(default_factory=list) 
    rated: Optional[str] = Field(None)  
    awards: Optional[Dict[str, Union[str, int]]] = Field(default_factory=dict) 
    year: Optional[int] = Field(None)
    imdb: Optional[Dict[str, Union[float, int]]] = Field(default_factory=dict)  
    countries: List[str] = Field(default_factory=list)
    type: str = Field(...)
    tomatoes: Optional[Dict[str, Union[dict, str, datetime]]] = Field(default_factory=dict)


class MovieUpdate(BaseModel):
    plot: Optional[str] = None
    fullplot: Optional[str] = Field(None)  #added
    genres: List[str] = Field(default_factory=list)
    runtime: Optional[int] = None
    cast: List[str] = Field(default_factory=list)
    num_mflix_comments: Optional[int] = None #second second try #it seems to have worked
    poster: Optional[str] = Field(None) #added
    lastupdated: Optional[datetime] =None  
    languages: List[str] = Field(default_factory=list) 

    directors: List[str] = Field(default_factory=list) 
    writers: List[str] = Field(default_factory=list) #added

    rated: Optional[str] = None
    awards: Optional[Dict[str, Union[str, int]]] = None 
    year: Optional[int] = Field(None) #added
    
    imdb: Optional[Dict[str, Union[float, int]]] = Field(default_factory=dict) #added
    countries: List[str] = Field(default_factory=list)
    tomatoes: Optional[Dict[str, Union[dict, str, datetime]]] = Field(default_factory=dict) #added
    
    