from flask import Flask, request, render_template, redirect
import os
import json

template_dir = os.path.abspath("./templates")
app = Flask(__name__, template_folder=template_dir)

songnames = ['VivaLaVida', '24KMagic', 'APT', 'Pompeii']

class Song:
    def __init__(self, id, songName):
        self.id = id
        self.songName = songName

    def GetID(self):
        return self.id
    
    def GetSongName(self):
        return self.songName
        
# http://127.0.0.1:5000
@app.route('/', methods=['GET'])
def index():
    with open('./db/songs.json', 'r') as file:
        songList = json.load(file)

    listaCanzoni = []

    for s in songList:
        listaCanzoni.append(Song(s['id'], s['songName']))

    return render_template('index.html', songs = listaCanzoni)