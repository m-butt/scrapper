from datetime import date, timedelta
from pickle import dump, load
import datetime
from Scrapping import Scrapper
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import re

class CDW(Scrapper):
    def __init__(self):
        self.brands = ["Apple","HP","Intel"]
        super().__init__(self.brands)
        
        self.Shop_By_Product_apple_links = []
        self.CDW()

    def CDW(self):
        with requests.Session() as session:
            print("Now Scraping link: ", "Apple")
            links_ = []
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
            for i in range(len(self.Shop_By_Product_apple_links)):
                try:
                    Proper_link = self.get_redirect_url(self.Shop_By_Product_apple_links[i],False)
                    if Proper_link:
                        self.Shop_By_Product_apple_links[i] = self.link_concat(Proper_link)
                except:
                    pass


            self.Apple()

        
    def Apple(self):           
        with requests.Session() as session:
            for each_link in self.Shop_By_Product_apple_links:
                Queue = []
                products = []
                Queue.append(each_link)
                while Queue:
                    current_link =  Queue.pop(0)
                    webpage = self.req(current_link)
                    soup = BeautifulSoup(webpage, 'html.parser')
                    product_,next_link = self.each_page_scrap(soup) 
                    products.extend(product_)
                    if self.check_redirection_error(next_link,current_link):
                        Queue.append(self.link_concat(next_link))
                    else:
                        print("working fine allah ka shukr")
                # Use regular expression to find substring after "enkwrd="
                match = re.search(r'enkwrd=([a-zA-Z]+)', each_link) 
                # If a match is found, return the captured substring, else return None
                if match:
                    cat = match.group(1)
                else:
                    cat = "products"
                
                self.save_in_file(products,cat,"Apple")

            

    
    def check_redirection_error(self,redirect_url,current_page):
        if redirect_url:
            # Find the index of the last "/"
            last_slash_index = current_page.rfind("/")
            
            # Extract the substring after the last "/"
            substring_after_last_slash = current_page[last_slash_index + 1:]
            if substring_after_last_slash == redirect_url:
                return True
            else:
                return False
        else:
            return False
    
    def save_in_file(self,products,cat,brand):
        cat = cat + ".csv"
        file_path = os.path.join(brand, cat)
        with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'Munfuctureid', 'price', 'specs', 'productimageurl']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write the header row
            writer.writeheader()

            # Write the product data to the CSV file
            writer.writerows(products)
    
    
    
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    # //////////////////////////////////////////////////////////////////////////////////
    def link_concat(self,link):
        full_link = "https://www.cdw.com" + link
        return full_link
    
    
    # //////////////////////////////////////////////////////////////////////////////////
    def simple_link_generator(self,links):
        for link in links:
            full_link = self.link_concat(link)
            self.Shop_By_Product_apple_links.append(full_link)
    
    
    
    # //////////////////////////////////////////////////////////////////////////////////
    def get_redirect_url(self,next_page_url,header = True):             
        
        if header:
            # Send a GET request to the URL
            response = requests.get(self.link_concat(next_page_url))
        else:
            response = requests.get(next_page_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
        # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, "html.parser")
            scripts = soup.find_all('script', type='text/javascript')
            # Extract the URL from the script tag
            redirect_url = None
            for script in scripts:
                script_text = script.get_text()
                match = re.search(r'location.href\s*=\s*["\']([^"\']+)["\'];', script_text)
                if match:
                    redirect_url = match.group(1)
                    break

            return redirect_url
            
    
    
    # //////////////////////////////////////////////////////////////////////////////////
    def check_nextpage_link(self,soup):
            outer_div_elements = soup.find_all('div', class_='search-pagination-list-container tagman search-pagination-footer')
            for outer_div in outer_div_elements:
                    next_page_link = outer_div.find('a', {'aria-label': 'Next Page'})
                    if next_page_link:
                        next_page_url = next_page_link['href']
                        return self.get_redirect_url(next_page_url)
                    else:
                        return
                    
    
     
    # //////////////////////////////////////////////////////////////////////////////////
    def each_page_scrap(self,soup):
        outer_div_elements = soup.find_all('div', class_='search-result coupon-check')
        product_data = []
        for outer_div in outer_div_elements:
            each_product = outer_div.find('div', class_='grid-row')
            each_product_detail = each_product.find_all('div', class_='columns-right grid-row col-6')
            # Extract product details
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
        next_url = self.check_nextpage_link(soup)
        return product_data, next_url

CDW()
