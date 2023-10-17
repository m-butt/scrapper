from datetime import date, timedelta
from pickle import dump, load
import datetime
from Scrapping import Scrapper
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import pathlib

class CDW(Scrapper):
    def __init__(self):
        super().__init__()
        self.Shop_By_Product_apple_links = []
        self.CDW()

    def CDW(self):
        with requests.Session() as session:
            print("Now Scraping link: ", "Apple")
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

        # //////////////////////////////////////////////////////////////////////
        # /////////////////////////////////////////////////////////////////////
        with requests.Session() as session:
            for each_link in self.Shop_By_Product_apple_links:
                webpage = self.req(each_link)
                soup = BeautifulSoup(webpage, 'html.parser')
                outer_div_elements = soup.find_all('div', class_='search-result coupon-check')
                product_data = []
                for outer_div in outer_div_elements:
                    each_product = outer_div.find('div', class_='grid-row')
                    each_product_detail = each_product.find_all('div', class_='columns-right grid-row col-6')
                    
                #     # Extract product details
                    for product_detail in each_product_detail:
                        product_name = product_detail.find('a', class_='search-result-product-url').text
                        manufacturer_id = product_detail.find('span', class_='mfg-code').text.split(': ')[1]
                        price = product_detail.find('div', class_='price-type-price').text.strip()
                        specs_dict = {}
                        specs = product_detail.find('div', class_='expanded-specs')
                        if specs:
                            spec_items = specs.find_all('div', class_='product-spec-listing')
                            for spec_item in spec_items:
                                header = spec_item.find('div', class_='product-spec-header').text.strip()
                                value = spec_item.find('div', class_='product-spec-value').text.strip()
                                specs_dict[header] = value

                        product_image_url = product_detail.find('a', class_='search-result-product-url')['href']

                        # Create a dictionary for each product
                        product_dict = {
                            "name": product_name,
                            "Munfuctureid": manufacturer_id,
                            "price": price,
                            "specs": specs_dict,
                            "productimageurl": product_image_url
                        }
                        # Append the product dictionary to the list
                        product_data.append(product_dict)
                
                self.save_in_file(product_data)
                exit()
                
                        


    
    def simple_link_generator(self,links):
        for link in links:
            full_link = "https://www.cdw.com" + link
            self.Shop_By_Product_apple_links.append(full_link)
    
    def save_in_file(self,products):
        with open('products.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'Munfuctureid', 'price', 'specs', 'productimageurl']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write the header row
            writer.writeheader()

            # Write the product data to the CSV file
            writer.writerows(products)

CDW()
