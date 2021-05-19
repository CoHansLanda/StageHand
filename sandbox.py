from selenium import webdriver
from selenium.webdriver.common.keys import Keys
PATH="C:\Program Files (x86)\chromedriver.exe"
movieName="The Godfather: part II"
# def getMovieID(movieName):
#     driver=webdriver.Chrome(PATH)
#     driver.get("https://www.imdb.com/")
#     inputBox=driver.find_element_by_id("suggestion-search")
#     inputBox.send_keys(movieName)
#     inputBox.send_keys(Keys.ENTER)
#     resultList=driver.find_element_by_link_text("Movie")
#     resultList.click()
#     moviePage=driver.find_element_by_link_text(movieName)
#     moviePage.click()

driver=webdriver.Chrome(PATH)
driver.get("https://www.imdb.com/")
inputBox=driver.find_element_by_id("suggestion-search")
inputBox.send_keys(movieName)
inputBox.send_keys(Keys.ENTER)
resultList=driver.find_element_by_link_text("Movie").click()
moviePage=driver.find_element_by_link_text(movieName).click()