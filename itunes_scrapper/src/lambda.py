import re
from urllib.parse import urlparse
import json
from bs4 import BeautifulSoup
import requests


def handler(event, context):
  webpage = 'https://itunes.apple.com/us/genre/podcasts/id26?mt=2'
  res = requests.get(url=webpage)
  bs = BeautifulSoup(res.content, "html.parser")
  divnode = bs.find('div', attrs={'id': 'genre-nav'})
  genre = []
  for link in divnode.find_all('a'):
        genre.append(
        {
            "text": link.contents[0],
            "link": link['href'],
            "id": get_Podcast_id(link['href'])
        })
  return {
    "statusCode": 200,
    "body": json.dumps(genre)
  }


def get_Podcast_id(url):
    path = urlparse(url)
    podcast_url = path.path.split('/').pop()
    podcast_id = re.findall('[0-9]+', re.findall('id[0-9]+', podcast_url)[0])[0]
    return podcast_id