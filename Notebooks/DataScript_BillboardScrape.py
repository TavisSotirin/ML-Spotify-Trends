import requests
import time

def readFile(data):
   song_delim = '<div class="ye-chart-item__title">'
   artist_delim = '<div class="ye-chart-item__artist">'
   rank_delim = '<div class="ye-chart-item__rank">'
   divider = '<a href="'
   
   songs = []
   curSong = ["","",""]
   nextLine = False

   for line in data:
        if line.find(song_delim) != -1 or line.find(artist_delim) != -1 or line.find(rank_delim) != -1:
            nextLine = True
            continue
        elif nextLine and line.find(divider) != -1:
            continue
        elif nextLine:
            if curSong[0] == '':
                curSong[0] = line.replace('\n','')
            elif curSong[1] == '':
                curSong[1] = line.replace('\n','')
            else:
                curSong[2] = line.replace('\n','')
                songs.append(curSong)
                curSong = ["","",""]
            
            nextLine = False
   
   return songs
   
def pullSongs(inTuple, songOutF):
    path = inTuple[0]
    genre = inTuple[1]
    startYear = inTuple[2]
    endYear = inTuple[3]
    
    print(genre,startYear,endYear,"\n----------------")
    
    url1 = 'https://www.billboard.com/charts/year-end/'
    songs = []
    
    for year in range(startYear,endYear+1):
        time.sleep(5)
        
        url = url1 + str(year) + path
        page = requests.get(url)
        
        with open('scrapeOut.txt','w') as f:
            for line in page.text:
                try:
                    f.write(line)
                except:
                    #ignore except error for unidentified characters in html code
                    pass
            
        with open('scrapeOut.txt','r') as f:
            songs = readFile(f)
            print(genre,year,len(songs))
            
            for i,track in enumerate(songs):  
                out = '\t'.join([genre,str(year),track[0],track[1].replace('&#039;','\'').replace('&amp;','&'),track[2].replace('&#039;','\'').replace('&amp;','&')])
                songOutF.write(out + '\n')
                                
# Manually define/add to func call loop
country = ('/hot-country-songs',"Country",2002,2020)
jazz = ('/smooth-jazz-songs',"Jazz",2006,2020)
latin = ('/hot-latin-songs',"Latin",2006,2020)
pop = ('/pop-songs',"Pop",2008,2020)
rb = ('/hot-r-and-and-b-hip-hop-songs',"R&B",2002,2020)

dataOut = open('billboardData.txt','w')
dataOut.write('\t'.join(['Genre','Year','Position','Song','Artist']))
dataOut.write('\n')

for genre in [country,jazz,latin,pop,rb]:
    pullSongs(genre, dataOut)
    # Wait between website requests to avoid being rejected by the server
    time.sleep(30)
    
dataOut.close()