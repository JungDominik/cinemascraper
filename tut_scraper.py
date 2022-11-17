import requests
from bs4 import BeautifulSoup

url = "https://realpython.github.io/fake-jobs/"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

job_elements = soup.find_all("div", class_ = 'card-content')

for job_element in job_elements:
    title_element = job_element.find("h2", class_ = "title")
    company_element = job_element.find("h3", class_ = "company")
    location_element = job_element.find("p", class_ = "location")
    
    
    
    print ('\n')
    print (title_element.text.strip())
    print (company_element.text.strip())
    print (location_element.text.strip())

#H2 elemente filtern, HTML-Strukturclutter entfernen, nur den reinen content anzeigen
pythonjobs = soup.find_all(             
    "h2", 
    string= lambda text: "ython" in text.lower()        #The normal search is for exact strings --> Text needs the lambda approach
    )


for job in pythonjobs:
    job = job.find('h2', class_ = "title is-5")
    print (job.parent.text)