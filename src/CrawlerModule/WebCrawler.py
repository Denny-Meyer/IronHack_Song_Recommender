# import libraries
from bs4 import BeautifulSoup
import requests as req
import pandas as pd
from random import randrange
import os
import time

class WebCrawler():

    # set const value
    hundred_songs_url = 'https://www.billboard.com/charts/hot-100/'  


    def __init__(self) -> None:
        self.music_table = None
        pass
    

    def search_hundred_songs_page(self):
        url = self.hundred_songs_url
        response = req.get(url=url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # run throug data
        data_complete = []

        for ultag in soup.find_all('ul', {'class': 'o-chart-results-list-row'}):

            data = []
            for litag in ultag.find_all('li', {'class': 'o-chart-results-list__item'}):
                    label = litag.findAll(class_='c-label')
                    for i in label:
                        d = i.text.strip('\n')
                        data.append(d)
                    title = litag.findAll(class_='c-title')
                    for t in title:
                        data.append(t.text.strip('\n'))
            #print(data)
            data_complete.append(data)
        
        self.music_table = pd.DataFrame(columns=['song','artist','last_week', 'peak_pos', 'wks_on_chart', 'featured'])


        # reason for counting backwards in data_complete
        # if element holds 'NEW' value, all elements seems to be shifted, in this case one list elements holds 10 instant of 8 items


        for entry in data_complete:
            row = {'song': entry[-7],'artist': entry[-8], 'last_week': entry[-6], 'peak_pos': entry[-5], 'wks_on_chart': entry[-4]}
            if entry[1] == 'NEW':
                row['featured'] = 'new'
            elif entry[1] == 'RE-\nENTER':
                row['featured'] = 'reenter'
            else:
                row['featured'] = '-'   
            self.music_table.loc[entry[0]] = row
        
        
        self.music_table['song'] = self.music_table['song'].str.lower()
        self.music_table['artist'] = self.music_table['artist'].str.lower()
        pass
    
    def get_artists_from_table(self) -> list:
        #print(self.music_table['artist'].unique())
        return self.music_table['artist']
        pass

    def search_web_page(self, url_name):
        pass

    
    def store_data_in_csv(self, filename='../data/song_list.csv'):
        if self.music_table.notna:
            self.music_table.to_csv(filename)
        pass
    

    def load_data_from_csv(self, filename='../data/song_list.csv') -> bool:
        if os.path.isfile(filename):
            # check modify time - if older 7 days should fetch from internet
            #print('file time ',os.path.getctime(filename) - time.localtime)
            if os.path.getmtime(filename) > 252000:
                self.music_table = pd.read_csv(filename)

            return True
        else:
            print('no file found, please create new data file')
        return False
