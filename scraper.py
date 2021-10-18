from log import Log
from functions import listToString
import validators
import requests
import bs4
import re

class Scraper:
    def __init__(self, url):
        self.phones = set()
        self.additional_urls = set()
        self.priority_urls = set()
        self.log = Log("log.txt")
        self.log.entry("Program started")
        self.url = url

    def validate_url(self):
        while not validators.url(self.url):
            self.log.entry(self.url + " is not a valid URL.")
            self.url = input("Please enter correct URL to scrape: ")
        if self.url[-1] == '/':
            self.url = self.url[: -1]

    def get_response(self, url):
        try:
            response = requests.get(url, allow_redirects=True)
            self.log.entry(url + " responded with status: " + str(response.status_code))
            while response.status_code != 200:
                if input("Would you like to try again? (y/n)\n") != 'y':
                    break
        except:
            self.log.entry("Could not get any response from " + url)
            self.url = input("URL to scrape: ")
        self.validate_url()
        self.soup = bs4.BeautifulSoup(response.text, 'html.parser')

    def get_phones(self, url):
        self.get_response(url)
        #self.log.entry("Scraping " + url)
        visible_text = self.soup.find_all(text=True)
        for line in visible_text:
            if any(chr.isdigit() for chr in line):
                phones = listToString(re.findall('[\+0-9]+', line))
                if len(phones) > 0 and phones[0] == '+':
                    phones = phones.split('+')
                    for phone in phones:
                        if len(phone) in range(10,27):
                            self.phones.add(int(phone))
        if len(self.phones) > 0:
            self.log.entry("Found " + str(len(self.phones)) + " phone number(s): " + str(self.phones)[1:-2])

    def get_urls(self, keywords):
        for a in self.soup.find_all('a', href=True):
                if a['href'][0] == '/':
                    link = self.url + a['href']
                else:
                    link = a['href']
                for keyword in keywords:
                    if keyword in a.text.lower() or keyword in a['href']:
                        self.priority_urls.add(link)
                if link.startswith(self.url) and link not in self.additional_urls:
                    self.additional_urls.add(link)
        self.additional_urls = self.additional_urls - self.priority_urls
        self.log.entry('Found ' + str(len(self.priority_urls)) + ' high priority and ' + str(len(self.additional_urls)) + ' low priority URL(s)')

