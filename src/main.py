from MachLearnModule.cluster_network import  ClusterNetwork as cluster
from SpotifyModule.spotifyHandler import SpotifyHandler as spotify
from CrawlerModule.WebCrawler import WebCrawler as crawler


from flask import Flask, render_template
from flask.globals import request
from werkzeug.utils import redirect




flask_app = Flask(__name__)

    


'''
init spotify account
init kmean network
'''
spoty = spotify()
songs = []
clust = cluster()
craw = crawler()

hot_songs = craw.get_songs_from_tabel()
print(hot_songs)
is_in_hot_list = ''
recommend=""
search_string = ''

def get_recommend(search_id):
    print('search_id',search_id)
    if search_id != 'search_song':
        res = spoty.get_title_features(search_id)
        result = clust.get_cluster_from_new_input(res)
        result = list(result)
        return 'https://open.spotify.com/embed/track/'+result[0]+'?utm_source=generator'


r = spoty.search_for_song('heros david')

res =spoty.get_title_features(r[0][-1])[0]

songs.append('https://open.spotify.com/embed/track/'+res['id']+'?utm_source=generator')    
#songs_id.append(res['id'])
@flask_app.route('/', methods=['GET','POST'])
def index():
    search_string = ''
    
    if request.method == 'POST':
        if request.form['button'] == 'search_song':
            search_string = request.form['search_text']
            res = spoty.search_for_song(search_string)
            songs.clear()
            for r in res:
                songs_id = r[-1].split(':')[-1]
                songs.append(["https://open.spotify.com/embed/track/"+r[-1].split(':')[-1]+"?utm_source=generator", songs_id])
            
        if request.form.get('button'):
            res_id = request.form['button']
            recommend = get_recommend(res_id)
        if str(search_string).lower() in hot_songs:
                is_in_hot_list = 'Yeahh, hot list'
        else:
            is_in_hot_list = ''
        return render_template('home.html', 
        title = "Music Referender",
        description="Smart page for music recomandation",
        hotlist=is_in_hot_list,
        songs=songs,
        recommend=recommend
        )

    else:        
        return render_template( 
        'home.html', 
        title = "Music Referender",
        description="Smart page for music recomandation",
        songs=songs
        )




if __name__ == "__main__":
    flask_app.run(debug=True)