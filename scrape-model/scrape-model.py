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
maxpage = 500
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

    print "running parsePage. Current is: " + str(current)
    global current
    global maxpage
    global data
    global temp_cra

    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")
    temp_cpa = {}

    current = current + 1

    # remove blank elements
    print "removing blanks"
    for x in soup.find_all():

        if len(x.text) == 0:
            x.decompose()

        if re.match(r"/^\s*$/", x.text):
            x.decompose()

    for x in soup.findAll(lambda tag: not tag.contents and (tag.string is None or not tag.string.strip())):
        x.decompose()

    # remove the table of contents on each page
    for toc in soup.find_all("div", id_="toc" ):
        toc.decompose()

    soup.find('p', class_='last-updated').decompose()

    # start parsing document - get h1 first
    for h1 in soup.find_all('h1'):

        print "looping through h1"

        # we have a CRA main page
        if re.search(r"^Part", h1.text):

            print "found CRA"

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
        elif re.search(r"^CPA", h1.text):
            print "found CPA"
            temp_cpa = {}
            temp_cpa['cpa'] = h1.text
            temp_cpa['objectives'] = []
            print h1.text

            # now get the h3s
            for h3 in h1.find_next_siblings("h3"):

                print "looping through h3"
                
                if h3.text.startswith("Purpose"):
                    temp_cpa['purpose'] = getPara(h3)
                    continue

                if re.search(r"^CC", h3.text):
                    temp_cpa['completeness'] = h3.text
                    temp_cpa['completeness_def'] = h3.find_next_sibling("ol").text
                    

                # now get level 4 - objectives
                for h4 in h3.find_next_siblings("h4"):

                    print "looping though h4"
                    temp_objective = {}

                    print "objective: " + h4.text

                    if re.search(r"^[SG]O", h4.text):
                        temp_objective['objective'] = h4.text
                        temp_objective['objective_def'] = getPara(h4)
                        temp_objective['activities'] = []
                        objnum = re.search(r"\d.\d.\d", h4.text)
                        if objnum:
                            #temp_objective['objective_num'] = objnum.group(0)
                            print objnum.group(0)

                        # parse the objective parts
                        objparts = re.search(r"(.*)(\d.\d.\d.):(.*)", h4.text)
                        if objparts:
                            temp_objective['objective_code'] = objparts.group(1)
                            temp_objective['objective_num'] = objparts.group(2)
                            temp_objective['objective_title'] = objparts.group(3)

                            


                        # and now the level 5s the Activities
                        for h5 in h4.find_next_siblings("h5"):
                            print "looping through h5"
                            temp_activity = {}
                            if re.search(r"^\s*$", h5.text):
                                continue

                            # pull out activity components 
                            num = re.search(r"(.*)(\d.\d.\d)(.\d):(.*)", h5.text)

                            if num:
                                temp_activity['activity_abbr'] = num.group(1)
                                temp_activity['activity_code'] = str(num.group(2)) + str(num.group(3))
                                temp_activity['activity_title'] = num.group(4)

                                print temp_activity

                            # we will check that the activity matches the objective
                            if num and objnum and num.group(2) != objnum.group(0):
                                print "skipped"
                                continue

                            print h5.text

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
                        # we'll only add it if it isn't already in
                        if not any(d.get('objective', None) == temp_objective['objective'] for d in temp_cpa['objectives']):
                            print "no objective"
                            temp_cpa['objectives'].append(temp_objective)
                    temp_objective = {}
            temp_cra['cpas'].append(temp_cpa)
            temp_cpa={}
        print "\n\n" 
    
    n = soup.find('a',string=re.compile('^Next*'))

    if(n):
         link = n.get('href')
         if current < maxpage and link:
            parsePage(base + link)
          
# let's kick this thing off
parsePage(startpage)

data.append(temp_cra)

# dump to a json file
with open('cessda_model.json', 'w') as outfile:
    json.dump(data, outfile)

