import time

import requests
from selenium.webdriver.chrome import webdriver
from Recipe import Recipe
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from lxml import etree


class RozkosznyScrape():
    def __init__(self):
        self.links = {"Sniadanie" : 'https://www.rozkoszny.pl/sniadanie/',
                     "Obiad" : 'https://www.rozkoszny.pl/obiad/',
                     "Lunchbox" : 'https://www.rozkoszny.pl/do-lunchboxa/',
                     "Slodkosci" : 'https://www.rozkoszny.pl/slodkosci/',
                     "do Chleba": 'https://www.rozkoszny.pl/do-chleba/',
                     "na lekko": 'https://www.rozkoszny.pl/na-lekko/',
                     "w Podrozy" : 'https://www.rozkoszny.pl/w-podrozy/'}



    def createSoup(self, link):
        driver = webdriver.Chrome()
        driver.get(link)
        time.sleep(1)
        check = True
        try :
            while check:
                loadButton = driver.find_element(By.XPATH,'/html/body/div[2]/div/section[3]/div/div/div/div/div/div/div/div/div/div/a')
                loadButton.click()
                time.sleep(1)
        except NoSuchElementException:
            check = False

        html = driver.page_source
        driver.quit()

        return BeautifulSoup(html, 'html.parser')
    def createSoupStatic(self,link):
        r = requests.get(link)
        return BeautifulSoup(r.content, 'html.parser')
    def scrapeOneRecipe(self,link,AllRecipes):
        # linkElement = recipe.find('a', class_='penci-image-holder penci-lazy')
        # link = linkElement['href']
        soupOneRecipe = self.createSoupStatic(link)
        ingredientsElements = soupOneRecipe.findAll('p', class_='has-text-align-center has-background')
        ingredientsElements += soupOneRecipe.findAll('p', class_='has-background has-text-align-center has-very-light-gray-background-color')
        ingredientsElements += soupOneRecipe.select('p[style="text-align: center;"]')
        ingredients = []
        for ingredient in ingredientsElements:
            if ingredient is not None:
                ingredients += (ingredient.getText(';', strip=True).split(";"))
        detailsElement = soupOneRecipe.find('section',class_='penci-section penci-disSticky penci-structure-10 elementor-section elementor-top-section elementor-element elementor-element-9863ba0 elementor-section-boxed elementor-section-height-default elementor-section-height-default')
        details = []
        for detail in detailsElement.select('p:not([class]):not([id]):not([style])'):
            details.append(detail.text)

        if len(ingredients) > 0 and len(details) > 0:
            title = ingredients.pop(0)
            amount  = ingredients.pop(0)
            AllRecipes.append(Recipe(ingredients, details,amount,title))



    def scrapeOnePage(self):
        for x in self.links:
            AllRecipes = []
            print("Tytul: " + x)
            soupRozkoszny = self.createSoup(self.links[x])
            recipes = soupRozkoszny.findAll('li', class_='list-post list-boxed-post')
            # print("ilosc przepisow w kategori: " + x + " = " + str(len(recipes)))
            for recipe in recipes:
                link = recipe.select_one('[href]')
                link = link['href']
                self.scrapeOneRecipe(link,AllRecipes)
            for recipe in AllRecipes:
                filename = x + ".txt"
                f = open(filename, "a",encoding="utf-8")
                recipe.writeInfo(f)
                f.close()





