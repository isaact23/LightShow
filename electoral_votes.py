#!/usr/bin/env python

from urllib.request import urlopen
#import re
from bs4 import BeautifulSoup
from time import sleep

url = 'https://www.nytimes.com/interactive/2020/11/03/us/elections/results-president.html'

biden = 0
trump = 0
tie = 0

def get_scores():
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.findAll("div", { "class" : "e-count-label" })
    return [d.text for d in data]

if __name__ == "__main__":
    while True:
        scores = get_scores()
        print(scores)
        if (biden != scores[0] or trump != scores[1]):
            print("Updated scores!")
        else:
            print("No update.")
        biden, trump, tie = scores[0], scores[1], scores[2]
        print("Biden", biden, "Trump", trump, "Tie", tie)

        sleep(15)
