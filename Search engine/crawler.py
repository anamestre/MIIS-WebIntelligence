# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 14:26:32 2020

"""

from bs4 import BeautifulSoup
import requests, re
import urllib.robotparser
import time
from urllib.parse import urlparse


def crawl_page(url):
    urls_to_check = []
    pages = []
    
    i = 0   # web pages counter
    page = requests.get(url)
    urls_to_check.append(url) # nodes yet to be visited -> it will be used as a queue
    
    # BFS strategy
    while(urls_to_check != []):
        act = urls_to_check[0]      # current node to visit (top of queue)
        if len(urls_to_check) > 1:  # pop first element
            urls_to_check = urls_to_check[1:]
        else:
            urls_to_check = []

        # https://docs.python.org/3/library/urllib.robotparser.html
        rp = urllib.robotparser.RobotFileParser() 
        data_url = urlparse(act)
        root_url = data_url.scheme + "://" + data_url.netloc

        robots = root_url + "/robots.txt"

        rp.set_url(robots)
        rp.read()
        rrate = rp.can_fetch("*", act) # Checking for allowed URLs
        cdelay = rp.crawl_delay("*") # Checking if there is crawl delay defined

        # Check if this URL can be crawled
        if rrate:
            if act not in pages:
                
                # Check crawl delay
                if cdelay is not None:
                    print("Delay: ", root_url, cdelay)
                    time.sleep(cdelay)
                
                i += 1
                pages.append(act)
                page = requests.get(act)
                soup = BeautifulSoup(page.content, 'html.parser')

                f = open("webs/web" + str(i) + ".html", "w+", encoding="utf-8")
                f.write(str(soup))
                f.close()

                if(i == 20): # Limit of pages to be crawled 
                    return
                for link in soup.findAll('a', attrs={'href': re.compile("^http") }):
                    urls_to_check.append(link.get('href'))

start_time = time.time()
crawl_page("https://en.wikipedia.org/wiki/Modern_Family")
print("--- %s seconds ---" % (time.time() - start_time))