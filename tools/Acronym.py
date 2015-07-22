#Embedded file name: tools/Acronym.py
import requests
import bs4
import itertools
import csv

class AcronymBuilder(object):
    """
    Initialize the AcronymBuilder with a given website
    from which the acronyms will be gathered
    """

    def __init__(self, website = 'http://www.noslang.com/dictionary/'):
        self.website = website

    def pageToSoup(self, url):
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text)
        return soup

    def getLinks(self):
        soup = self.pageToSoup(self.website)
        return [ link['href'] for link in soup.select('div[style] a[href^=' + self.website + ']') ]

    def build(self):
        acronyms_name = []
        acronyms_meaning = []
        for link in self.getLinks():
            soup = self.pageToSoup(link)
            acronyms_name += [ acronym['name'] for acronym in soup.select('dt a[name]') ]
            acronyms_meaning += [ acronym_meaning['title'] for acronym_meaning in soup.select('dt abbr[title]') ]

        self.acronyms = dict(itertools.izip(acronyms_name, acronyms_meaning))

    def save(self):
        with open('acronym.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            for row in self.acronyms.iteritems():
                writer.writerow(row)
