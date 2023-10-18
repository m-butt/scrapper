import re
import requests
from bs4 import BeautifulSoup



def link_concat(link):
        full_link = "https://www.cdw.com" + link
        return full_link


def get_price(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the price element inside the specific div
        price_div = soup.find('div', {'class': 'price-type-single ui-priceselector-single'})
        discount_div = soup.find('div', {'class': 'pdprightrailmsrp'})
        
        if price_div:
            price_element = price_div.find('span', {'class': 'price-type-selected'})
            # Check if discount_div is not None before accessing its attributes
            discount_element = None
            if discount_div:
                discount_element = discount_div.get('data-pricevalue')
                if float(discount_element) == 0:
                     discount_element = None
            
            if price_element and discount_element:
                 # Extract numeric value from the content attribute using regular expressions
                price_value = float(re.search(r'[\d.]+', price_element['content']).group())
                discount = float(discount_element) - float(price_value)
                print("Price $:", price_value)
                print("Discount $:", round(discount))
            
            elif price_element:
                price = price_element.text.strip()
                print("Price:", price)
                print("No Discount on this prodcut")
            else:
                print("Unable to get the price.")
        else:
            print("Page do not have information regarding price.")
    else:
        print("Failed to fetch the page. Status Code:", response.status_code)



def get_searched_link(url,mnFID):
    # URL to be scraped
    url = url+mnFID
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        scripts = soup.find_all('script', type='text/javascript')

        # Extract the URL from the script tag
        redirect_url = None
        for script in scripts:
            script_text = script.get_text()
            match = re.search(r'location.href\s*=\s*["\']([^"\']+)["\'];', script_text)
            if match:
                redirect_url = match.group(1)
                break

        if redirect_url:
            correct_url = link_concat(redirect_url)
            get_price(correct_url)
        else:
            print("Record Not Found.")
    else:
        print("Failed to fetch the page. Status Code:", response.status_code)
    

search_query = input("Enter MFG#: ")
get_searched_link("https://www.cdw.com/search/?key=",search_query)