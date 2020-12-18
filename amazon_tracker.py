import requests
from glob import glob
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from time import sleep

HEADERS = ({"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"})

prod_tracker = pd.read_csv('trackers/TRACKER_PRODUCTS.csv')
prod_tracker_URLS = prod_tracker.url

page = requests.get(prod_tracker_URLS[0], headers = HEADERS)

soup = BeautifulSoup(page.content, features="lxml")
