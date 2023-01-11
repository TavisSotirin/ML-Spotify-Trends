import time
import random

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid = '8e7fbe2dfc9f48d1989e064569e7cc66'
secret = '63a94bfd5ce34713b0f30b67940baf17'

# Spotipy set up
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# Set up features and indices for song data array
features = ['track','searchTrack','searchArtist','artist','uri','lookupError','chartyear','genre','release_date','popular','key','explicit','mode','chartrank','acousticness','danceability','energy','duration_ms','instrumentalness','valence','tempo','liveness','loudness','speechiness','time_signature']
fIndex = {}

# Define splits in artist and track names that prevent spotify from searching correctly
artistSplits = ['with','featuring','&',',','duet']
trackSplits = ['\'']

numSongs = 0

for i,f in enumerate(features):
    fIndex[f] = i
	
def get_audio_features(songData):
    uri = songData[fIndex['uri']]
    
    songFeatures = sp.audio_features(uri)[0]
    
    for f in songFeatures:
        try:
            songData[fIndex[f]] = str(songFeatures[f])
        except:
            pass

    # Spotify request
    trackData = sp.track(uri)
    
    artists = ""
    for i,t in enumerate(trackData['artists']):
        if i < len(trackData['artists']) - 1:
            artists += t['name'] + ' /and/ '
        else:
            artists += t['name']
    
    songData[fIndex['searchArtist']] = artists
    songData[fIndex['searchTrack']] = trackData['name']
    songData[fIndex['release_date']] = trackData['album']['release_date']
    songData[fIndex['explicit']] = '1' if trackData['explicit'] else '0'
	
def set_song_uri(songData):
    songURI = ""
    
    name = songData[fIndex['track']].lower()
    artist = songData[fIndex['artist']].lower()
    
    for split in artistSplits:
        if artist.find(split) != -1:
            artist = artist.split(split)[0].strip()
        
    for split in trackSplits:
        if name.find(split) != -1:
            name = name.split(split)[0].strip()
    
    query = 'track:' + name + ' artist:' + artist
    
    # Grab song from chart year
    try:
        # Spotify request
        result = sp.search(q=query, type='track')
        songURI = result['tracks']['items'][0]['uri']
        
        songData[fIndex['uri']] = songURI
        songData[fIndex['lookupError']] = '0'
    except:
        # If unable to grab mark for reivew
        songData[fIndex['lookupError']] = '1'
		
def build_track_data(inFile,outFile,delim):
    outF = open(outFile,'w')

    with open(inFile,'r') as f:
        counter = 1
        
        for line in f:
            songData = [""]*len(features)
            
            genre,year,rank,track,artist = line.split('\t')

            # From billboard chart data
            songData[fIndex['chartyear']] = year.strip()
            songData[fIndex['genre']] = genre.strip()
            songData[fIndex['chartrank']] = rank.strip()
            songData[fIndex['track']] = track.strip()
            songData[fIndex['artist']] = artist.strip()
            songData[fIndex['popular']] = '1'

            # Avoid requesting data too frequently
            time.sleep(random.uniform(.25,.75))

            # Look up URI for spotify data
            set_song_uri(songData)

            # Get spotify data
            try:
                if songData[fIndex['lookupError']] != '1':
                    get_audio_features(songData)
                    print(str(counter) + "/" + str(numSongs) + " - GOT IT")
                else:
                    print(str(counter) + "/" + str(numSongs) + " - DO NOT GOT IT")
            except:
                print("Error retrieving",counter," - ",track,artist)
                outF.flush()
                
            out = ""
            counter += 1
            
            for i,v in enumerate(songData):
                if i < len(songData) - 1:
                    out += v + delim
                else:
                    out += v + '\n'
            
            try:
                outF.write(out)
            except:
                outF.flush()
                print("Error writing",counter," - ",out)
                
    outF.close()
	
inFile = 'billboardData.txt'

# For time delay sanity
with open(inFile,'r') as f:
    numSongs = len(f.read().split('\n'))

build_track_data(inFile,'outData.txt',';')