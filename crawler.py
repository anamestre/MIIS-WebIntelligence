# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 14:26:32 2020

"""

from bs4 import BeautifulSoup
import requests


def crawl_page(url):
    page = requests.get(url)