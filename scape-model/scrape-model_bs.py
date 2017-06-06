# scrapes the website for the CESSDA SAW Capability Maturity Model
# and stores it in a json file

# @author Peter Neish

import requests
import re
import json
from bs4 import BeautifulSoup

startpage = "https://cessda.net/eng/CESSDA-Services/Projects/Current-projects/CESSDA-SaW/Work-Packages/WP3/CESSDA-CDM/Part-1-CRA1-Organisational-Infrastructure"
base = "https://cessda.net"

outputfile = "model.json"
data = []
maxpage = 100 
current = 0
temp_cra = {}


# returns the text from any following paragraphs up to the next heading
def getPara(start):
    #global soup
    ret = ""
    for el in start.find_next_siblings():
        if el.name.startswith('h'): 
            break
        if el.name == 'p':
            ret += el.text
    return ret

# main page parsing function - called recursively
def parsePage(url):
    global current
    global maxpage
    global data
    global temp_cra

    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")

    current = current + 1

    # remove blank elements
    for x in soup.find_all():

        if len(x.text) == 0:
            x.extract()

    # remove the table of contents on each page
    for toc in soup.find_all("div", id_="toc" ):
        toc.decompose()

    soup.find('p', class_='last-updated').extract()

    # start parsing document - get h1 first
    for h1 in soup.find_all('h1'):

        # we have a CRA main page
        if re.search(r"^Part", h1.text):

            # put any existing CRAs into our data array
            if(len(temp_cra) > 0):
                data.append(temp_cra)
            temp_cra = {}
            temp_cra['cra'] = h1.text
            temp_cra['cpas'] = []

            for h3 in h1.find_next_siblings("h3"):
                if h3.text.startswith('High'):
                    temp_cra['description'] = getPara(h3)

        # we have a CPA page       
        if re.search(r"^CPA", h1.text):
            temp_cpa = {}
            temp_cpa['cpa'] = h1.text
            temp_cpa['objectives'] = []
            print h1.text

            # now get the h3s
            for h3 in h1.find_next_siblings("h3"):

                if re.search(r"^CC", h3.text):
                    temp_cpa['completeness'] = h3.text
                    temp_cpa['completeness_def'] = h3.find_next_sibling("ol").text
                    
                if h3.text.startswith("Purpose"):
                    temp_cpa['purpose'] = getPara(h3)

                # now get level 4 - objectives
                for h4 in h3.find_next_siblings("h4"):
                    if re.search(r"^[SG]O", h4.text):
                        temp_objective = {}
                        temp_objective['objective'] = h4.text
                        temp_objective['objective_def'] = getPara(h4)
                        temp_objective['activities'] = []

                        # and now the level 5s the Activities
                        for h5 in h4.find_next_siblings("h5"):
                            temp_activity = {}
                            temp_activity['activity'] = h5.text
                            temp_activity['question'] = getPara(h5)
                            temp_activity['answers'] = []

                        
                            table =  h5.find_next_sibling("table")
                            if table:
                                td = table.findChildren("td")
                                temp_activity['answers'].append({'numeric': 0, 'value': td[0].text, 'definition': td[1].text})
                                temp_activity['answers'].append({'numeric': 1, 'value': td[2].text, 'definition': td[3].text})
                                temp_activity['answers'].append({'numeric': 2, 'value': td[4].text, 'definition': td[5].text})
                                temp_activity['answers'].append({'numeric': 3, 'value': td[6].text, 'definition': td[7].text})
                                temp_activity['answers'].append({'numeric': 4, 'value': td[8].text, 'definition': td[9].text})
                                temp_activity['answers'].append({'numeric': 5, 'value': td[10].text, 'definition': td[11].text})
                            temp_objective['activities'].append(temp_activity) 
                            temp_activity = {}
                        temp_cpa['objectives'].append(temp_objective)
                        temp_objective = {}
            temp_cra['cpas'].append(temp_cpa)
            temp_cpa={}
        print "\n\n" 
    
    n = soup.find('a',string=re.compile('^Next*'))


    if(n):
         link = n.get('href')
         if current < maxpage:
            parsePage(base + link)
          

parsePage(startpage)

data.append(temp_cra)

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)

