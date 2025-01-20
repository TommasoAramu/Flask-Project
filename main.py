from flask import Flask, request, render_template, redirect
import os, json, random

template_dir = os.path.abspath("./templates")
app = Flask(__name__, template_folder=template_dir)

songnames = ['VivaLaVida', '24KMagic', 'APT', 'Pompeii']
streams = ['20.000', '100.000','2.000.000', '400', '700.000' ]

class Song:
    def __init__(self, id, songName, songStreams):
        self.id = id
        self.songName = songName
        self.songStreams = songStreams

    def GetID(self):
        return self.id
    
    def GetSongName(self):
        return self.songName
    
    def GetSongStreams(self):
        return self.songStreams
        
# http://127.0.0.1:5000
@app.route('/', methods=['GET'])
def index():
    with open('./db/songs.json', 'r') as file:
        songList = json.load(file)

    listaCanzoni = []

    for s in songList:
        listaCanzoni.append(Song(s['id'], s['songName'], s['songStreams']))

    return render_template('index.html', songs=listaCanzoni)








@app.route('/new', methods=['POST'])
def add_song():
    with open('./db/songs.json', 'r') as file:
        data = json.load(file)
    
    lastSongId = data[-1]['id'] + 1 if data else 1

    newSong = Song(lastSongId, random.choice(songnames), random.choice(streams))
        
    data.append(newSong.__dict__)
    
    # Salva il file JSON aggiornato
    with open('./db/songs.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

    return redirect('/')