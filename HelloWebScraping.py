# web scrapping example with beautiful soup.
# Objectives:
#   scrape data into a CSV.
#   Goal: grab all links from Rithm School blog.
#   Data: store URL, anchor tag text, and date.

import requests
from csv import writer
from bs4 import BeautifulSoup

# http request.
response = requests.get("https://www.rithmschool.com/blog")
# instantiate BS to a variable.
soup = BeautifulSoup(response.text, "html.parser")
# find all article tags in the html.
articles = soup.find_all("article")
# write csv file, csv file will contain web scarped information.
with open("blog_data.csv", "w") as csv_file:
    csv_writer = writer(csv_file)
    csv_writer.writerow(["title", "link", "date"])
    # for all articles in html, find the anchor tags and retrieve the text.
    for article in articles:
        # get anchor tag.
        a_tag = article.find("a")
        # get title text from anchor tag.
        title = a_tag.get_text()
        # get url from href from anchor tag.
        url = a_tag["href"]
        # get date from article.
        date = article.find("time")["datetime"]
        csv_writer.writerow([title, url, date])