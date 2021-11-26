from MachLearnModule.cluster_network import  ClusterNetwork as cluster
from SpotifyModule.spotifyHandler import SpotifyHandler as spotify


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

r = spoty.search_for_song('heros david')

res =spoty.get_title_features(r[0][-1])[0]

songs.append('https://open.spotify.com/embed/track/'+res['id']+'?utm_source=generator')    
    
@flask_app.route('/', methods=['GET','POST'])
def index():
    
    
    if request.method == 'POST':
        if request.form['button'] == 'add song':
            songs.append("https://open.spotify.com/embed/track/7tthMTxuAH4G0WkQkiT3t2?utm_source=generator")
        if request.form['button'] == 'drop':
            if len(songs) > 0:
                songs.pop()
        return render_template('home.html', 
        title = "Music Referender",
        description="Smart page for music recomandation",
        songs=songs)
    else:        
        return render_template( 
        'home.html', 
        title = "Jinja Demo Site",
        description="Smarter page templates with Flask & Jinja.",
        songs=songs)




if __name__ == "__main__":
    flask_app.run(debug=True)