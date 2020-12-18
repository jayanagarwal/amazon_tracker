import requests
from glob import glob
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from time import sleep

HEADERS = ({"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"})

def search_product_list(interval_count = 1, interval_hours = 6):
    prod_tracker = pd.read_csv('trackers/TRACKER_PRODUCTS.csv')
    prod_tracker_URLS = prod_tracker.url
    tracker_log = pd.DataFrame()
    now = datetime.now().strftime('%Y-%m-%d %Hh%Mm')
    interval = 0

    while interval<interval_count :
        for x,url in enumerate(prod_tracker_URLS):
            page = requests.get(url, headers = HEADERS)
            soup = BeautifulSoup(page.content, features="lxml")

            title= soup.find(id='productTitle').get_text().strip()

            try:
                price = float(soup.find(id="priceblock_ourprice").get_text().replace('₹','').replace(',','').strip())

            except:
                try:
                    price = float(soup.find(id="priceblock_dealprice").get_text().replace('₹', '').replace(',', '').strip())
                except:
                    price = ''

            try:
                review_score = float(soup.select('.a-star-4-5')[0].get_text().split()[0].replace(',', '.'))
                review_count = int(soup.select('#acrCustomerReviewText')[0].get_text().split()[0])
            except:
                review_score = ""
                review_count = ""

            try:
                soup.select('#availability .a-color-state')[0].get_text().strip()
                stock = 'Out of Stock'
            except:
                stock = "Available"

            log = pd.DataFrame({'date':now.replace('h',':').replace('m',''),
                                'code':prod_tracker.code[x],
                                'url':url,
                                'title': title,
                                'buy_below': prod_tracker.buy_below[x],
                                'price': price,
                                'stock': stock,
                                'review_score': review_score,
                                'review_count': review_count}, index=[x])

            try:
                if price< prod_tracker.buy_below[x]:
                    print('ALERT!!!!\nBuy the '+prod_tracker.code[x]+'\n'+prod_tracker.url[x])

            except:
                pass

            tracker_log = tracker_log.append(log)
            print('append '+prod_tracker.code[x]+'\n'+ title +'\n\n')
            sleep(5)

        interval += 1

        sleep(interval_hours*1*1)
        print('end of interval '+ str(interval))

    last_search = glob('/home/jayan/Desktop/amazon_tracker/search/*.xlsx')[-1]
    search_hist = pd.read_excel(last_search)
    final_df = search_hist.append(tracker_log, sort = False)
    final_df.to_excel('search/SEARCH_HISTORY_{}.xlsx'.format(now), index=False)
    print('End of Search')

search_product_list()
