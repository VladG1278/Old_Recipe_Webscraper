import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import sys

sys.argv
numTimes = 5
if len(sys.argv) < 2:
    quit()
if len(sys.argv) >= 2:
    search = sys.argv[1]
if len(sys.argv) == 3:
    numTimes = int(sys.argv[2])
driver = webdriver.Chrome()
link = "https://www.allrecipes.com/search?q=" + search.replace(" ", "%20")
driver.get(link)
time.sleep(5)
numReference = 0
counter = 0
while counter < numTimes:
    if numReference == 0:
        newLink = driver.find_element("id", "mntl-card-list-items_1-0").get_attribute("href")
    else:
        newLink = driver.find_element("id", "mntl-card-list-items_1-0-" + str(numReference)).get_attribute("href")
    if not newLink.find("/recipe/") > 0:
        numReference = numReference + 1
    else:
        secondTab = requests.get(newLink)
        soup = BeautifulSoup(secondTab.content, "html.parser")
        titleResults = soup.find(id="article-heading_1-0").text.replace("\n", "")

        # Creates new file for the recipe
        file = open(titleResults + ".txt", "w")
        file.close()

        # Grabbing Information WebScraper
        infoResults = soup.find(id="recipe-details_1-0")

        # Making Info Look Pretty
        if infoResults.text is not None:
            infoResults = infoResults.text
            infoResults = infoResults.replace("\n", "").replace("Jump to Nutrition Facts", "")
            infoResults = infoResults.replace(":", ": ").replace("mins", "mins\n").replace("hrsS", "hrs\nS").replace("hrsT", "hrs\nT")
            infoResults = infoResults.replace("Yield: ", "\nYield: ")
        # Putting Info Into File
        file = open(titleResults + ".txt", "a")
        file.write(titleResults + "\n\nHelpful Information:\n" + infoResults)
        file.close()

        # Getting ingredients
        ingredients = soup.findAll(class_="mntl-structured-ingredients__list-item")
        file = open(titleResults + ".txt", "a")
        file.write("\n\nIngredients: ")

        # Putting Ingredients Into A File
        for x in ingredients:
            file.write("\n" + x.text.replace("\n", "").replace('\u2153', "1/3").replace('\u215b', "1/8").replace('\u2154', "2/3"))
        file.close()

        # Instructions
        # https://stackoverflow.com/questions/32063985/deleting-a-div-with-a-particular-class-using-beautifulsoup
        delete = soup.findAll(class_="figure-article-caption-owner")
        for x in delete:
            x.decompose()
        steps = soup.findAll(class_="comp mntl-sc-block-group--LI mntl-sc-block mntl-sc-block-startgroup")
        file = open(titleResults + ".txt", "a")
        stepCounter = 1
        file.write("\n\nSteps:\n")
        for x in steps:
            file.write(str(stepCounter) + ". " + x.text.replace("\n", "") + '\n')
            stepCounter = stepCounter + 1
        file.close()
        numReference = numReference + 1
        counter = counter + 1
