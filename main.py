import Flickr
from datetime import datetime

print("Welcome to our Flickr scraper and searcher")
# input a number
while True:
    try:
        size = int(input("Enter size of numbers to search: "))
        break
    except ValueError:
        print("Please insert numbers only...")
        continue

print("Size selected: ", size)

print("\n")
while True:
    keyword = input("Enter the keyword of photos to search: ")
    if len(keyword) > 100:
        print("Max characters is 100")
        continue
    else:
        print("Keyword selected: ", keyword)
        break

# Flickr.scrape(keyword, size)

minScrapeTime = input("Please enter the minimum scraping time to search in 'yyyy-mm-dd hh:mm:ss format: ")
maxScrapeTime = datetime.now().isoformat(' ', 'seconds')

Flickr.search(keyword, size, minScrapeTime, maxScrapeTime)

print("\n"
      "Thank you for scraping and searching")
