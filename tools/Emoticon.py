#Embedded file name: tools/Emoticon.py
import requests
import bs4
import itertools
import csv

class EmoticonBuilder(object):
    """
    Initialize the EmoticonBuilder class with the website where
    emoticon unicodes are going to be gathered
    """

    def __init__(self, website = 'http://apps.timwhitlock.info/emoji/tables/unicode'):
        self.website = website

    def pageToSoup(self, url):
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text)
        return soup

    def build(self):
        emoticon_unicodes = []
        emoticon_description = []
        soup = self.pageToSoup(self.website)
        emoticon_unicodes = [ emoticon.text for emoticon in soup.select('tr > td:nth-of-type(9)') ]
        emoticon_description = [ description.text for description in soup.select('tr > td:nth-of-type(10)') ]
        self.emoticons = dict(itertools.izip(emoticon_unicodes, emoticon_description))

    def save(self):
        with open('emoticons.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            for row in self.emoticons.iteritems():
                writer.writerow(row)
