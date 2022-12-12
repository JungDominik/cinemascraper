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

#filmlist = processed.get('props').get('pageProps').get('films')
filmlist = processed['props']['pageProps']['films']

filmobjects = []
for film in filmlist: filmobjects.append(film['fields'])

sampleentry = filmobjects[0]
movietitle = sampleentry['title']
examplemoviesessions = sampleentry['sessions']
onesession = examplemoviesessions[0]
starttime = onesession['fields']['startTime']
cinemaname = onesession['fields']['cinema']['fields']['name']

def get_allmovies():
    allmovies = []
    for film in filmobjects:
        movietitle = film['title']
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
        if film['fields']['title'] == searchmovie:
            sessionsforfilm = film['fields']['sessions']
    print('numberofsessions')
    print (len(sessionsforfilm))
    for session in sessionsforfilm:
        starttime = session['fields']['startTime']
        print (starttime)

    #search the right datastructure for the searchmovei
    # print the times


def fillSessionDetails(): #Go-through-datastructure-method
    import pandas as pd
    df_sessiondetails = pd.DataFrame(columns = ['Film', 'Cinema','Starttime']) 

    numberfilms = len (filmobjects)
    for film in filmobjects:
        #print(film.keys())
        filmtitle = film['title']
        filmsessions = film['sessions']
        numbersessions = len (filmsessions)
        for i in range (numbersessions):
            sessionstartdate = filmsessions[i]['fields']['startTime']
            sessioncinema = filmsessions[i]['fields']['cinema']['fields']['name']
            #print ('{0} - {1} - {2}'.format(filmtitle, sessionstartdate, sessioncinema))
            #df_sessiondetails = df_sessiondetails.append([[filmtitle, sessioncinema, sessionstartdate],])

            #new_row = {'Film': filmtitle, 'Cinema':sessioncinema, 'Starttime':sessionstartdate}
            #df_sessiondetails =df_sessiondetails.append(new_row, ignore_index = True)
            
            new_row = pd.DataFrame({'Film': filmtitle, 'Cinema':sessioncinema, 'Starttime':sessionstartdate}, index = [0])
            df_sessiondetails = pd.concat([new_row, df_sessiondetails.loc[:]]).reset_index(drop=True)
    df_sessiondetails.sort_values(by = ['Film', 'Starttime'])

    return df_sessiondetails
    # TODO: Take from the data structure, fill into a pandas dataframe (append as new row at the bottom)

def findfilmsessions(film):
    return fillSessionDetails().query("Film == @film")