from time import sleep
from urllib.request import Request, urlopen
from datetime import date
import os


class Scrapper:
    def __init__(self,brands):
        for i in brands:
            try:
                os.mkdir(i)
            except:
                pass
        

    def req(self, link):
        req = Request(
            url=link,
            headers={'User-Agent': 'Chrome/91.0.4472.124'})
        while (True):
            try:
                webpage = urlopen(req).read()
                break

            except ValueError as e:
                print('\n')
                print(e)
                print(
                    "\n\nNetwork Error, trying again in 15 seconds")
                os.system("clear")
                webpage = urlopen(req).read()
            except Exception as e:
                print('\n')
                print(e)
                print(
                    "\n\nWebsite blocked the request, trying again in 15 seconds")
                sleep(20)  # sleep to avoid blocking
                os.system("clear")
                webpage = urlopen(req).read()
        return webpage

    def savefile(self, name, data):
        data.to_csv(name)
