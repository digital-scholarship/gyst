# scrapes the website for the CESSDA SAW Capability Maturity Model
# and stores it in a json file

# @author Peter Neish

import lxml.html as LH
import requests



startpage = "https://cessda.net/eng/CESSDA-Services/Projects/Current-projects/CESSDA-SaW/Work-Packages/WP3/CESSDA-CDM/Part-1-CRA1-Organisational-Infrastructure"
base = "https://cessda.net"

outputfile = "model.json"
data = {}
level = ''
maxpage = 3 
current = 0


def parsePage(url):
    global current
    global maxpage
    current = current + 1
    page = requests.get(url)
    tree = LH.fromstring(page.content)
   
    # remove blank elements
    for element in tree.iter("*"):
        if element.text is not None and not element.text.strip():
            element.text = None

    # remove the table of contents on each page
    for toc in  tree.xpath('//div[@id="toc"]'):
        toc.getparent().remove(toc)
    
    
    level = tree.xpath('//h1[contains(text(),"CRA")]/text()')
    h3 = tree.xpath('//h3/text()')

    print tree.xpath('//h1/text()')

    h3 = tree.xpath('//h3')

    for e in h3[0].itersiblings("p"):
        print(e)
    
    print tree.xpath('//h2/text()')
    print tree.xpath('//h3/text()')
    print tree.xpath('//h4/text()')
    print tree.xpath('//h5/text()')

    print ("\n\n")

    n = tree.xpath('//a[contains(text(),"Next")]')
    if(n):
         link = n[0].get('href')
         if current < maxpage:
            parsePage(base + link)
           


parsePage(startpage)


