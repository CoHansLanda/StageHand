from tmdb import getBio, getMovieRuntime, movieCredits
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import imdb
from imdb.Person import Person
ia=imdb.IMDb()
PATH="C:\Program Files (x86)\chromedriver.exe"
def getMovieRatings(movieName):
    driver=webdriver.Chrome(PATH)
    driver.get("https://www.google.com/")
    searchBox=driver.find_element_by_tag_name("input")
    searchBox.send_keys(movieName)
    searchBox.send_keys(Keys.ENTER)
    rating=driver.find_elements_by_xpath("//span[@class='gsrt IZACzd']")
    print(len(rating))
    ratings={
        "IMDb":rating[0].text,
        "Rotten Tomatoes":rating[1].text,
    }
    driver.quit()
    return ratings
def getMovieID(movieName):
    try:
        movies=ia.search_movie(movieName)
        id=movies[0].movieID
    except:
        driver=webdriver.Chrome(PATH)
        driver.get("https://www.google.com/")
        searchBox=driver.find_element_by_tag_name("input")
        searchBox.send_keys(movieName)
        searchBox.send_keys(Keys.ENTER)
        pageLinks=driver.find_elements_by_class_name("NY3LVe")
        imdb=pageLinks[0]
        imdb.click()
        url=''.join(driver.current_url)
        id=url[url.index('title')+8:url.index('title')+15]
        driver.quit()
    finally:
        return id

def getActorID(actorName):
    try:
        people=ia.search_person(actorName)
        id=people[0].personID
    except:
        driver=webdriver.Chrome(PATH)
        driver.get("https://www.google.com/")
        searchBox=driver.find_element_by_tag_name("input")
        searchBox.send_keys(actorName)
        searchBox.send_keys(Keys.ENTER)
        pageLinks=driver.find_element_by_link_text("imdb.com")
        pageLinks.click()
        url=''.join(driver.current_url)
        id=url[url.index('name')+6:-1]
        driver.quit()
    finally:
        return id

def getDirector(movieName):
    movie=ia.get_movie(getMovieID(movieName))
    director=movie['director'][0]
    return director

def getActorDet(actorName):
    try:
        actorID=getActorID(actorName)
        actor=ia.get_person(actorID,info=['awards'])
        actor.infoset2keys
        dump={
            'bio':getBio(actorName),
            'awards':actor['awards'],
            'films':movieCredits(actorName)
        }
        return dump
    except Exception as e:
        print(e)