# Esploro

A collection of tools used for the migration of assets in BePress to Esploro. For questions contact Tim Norris at tnorris@miami.edu.

## org_converter_tiered.py
this takes the employee grouping table and turns into a tiered (unit to subunit) xml structure

## researcher_cleanup.py
this takes the researcher feeds and removes blank and duplicate affiliations, and soon to map existing academic units to employee grouping.

## getOAI.py  
getOAI.py harvests all metadata from an OAI-PMH endpoint (in this case a BePress instance).  

Usage: > python getOAI.py url [parameters]  

  - url: domain of OAI-PMH server, example: scholarlyrepository.miami.edu  
  - parameters (optional): addition parameters to pass to the OAI-PMH endpoint, example: '&metadataPrefix=document-export&set=publication:um_research_publications'  
  - NOTE: because there are '&' characters in the parameters string, you must use singles quotes around the parameters string.  

Output: by default the script will create a file YYYYMMDD_OAI.xml in the directory that you run the script.

## FeedAnalysis.ipynb
This jupyter notebook has several scripts for analyzing xml produced from a workday feed. You will need to have anaconda/jupyter installed (get the python 3.7 version from [https://www.anaconda.com/distribution/](https://www.anaconda.com/distribution/)).
  
  
## S3.ipynb
This jupyter notebook contains several scripts to verify and manipulate file names in the S3 bepress dump. You will need to have jupyter installed (get the python 3.7 version from [https://www.anaconda.com/distribution/](https://www.anaconda.com/distribution/)). You will also need the Boto3 library ('pip install boto3' in shell).