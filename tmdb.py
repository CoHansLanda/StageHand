import requests
import json
import os
TMDb_API_KEY=os.environ.get('TMDB_API_KEY')
url='https://api.themoviedb.org/3/'

def getTMDbMovieID(movieName):
    response=requests.get(url+'search/movie?api_key='+str(TMDb_API_KEY)+'&query='+movieName)
    if(response.status_code==200):
        res=json.loads(response.text)
        result=res['results']
        id=result[0]['id']
        return str(id)
    else:
        print('Wrong status code:'+response.status_code)
def getTMDbPersonid(actorName):
    actorName=actorName.replace(' ','+')
    response=requests.get(url+'search/person?api_key='+TMDb_API_KEY+'&language=en-US&query='+actorName+'&page=1')
    if(response.status_code==200):
        print(url+'search/person?api_key='+TMDb_API_KEY+'&language=en-US&query='+actorName+'&page=1&include_adult=True')
        res=json.loads(response.text)
        id=res['results'][0]['id']
        return id
    else:
        print('Wrong status code:'+response.status_code)


def getBio(actorName):
    actorName=actorName.replace(' ','+')
    id=getTMDbPersonid(actorName)
    response=requests.get(url+'person/'+str(id)+'?api_key='+TMDb_API_KEY+'&language=en-US')
    if(response.status_code==200):
        response=json.loads(response.text)
        bio=response['biography']
        bio=bio.replace('\n','')
        return bio
    else:
        print('Wrong status code:'+response.status_code)

def movieCredits(actorName):
    try:
        movies=[]
        actorName=actorName.replace(' ','+')
        response=requests.get(url+'search/person?api_key='+TMDb_API_KEY+'&language=en-US&query='+actorName+'&page=1')
        if(response.status_code==200):
            print(url+'search/person?api_key='+TMDb_API_KEY+'&language=en-US&query='+actorName+'&page=1&include_adult=True')
            res=json.loads(response.text)
            known_for=res['results'][0]['known_for']
            for data in known_for:
                movies.append(data['original_title'])
            return movies
        else:
            print('Wrong status code:'+response.status_code)
    except Exception as e:
        print(e)

def getMovieSummary(movieName):
    try:
        movieName=movieName.replace(' ','+')
        response=requests.get(url+'search/movie?api_key='+TMDb_API_KEY+'&query='+movieName)
        if(response.status_code==200):
            res=json.loads(response.text)
            summary=res['results'][0]['overview']
            return summary
        else:
            print('Wrong status code:'+response.status_code)
    except Exception as e:
        print(e)

def getMovieRuntime(movieName):
    try:
        id=getTMDbMovieID(movieName)
        response=requests.get(url+'/movie/'+id+'?api_key='+TMDb_API_KEY+'&language=en-US')
        if(response.status_code==200):
            res=json.loads(response.text)
            runtime=res['runtime']
            return int(runtime)
        else:
            print('Wrong Status code'+str(response.status_code))
            raise Exception
    except Exception as e:
        print('Exception')
        print(e)

def getMovieInfo(movieName):
    print(movieName)
    try:
        movieName=movieName.replace(' ','+')
        id=getTMDbMovieID(movieName)
        response=requests.get(url+'/movie/'+id+'?api_key='+TMDb_API_KEY+'&language=en-US')
        if(response.status_code==200):
            res=json.loads(response.text)
            genres=res['genres']
            runtime=res['runtime']
            tagline=res['tagline']
            popularity=res['popularity']
            ratings=res['vote_average']
            dump={
                'genres':genres,
                'runtime':runtime,
                'tagline':tagline,
                'popularity':popularity,
                'ratings':ratings,
            }
            return dump
        else:
            print('Wrong status code'+str(response.status_code))
            raise Exception
    except Exception as e:
        print('Exception'+str(e))
# dump=getMovieInfo('Scott Pilgrim vs the world')
# print(dump['tagline'])