import requests
import json
from bs4 import BeautifulSoup

url = 'https://www.yorck.de/en/films'
request = requests.get(url)

soup = BeautifulSoup (request.content, 'lxml')

#print(soup.prettify())

list_h3s = (soup.find_all('h3', {'class':'whatson-film-title'}))
nameslist = []
for h3 in list_h3s: 
    nameslist.append(h3.getText())
#print (nameslist)

list_spans = soup.find_all('span', {'class' : 'MuiTypography-label'})
labels = []
for span in list_spans:
    labels.append (span.getText())

#print (labels)


list_h4 = soup.find_all('h4', {'class' : 'MuiTypography-root MuiTypography-h4 css-14z9z3z'})
times = []
for h4 in list_h4: 
    times.append (h4.getText())
print (len(times))
print(times)



## Extract movies Json
datajson = soup.find("script", id = "__NEXT_DATA__").text

processed = json.loads(datajson)

filmlist = processed.get('props').get('pageProps').get('films')

filmfields = []

for film in filmlist: filmfields.append(film.get('fields'))

sampleentry = filmfields[0]

movietitle = sampleentry.get('title')

examplemoviesessions = sampleentry.get('sessions')

onesession = examplemoviesessions[0]

starttime = onesession.get('fields').get('startTime')
cinemaname = onesession.get('fields').get('cinema').get('fields').get('name')

def get_allmovies():
    allmovies = []
    for film in filmfields:
        movietitle = film.get('title')
        allmovies.append(movietitle)
    return allmovies

def show_allmovies():
    currentmovies = get_allmovies()
    currentmovies.sort()
    for i in range (len(currentmovies)):
        print ('{}. {}'.format(i, currentmovies[i]))


def get_times(searchmovie): #Works, refactor / aufteilen in Teilfunktionen
    sessionsforfilm = []
    for film in filmlist:
        if film.get('fields').get('title') == searchmovie:
            sessionsforfilm = film.get('fields').get('sessions')
    print('numberofsessions')
    print (len(sessionsforfilm))
    for session in sessionsforfilm:
        starttime = session.get('fields').get('startTime')
        print (starttime)

    #search the right datastructure for the searchmovei
    # print the times