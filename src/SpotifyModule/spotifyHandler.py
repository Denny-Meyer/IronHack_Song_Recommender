import os
from typing import Dict
from pandas.core import frame
import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint


# testining 
import pandas as pd

import config

class SpotifyHandler:

    
    def __init__(self) -> None:
        # setup connection to spotify
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= config.client_id,
                                                           client_secret= config.client_secret))
        if self.sp == None:
            print('could not connect to spotify')
        pass

    
    def get_artist_from_playlist(self, playlist) -> list:
        res = self.sp.playlist_tracks(playlist_id=playlist)
        artist_list = []
        for art_id in res['items']:
            if art_id['track'] == None:
                continue
            artist_list.append(art_id['track']['album']['artists'][0]['name'])
        return artist_list


    def get_albums_ids_from_artist(self, artist_name, market = 'GB'):
        album_ids = {}
        
        res = self.sp.search(q=artist_name, type='artist',  market= market) #,
        if res['artists']['total'] == 0:
            print('no entries found for:', artist_name)
            return None

        art_name = res['artists']['items'][0]['name']
        art_id = res['artists']['items'][0]['id']
        albums = self.sp.artist_albums(art_id)
        if albums == None:
            print('no album found for', art_name)
            return None

        for elem in albums['items']:
            album_ids[elem['name']] = elem['uri']
        
        return {'album_ids':album_ids, 'artist_id' : art_id, 'artist_name': art_name}


    def get_album_image_ref(self, album_id) -> str:
        res = self.sp.album(album_id=album_id)['images'][-1]['url']
        return res
        
    
    def get_track_ids_from_album(self, album_id) -> dict:
        ids = {}
        res = self.sp.album(album_id= album_id)

        for track in res['tracks']['items']:
            ids[track['name']] = [track['uri']]
        return ids


    def get_title_features(self, title_name_ids):
        res = self.sp.audio_features(title_name_ids)
        return res


    def get_song_widget(self, title_name_id):
        pass


    # user requested search
    def search_for_song(self, song_title:str, artist_name = ''):
        res = None
        if artist_name == '':
            res = self.sp.search(q='track:' + song_title, type='track', limit=3)
        else:
            res = self.sp.search(q='track:' + song_title + ' artist:'+ artist_name , type='track', limit=3)
        req = []
        for i in res['tracks']['items']:
            req.append([i['name'], i['artists'][0]['name'], i['uri']])
        return  req
    


    
    def fetch_features_for_artist_name(self, artist_name : str)-> dict:

        features = []
    
        res  = self.get_albums_ids_from_artist(artist_name= artist_name)
        if res == None:
            return

        for alb_v in res['album_ids'].values():
            tracks = self.get_track_ids_from_album(album_id= alb_v)
            
            #print(tracks)
            for tra_k, tra_v in tracks.items():

            # get final dictionary
                f = self.get_title_features(title_name_ids= tra_v)[0]
                
                if f == None:
                    print('no features returned', tra_k)
                    continue

                # add useful data
                f['track_name'] = str(tra_k)
                f['track_id'] = str(tra_v[0])
                f['artist_name'] = str(res['artist_name'])
                f['artist_id'] = str(res['artist_id'])
                features.append(f)

        return {'features':features, 'artist_name' :res['artist_name']}


    def create_csv_from_artist(self, artist_name: str):
        
        file_name = artist_name.replace('/','-')
        print('file_name:',file_name)

        if not os.path.isfile('../data/artist_data/' + file_name + '.csv'):
            res = self.fetch_features_for_artist_name(artist_name= artist_name)
            if res == None:
                return
            
            frame = pd.DataFrame(res['features'])
            frame.to_csv('../data/artist_data/' + file_name + '.csv')
        else:
            print('artist:', artist_name, 'allready stored')
        