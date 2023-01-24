import requests
import mysql.connector
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime


def insert_row(x, y, z):
    # this func inserts the data we receive into the database table in mysql
    row = "insert into images (imageUrl,scrapeTime,keyword) VALUES ('" + x + "','" + y + "','" + z + "')"
    return row


def getdata(url):
    # this function returns url as texts and handles errors

    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)



def scrape(keyword, size):
    # this func scrapes data from web, creates connection with mysql db and inserts the data into table
    counter = 0
    conn = mysql.connector.connect(
        user='root', password='password', host='localhost', database='flickr')
    cursor = conn.cursor()

    old_search = keyword
    keyword = keyword.replace(' ', '%20')
    tag = 'text='
    view = '&view_all=1'

    html_requests = getdata("https://www.flickr.com/search/?" + tag + keyword)
    soup = BeautifulSoup(html_requests, 'html.parser')
    if (soup.find_all("div", {"class": "no-results-message-container"})):
        print("No matching results")
    else:
        html_requests = getdata("https://www.flickr.com/search/?" + tag + keyword + view)
        soup = BeautifulSoup(html_requests, 'html.parser')
        for img in soup.find_all('img')[:size + 1]:
            if (img['src'] == "https://combo.staticflickr.com/ap/build/images/getty/IStock_corporate_logo.svg"):
                print(" ")
            else:
                insert_stmt = insert_row(img['src'], datetime.now().isoformat(' ', 'seconds'), old_search)
                cursor.execute(insert_stmt)
                conn.commit()
                counter = counter + 1

    cursor.close()
    conn.close()
    print("Added " + str(counter) + " rows out of " + str(size))


def search(keyword, size, minScrapeTime, maxScrapeTime):
    # this func query for the data in mysql and creates pandas dataframe

    db = mysql.connector.connect(user='root', password='password', host='localhost', database='flickr')
    cursor = db.cursor()
    query1 = "SELECT * FROM images where keyword='" + keyword + "'  AND scrapeTime BETWEEN '" + minScrapeTime + "' AND '" + maxScrapeTime + "' ORDER BY 2 LIMIT " + str(
        size)

    cursor.execute(query1)
    records = cursor.fetchall()
    if len(records) == 0:
        print("There is no Data")
    elif len(records) < size:
        print("Only " + len(records) + " have been found in db")
    df = pd.DataFrame(records, columns=['imageUrl', 'scrapeTime', 'keyword'])
    print(df)
