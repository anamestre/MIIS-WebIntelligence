# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 14:26:32 2020

"""

from bs4 import BeautifulSoup
import requests, re


def crawl_page(url):
    crawled_urls = []
    urls_to_check = []
    
    i = 0
    page = requests.get(url)
    crawled_urls.append(url) # visited
    urls_to_check.append(url)
    
    while(urls_to_check != []):
        i += 1
        act = urls_to_check[0]
        if len(urls_to_check) > 1:
            urls_to_check = urls_to_check[1:]
        else:
            urls_to_check = []
            
        page = requests.get(act)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        f = open("webs/web" + str(i) + ".html", "w+", encoding="utf-8")
        f.write(str(soup))
        f.close()
        
        if(i == 10):
            return
        for link in soup.findAll('a', attrs={'href': re.compile("^http") }):
            urls_to_check.append(link.get('href'))


crawl_page("https://www.pornhub.com")
        
        