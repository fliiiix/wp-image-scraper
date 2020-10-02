import requests
from slugify import slugify
from bs4 import BeautifulSoup
import os
import sys


if len(sys.argv) != 2:
    print("needs url as param")
    exit(1)

URL = sys.argv[1]
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

title = soup.find('h1', class_='entry-title')
title = slugify(title.text.strip())
print("Downloading: {}".format(title))

os.makedirs(title)

results = soup.find_all('a')

for r in results:
    if 'uploads' in r['href']:
        url = r['href']
        filename = url.split("/")[-1]
        filename = "{}/{}".format(title, filename)
        print("  Downloading {}".format(filename))
        r = requests.get(url, timeout=0.5)

        if r.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(r.content)

