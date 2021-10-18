from scraper import Scraper
from functions import splitAt
import argparse


parser = argparse.ArgumentParser(description="Let's scrape some phone numbers :)")
parser.add_argument('url', type=str)
args = parser.parse_args()
scraper = Scraper(args.url)

with open('keywords.txt') as f:
    keywords = f.read().splitlines()
scraper.log.entry("Your keywords are: " + str(keywords)[1:-2].replace("'",""))

# Check if URL is correct
scraper.validate_url()
# Scrape URL for phones
scraper.get_phones(scraper.url)
if len(scraper.phones) == 0:
    #Get urls from website
    scraper.get_urls(keywords)
    for url in scraper.priority_urls:
        if len(scraper.phones) > 0: break
        scraper.get_phones(url)
    for url in scraper.additional_urls:
        if len(scraper.phones) > 0: break
        scraper.get_phones(url)
if len(scraper.phones) > 0:
    # Get lowest phone number [ASSUMPTION: Main company number is usually the lowest extension number]
    scraper.phone = '+' + str(min(scraper.phones))
    scraper.log.entry("Main company number is "+" ".join(splitAt(scraper.phone, 3)))
    if not scraper.log.enable_printing:
        print(" ".join(splitAt(scraper.phone, 3)))
else:
    scraper.log.entry("Unfortunately no number was found :(")
scraper.log.entry("Program closed")
