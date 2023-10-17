from datetime import date, timedelta
from pickle import dump, load
import datetime
from Scrapping import Scrapper
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import pathlib

class CDW(Scrapper):
    def __init__(self):
        super().__init__()
        self.Shop_By_Product_apple_links = []
        self.CDW()

    def CDW(self):
        with requests.Session() as session:
            print("Now Scraping link: ", "iphone")
            links_ = []
            Product = []
            Price = []
            Man_Number = []
            webpage = self.req("https://www.cdw.com/content/cdw/en/brand/apple.html")
            soup = BeautifulSoup(webpage, 'html.parser')
            outer_div_elements = soup.find_all('div', class_='cdwgridlayout parbase section')
            for outer_div in outer_div_elements:
                inner_div_elements = outer_div.find_all('div', class_='cdwheadlineatom parbase section') 
                # Iterate through inner div elements and find h2 elements
                for inner_div in inner_div_elements:
                    h2_elements = inner_div.find_all('h2')
                    # Extract text from h2 elements
                    for h2 in h2_elements:
                        if h2 is not None and h2.text.strip() == "Shop By Product":
                            links = outer_div.find_all('a', href=True)
                            for link in links:
                                links_.append(link['href'])
            self.simple_link_generator(links_)
    
    def simple_link_generator(self,links):
        for link in links:
            full_link = "https://www.cdw.com" + link
            self.Shop_By_Product_apple_links.append(full_link)
        print(self.Shop_By_Product_apple_links)


CDW()
