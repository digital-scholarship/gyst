# scrapes the website for the CESSDA SAW Capability Maturity Model
# and stores it in a json file

# @author Peter Neish

import lxml.html as LH
import requests



startpage = "https://cessda.net/eng/CESSDA-Services/Projects/Current-projects/CESSDA-SaW/Work-Packages/WP3/CESSDA-CDM/Part-1-CRA1-Organisational-Infrastructure"

outputfile = "model.json"

data = {}
level = ''


def parsePage(url):
    page = requests.get(url)
    tree = LH.fromstring(page.content)
    
    for toc in  tree.xpath('//div[@id="toc"]'):
        toc.getparent().remove(toc)
    
    
    if(tree.xpath('//h1[contains(text(),"CRA")]')):
        level = tree.xpath('//h1[contains(text(),"CRA")]/text()')
        h3 = tree.xpath('//h3/text()')
        print h3

parsePage(startpage)


