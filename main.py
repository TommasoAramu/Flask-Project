from flask import Flask, request, render_template, redirect
import os, json, random

template_dir = os.path.abspath("./templates")
app = Flask(__name__, template_folder=template_dir)

songnames = ['Viva La Vida', '24 KMagic', 'APT', 'Pompeii', 'Despacito', 'See You Again', 'Shape of You', 'Uptown Funk', 'Sugar', 'Waka Waka', 'Faded', 'Girls Like You', 'Hello', 'Stressed Out']
streams = ['10.000.000', '9.000.000','8.000.000', '7.000.000', '6.000.000', '5.000.000', '4.000.000', '3.000.000', '2.000.000', '1.000.000', '900.000', '800.000', '700.000', '600.000', '500.000', '400.000', '300.000', '200.000', '100.000']

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
    
    with open('./db/songs.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

    return redirect('/')


@app.route('/edit', methods=['GET'])
def edit_song():

    song_id = request.args.get('id')

    if not song_id:
        return "Errore: parametro 'id' mancante", 400

    try:
        song_id = int(song_id)
    except ValueError:
        return "Errore: parametro 'id' non valido", 400

    with open('./db/songs.json', 'r') as file:
        data = json.load(file)

    song_to_edit = next((song for song in data if song['id'] == song_id), None)

    if not song_to_edit:
        return "Errore: canzone non trovata", 404

    return render_template('edit.html', song=song_to_edit)


@app.route('/update', methods=['POST'])
def update_song():

    song_id = request.form.get('id')
    song_name = request.form.get('songName')
    song_streams = request.form.get('songStreams')

    if not song_id or not song_name or not song_streams:
        return "Errore: dati mancanti", 400

    try:
        song_id = int(song_id)
    except ValueError:
        return "Errore: ID non valido", 400

    with open('./db/songs.json', 'r') as file:
        data = json.load(file)

    for song in data:
        if song['id'] == song_id:
            song['songName'] = song_name
            song['songStreams'] = song_streams
            break
    else:
        return "Errore: canzone non trovata", 404

    with open('./db/songs.json', 'w') as file:
        json.dump(data, file, indent=4)

    return redirect('/')


@app.route('/delete', methods=['POST'])
def delete_song():   
    song_id = request.form.get('id')

    if not song_id:
        return "Errore: parametro 'id' mancante", 400

    try:
        song_id = int(song_id)
    except ValueError:
        return "Errore: parametro 'id' non valido", 400

    with open('./db/songs.json', 'r') as file:
        data = json.load(file)

    updated_data = [song for song in data if song['id'] != song_id]

    if len(data) == len(updated_data):
        return "Errore: canzone non trovata", 404

    with open('./db/songs.json', 'w') as file:
        json.dump(updated_data, file, indent=4)

    return redirect('/')
