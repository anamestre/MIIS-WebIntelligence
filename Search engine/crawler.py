# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 14:26:32 2020

"""

from bs4 import BeautifulSoup
import requests, re
import urllib.robotparser
import time


def crawl_page(url):
    crawled_urls = []
    urls_to_check = []
    pages=[]
    
    i = 0
    page = requests.get(url)
    crawled_urls.append(url) # visited
    urls_to_check.append(url)
    
    while(urls_to_check != []):
        act = urls_to_check[0]
        if len(urls_to_check) > 1:
            urls_to_check = urls_to_check[1:]
        else:
            urls_to_check = []


        rp = urllib.robotparser.RobotFileParser() #https://docs.python.org/3/library/urllib.robotparser.html

        from urllib.parse import urlparse

        data_url = urlparse(act)
        root_url=data_url.scheme + "://" + data_url.netloc


        robots = root_url + "/robots.txt"

        rp.set_url(robots)
        rp.read()
        rrate=rp.can_fetch("*",act)
        cdelay = rp.crawl_delay("*")

        if rrate:
            if act not in pages:
                
                if cdelay is not None:
                    print("Delay root_url: ", cdelay)
                    time.sleep(cdelay)
                
                i += 1
                pages.append(act)
                #print("Robots: " + robots + " web " + act)
                page = requests.get(act)
                soup = BeautifulSoup(page.content, 'html.parser')

                f = open("webs/web" + str(i) + ".html", "w+", encoding="utf-8")
                f.write(str(soup))
                f.close()

                if(i == 20):
                    return
                for link in soup.findAll('a', attrs={'href': re.compile("^http") }):
                    urls_to_check.append(link.get('href'))

start_time = time.time()
crawl_page("https://en.wikipedia.org/wiki/Modern_Family")
print("--- %s seconds ---" % (time.time() - start_time))