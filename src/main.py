import pandas
from CrawlerModule.WebCrawler import WebCrawler as crawler
from ServerModule.CrawlerServer import application as app
from SongManageModule.song_manage import Song_Mangaer as smang
from SpotifyModule.spotifyHandler import SpotifyHandler as spoti

import os
import pandas as pd


class Programm:

    

    def __init__(self) -> None:
        self.server = None
        self.crawl = None
        self.spoti_app = spoti()    
        pass


    def start_server(self):
        server = app()
        server.run()
        pass


    def start_web_crawler(self):
        self.crawl = crawler()
        if self.crawl.music_table == None:
            if not self.crawl.load_data_from_csv():
                self.crawl.search_hundred_songs_page()
                self.crawl.store_data_in_csv()
        #print(self.crawl.music_table)
        pass
    

    def run_program(self):
        self.start_web_crawler()
        #self.create_data_from_table(self.crawl.music_table)
        self.create_data_from_playlist()
        #self.start_server()



    def create_data_from_table(self, table):
        res = list(self.crawl.get_artists_from_table())
        set_res = set(res)
        for name in set_res:
            print('create for',name)
            self.spoti_app.create_csv_from_artist(name)
        
    
    def create_data_from_playlist(self, filename='../data/spotify_top.txt'):
        with open(filename) as f:
            play_list_ids = f.readlines()

            ids = []
            for i in play_list_ids:
                id_raw = i.strip()
                if id_raw.startswith('http'):
                    id_raw = id_raw.split('/')[-1]
                    id_raw = id_raw.rsplit('?')[0]
                    i = id_raw
                
                ids.append(i)

            results = []
            for id in ids:
                results.extend(self.spoti_app.get_artist_from_playlist(str(id)))
            
            art_list = set(results)
            for art in art_list:
                print('create for',art)
                self.spoti_app.create_csv_from_artist(art)



class TestClass:

    def concate_all_csv(self, folder = '../data/artist_data/'):
        f = os.listdir(folder)
        files = []
        for i in f:
            if i.endswith('.csv'):
                files.append(i)
        frames = []
        print('number of csv files',len(files))
        for elem in files:
            d = pd.read_csv(folder + elem)
            d.drop(columns='Unnamed: 0')
            frames.append(d)
        
        res = pd.concat(frames, ignore_index=True )
        print(res)


if __name__ == '__main__':
    TestClass().concate_all_csv()
    #Programm().run_program()