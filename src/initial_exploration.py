import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

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

def get_names(clean_data):
    new_arr = []
    player_id=0
    for i in clean_data:
        if len(i) < 2: 
            if re.search('[a-z]', i[0]) and (i[0] not in new_arr):
                new_arr.append(i[0])
                player_id += 1
    return new_arr

def get_categories(clean_data):
    new_arr = ['NAME']
    for i in clean_data:
        if len(i) > 3:
            for j in i:
                if re.search('[A-Z]', j) and (j not in new_arr):
                    new_arr.append(j)
    return new_arr

def get_stats(clean_data):
    new_arr=[]
    data_id=0
    for i in clean_data:
        if len(i) > 3:
            if re.search('[0-9.]', i[0]) and (i[0] not in new_arr):
                if len(i) > 12:
                    new_arr.append([data_id, i])
                    data_id += 1
    return new_arr[:-1]

def combine_data(names_arr, stats_arr):
    combed_stats = []
    combined_arr = []
    for i in range(len(names_arr)):
        combed_stats.append(stats_arr[i][1] + (stats_arr[i+len(names_arr)][1]))
    for i in range(len(combed_stats)):
        combined_arr.append([names_arr[i]] + combed_stats[i])
    return combined_arr

'''
Target format:
Player  GP  GS  MIN  PTS  OR  DR  REB  AST  STL  BLK  TO  PF  AST/TO  FGM  FGA  FG%  3PM  3PA  3P% FTM  FTA  FT%  2PM  2PA  2P%  SC-EFF  SH-EFF
'''
def create_dataframes(labels, combined_stats):
    for i in range(len(combined_stats)):
        combined_stats[i] = pd.Series(combined_stats[i])
    df_combed = pd.DataFrame(combined_stats)
    df_combed=df_combed.rename(columns=pd.Series(labels))
    return df_combed

'''
this gets all info twice. Once individually and once all together in one line. this is because of the html structure having the text mentioned twice. 

We need to first separate out names, categories, values, etc. Then we need to parse them correctly into the right columns and such
'''
def clean_data_arrs(data_arrs):
    new_arr = []
    for i in data_arrs:
        if len(i) > 1 and (i not in new_arr):
            if len(i) < 4:
                new_arr.append([i[0].lower()])
            else:
                new_arr.append(i)
    return new_arr

def strip_elements(soup_elem):
    data_arrs = []
    for stuff in soup_elem(['th','tr','td']):
        a = stuff.get_text(separator=',', strip=True)
        page_data_arr = a.split(',')
        data_arrs.append(page_data_arr)
    return data_arrs
    

if __name__=='__main__':
    '''
        url formats (... = https://www.espn.com): 
        team stats: .../nba/team/stats/_/name/<city_tag>/<city_name-team_name>
    '''
    page = requests.get('https://www.espn.com/nba/team/stats/_/name/bos/boston-celtics')
    page_html = page.text
    html_file = open('../out/page.html', 'w')
    html_file.write(page_html)
    html_file.close()

    soup = BeautifulSoup(open('../out/page.html','r'), 'html.parser')

    page_text = soup.get_text(separator='\n', strip=True)
    #print(page_text)

    data_arrs = strip_elements(soup)
    data_arrs_clean = clean_data_arrs(data_arrs)
    names_arr = get_names(data_arrs_clean)
    categories_arr = get_categories(data_arrs_clean)
    stats_arr = get_stats(data_arrs_clean)
    combined_arr = combine_data(names_arr, stats_arr)
    stats_df = create_dataframes(categories_arr, combined_arr)

    print('-----------------------------------------------------------------------------------------------------')
    print('DATA ARR')
    print('--------')
    print(data_arrs_clean)
    print('-----------------------------------------------------------------------------------------------------')
    print('NAMES')
    print('-----')
    print(names_arr)
    print('LEN:', len(names_arr))
    print('-----------------------------------------------------------------------------------------------------')
    print('CATEGORIES')
    print('----------')
    print(categories_arr)
    print('-----------------------------------------------------------------------------------------------------')
    print('STATS')
    print('-----')
    print(stats_arr)
    print('LEN:', len(stats_arr))
    print('-----------------------------------------------------------------------------------------------------')
    print('COMBINED')
    print('--------')
    print(combined_arr)
    print('LEN:', len(combined_arr))
    print('-----------------------------------------------------------------------------------------------------')
    print('DATAFRAME')
    print('---------')
    print(stats_df)
    page_text = soup.get_text(separator='\n', strip=True)
    # print(page_text)
    

    #page_text = page_text.split('\n')