# Esploro

## org_converter_tiered.py
this takes the employee grouping table and turns into a tiered (unit to subunit) xml structure

## researcher_cleanup.py
this takes the researcher feeds and removes blank and duplicate affiliations, and soon to map existing academic units to employee grouping.

## getOAI.py  
getOAI.py harvests all metadata from an OAI-PMH endpoint.  

Usage: > python getOAI.py url [parameters]  

  - url: domain of OAI-PMH server, example: scholarlyrepository.miami.edu  
  - parameters (optional): addition parameters to pass to the OAI-PMH endpoint, example: '&metadataPrefix=document-export&set=publication:um_research_publications'  
  - NOTE: because there are '&' characters in the parameters string, you must use singles quotes around the parameters string.  

Output: by default the script will create a file YYYYMMDD_OAI.xml in the directory that you run the script.  