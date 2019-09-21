import sys
import requests
import xml.etree.ElementTree as ET
import datetime

def getOAI(url,params=''):

    page = 1
    print ('page:', page)

    ET.register_namespace('oai','http://www.openarchives.org/OAI/2.0/')

    url = "https://" + url + "/do/oai/?verb=ListRecords"
    response = requests.get(url+params)

    allXML = ET.fromstring(response.content.decode('utf-8'))

    documentlist = allXML.find('{http://www.openarchives.org/OAI/2.0/}ListRecords')
    resume = documentlist.find('{http://www.openarchives.org/OAI/2.0/}resumptionToken')
    documentlist.remove(resume)
    resume = resume.text

    while not resume == None:
        page += 1
        print ('page:',page)
        response = requests.get(url+'&resumptionToken='+resume)
        pageXML = ET.fromstring(response.content.decode('utf-8'))
        pagelist = pageXML.find('{http://www.openarchives.org/OAI/2.0/}ListRecords')
        resume = pagelist.find('{http://www.openarchives.org/OAI/2.0/}resumptionToken')
        pagelist.remove(resume)
        resume = resume.text
        documentlist.extend(pagelist)
        
    root = ET.ElementTree(allXML)
    today = datetime.datetime.now().isoformat()[0:10].replace('-', '')
    root.write(today+'_OAI.xml',encoding="utf-8",xml_declaration=True)

if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == 'help':
      print("""
        getOAI.py harvests all metadata from an OAI-PMH endpoint.
        Usage: python getOAI url [parameters]
          url: domain of OAI-PMH server, example: scholarlyrepository.miami.edu
          parameters (optional): addition parameters to pass to the OAI-PMH endpoint, example: '&metadataPrefix=document-export&set=publication:um_research_publications'
          NOTE: because there are '&' characters in the options, you must use singles quotes around the options string.
        Output: by default the script will create a file YYYYMMDD_OAI.xml in the directory that you run the script.
        """)
      sys.exit()
    params = ''
    url = sys.argv[1]
    if len(sys.argv) == 3:
      params = sys.argv[2]
    getOAI(url, params)
