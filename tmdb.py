import requests
import json
import os
TMDb_API_KEY=os.environ.get('TMDB_API_KEY')
url='https://api.themoviedb.org/3/'

def getTMDbMovieID(movieName):
    movieName=movieName.replace(' ','+')
    response=requests.get(url+'search/movie?api_key='+TMDb_API_KEY+'&query='+movieName)
    res=json.loads(response.text)
    result=res['results']
    id=result[0]['id']
    return id
def getTMDbPersonid(actorName):
    actorName=actorName.replace(' ','+')
    response=requests.get(url+'search/person?api_key='+TMDb_API_KEY+'&language=en-US&query='+actorName+'&page=1')
    print(url+'search/person?api_key='+TMDb_API_KEY+'&language=en-US&query='+actorName+'&page=1&include_adult=True')
    res=json.loads(response.text)
    id=res['results'][0]['id']
    return id

def getBio(actorName):
    actorName=actorName.replace(' ','+')
    id=getTMDbPersonid(actorName)
    response=requests.get(url+'person/'+str(id)+'?api_key='+TMDb_API_KEY+'&language=en-US')
    response=json.loads(response.text)
    bio=response['biography']
    bio=bio.replace('\n','')
    return bio

def movieCredits(actorName):
    try:
        movies=[]
        actorName=actorName.replace(' ','+')
        response=requests.get(url+'search/person?api_key='+TMDb_API_KEY+'&language=en-US&query='+actorName+'&page=1')
        print(url+'search/person?api_key='+TMDb_API_KEY+'&language=en-US&query='+actorName+'&page=1&include_adult=True')
        res=json.loads(response.text)
        known_for=res['results'][0]['known_for']
        for data in known_for:
            movies.append(data['original_title'])
        return movies
    except Exception as e:
        print(e)
