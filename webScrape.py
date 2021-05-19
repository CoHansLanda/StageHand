from selenium import webdriver
from selenium.webdriver.common.keys import Keys
PATH="C:\Program Files (x86)\chromedriver.exe"
def getMovieRatings(movieName):
    driver=webdriver.Chrome(PATH)
    driver.get("https://www.google.com/")
    searchBox=driver.find_element_by_tag_name("input")
    searchBox.send_keys(movieName)
    searchBox.send_keys(Keys.ENTER)
    rating=driver.find_elements_by_xpath("//span[@class='gsrt IZACzd']")
    print(len(rating))
    imdb=rating[0].text
    rt=rating[1].text
    web3=rating[2].text
    ratings={
        "IMDb":imdb,
        "Rotten Tomatoes":rt,
        "web3": web3
    }
    driver.quit()
    return ratings

def getMovieInfo(movieName):
    print(movieName)
    driver=webdriver.Chrome(PATH)
    driver.get("https://www.google.com/")
    searchBox=driver.find_element_by_tag_name("input")
    searchBox.send_keys(movieName)
    searchBox.send_keys(Keys.ENTER)
    pageLinks=driver.find_elements_by_class_name("NY3LVe")
    imdb=pageLinks[0]
    imdb.click()
    outerWrap=driver.find_elements_by_tag_name('p')
    summary=outerWrap[22].text
    driver.quit()
    return summary

def getDirector(movieName):
    driver=webdriver.Chrome(PATH)
    driver.get("https://www.google.com/")
    searchBox=driver.find_element_by_tag_name("input")
    searchBox.send_keys(movieName+" director")
    searchBox.send_keys(Keys.ENTER)
    director=driver.find_element_by_css_selector("a.FLP8od").text
    driver.quit()
    return director