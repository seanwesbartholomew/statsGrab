'''
general api for what we looking for kind of hard, so may have to start with custom janky build

structure / design thoughts:

backlog / archive seasons - Need to load all historical stats into site for whichever sports we want. can choose how far we want to go back

current seasons - for each sport we do this will be where the current season is held.  Live games will appear here and then once a new season starts the current season will be added to the archive

    in season

    -> leagues -> teams -> games -> finished / live
    -> live games will update frequently until completion then end

    out of season
    
    -> similar structure above with the most recent season here

for now I think our best bet is going to be internet scurbbing, easiest way to find up to date stats that I know of right now

'''

import pandas as pd
import requests
from bs4 import BeautifulSoup

def strip_elements(soup_elem):
    for stuff in soup_elem(['th','tr','td']):
        a = stuff.get_text()
        print(a)
    return soup_elem.get_text()
    

if __name__=='__main__':
    '''
        url formats (... = https://www.espn.com): 
        team stats: .../nba/team/stats/_/name/<city_tag>/<city_name-team_name>

    '''
    page = requests.get('https://www.espn.com/nba/team/stats/_/name/bos/boston-celtics')
    page_html = page.text
    html_file = open('page.txt', 'w')
    html_file.write(page_html)
    html_file.close()

    soup = BeautifulSoup(open('page.html','r'), 'html.parser')

    page_text = soup.get_text(separator='\n', strip=True)
    #print(page_text)

    page_text=strip_elements(soup)
    print("-----------------------------------------------------------------------------------------------------")

    page_text = soup.get_text(separator='\n', strip=True)
    #print(page_text)
    

    #page_text = page_text.split('\n')