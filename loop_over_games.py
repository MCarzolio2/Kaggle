# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import urllib2
from bs4 import BeautifulSoup
import game_level_parser as glp

# <codecell>

url = 'http://stats.ncaa.org/team/index/12020?org_id=742'
html_file = urllib2.urlopen(url)
soup = BeautifulSoup(html_file)


# Gives the list of urls for play-by-play data for team(season) given at url:
url_list = []

for a in soup.find_all('a', href=True):
    string = a['href']
    if string[1:5]=='game':
        game_id = string[12:19]
        url_list.append('http://stats.ncaa.org/game/play_by_play/'+game_id)
    

# <codecell>


