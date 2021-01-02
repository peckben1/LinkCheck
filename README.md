# LinkCheck

**PLEASE CHECK THE ROBOTS.TXT PAGE OF A SITE AND ENSURE THAT CRAWLING IS ALLOWED BEFORE PASSING THAT SITE AS THE ROOT URL FOR THIS SCRIPT**

## Guide to Files

- LinkCheck.ipynb: This is a quick script that takes a root url and a target url as input, then crawls the root url and logs all instances of links to the target url. This is extremely useful if you need to update or remove all instances of a link. The crawl does not follow external links and stays on the root domain, though the target link can be an external one. The crawl also excludes links which contain a query string (i.e. at least one instance of a question mark). 
- LinkCheckUntargeted.py: This script is a modification of LinkCheck which takes only a root url as an input (no target is necessary) and crawls the domain from there, checking all internal and external links which do not contain an ignored string (?, @, #, or javascript:) and logging any links which fail and the response codes received from failures. LinkCheckUntargeted.py currently does not work on pages rendered in JavaScript, though I'm working on using requests-html to add that functionality. This version is also a simple python script .py file and therefore does not require any version of Jupyter to run. 

## Requirements

To run properly, these scripts requires Python 3 and the following modules:
- JupyterLab or Jupyter Notebook (for LinkCheck.ipynb only)
- Requests
- bs4 (BeautifulSoup)
- the standard "time" and "sys" modules
