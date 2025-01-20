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



@app.route('/edit', methods=['GET'])
def edit_song():
    # Ottieni l'ID della canzone dalla richiesta GET
    song_id = request.args.get('id')

    if not song_id:
        return "Errore: parametro 'id' mancante", 400

    try:
        song_id = int(song_id)
    except ValueError:
        return "Errore: parametro 'id' non valido", 400

    # Leggi il file JSON e trova la canzone da modificare
    with open('./db/songs.json', 'r') as file:
        data = json.load(file)

    song_to_edit = next((song for song in data if song['id'] == song_id), None)

    if not song_to_edit:
        return "Errore: canzone non trovata", 404

    # Passa i dati della canzone al template edit.html
    return render_template('edit.html', song=song_to_edit)


@app.route('/update', methods=['POST'])
def update_song():
    # Ottieni i dati modificati dal form
    song_id = request.form.get('id')
    song_name = request.form.get('songName')
    song_streams = request.form.get('songStreams')

    if not song_id or not song_name or not song_streams:
        return "Errore: dati mancanti", 400

    try:
        song_id = int(song_id)
    except ValueError:
        return "Errore: ID non valido", 400

    # Leggi il file JSON e aggiorna la canzone
    with open('./db/songs.json', 'r') as file:
        data = json.load(file)

    for song in data:
        if song['id'] == song_id:
            song['songName'] = song_name
            song['songStreams'] = song_streams
            break
    else:
        return "Errore: canzone non trovata", 404

    # Salva il file JSON aggiornato
    with open('./db/songs.json', 'w') as file:
        json.dump(data, file, indent=4)

    # Reindirizza alla homepage
    return redirect('/')






@app.route('/delete', methods=['POST'])
def delete_song():
    # Ottieni l'ID della canzone dalla richiesta
    song_id = request.form.get('id')  # 'id' è il nome del parametro passato dal form

    if not song_id:
        return "Errore: parametro 'id' mancante", 400

    try:
        song_id = int(song_id)
    except ValueError:
        return "Errore: parametro 'id' non valido", 400

    # Leggi il file JSON
    with open('./db/songs.json', 'r') as file:
        data = json.load(file)

    # Cerca e rimuovi la canzone con l'ID specificato
    updated_data = [song for song in data if song['id'] != song_id]

    # Controlla se è stata effettivamente rimossa
    if len(data) == len(updated_data):
        return "Errore: canzone non trovata", 404

    # Scrivi il file JSON aggiornato
    with open('./db/songs.json', 'w') as file:
        json.dump(updated_data, file, indent=4)

    return redirect('/')
