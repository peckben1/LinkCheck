# LinkCheck

**PLEASE CHECK THE ROBOTS.TXT PAGE OF A SITE AND ENSURE THAT CRAWLING IS ALLOWED BEFORE PASSING THAT SITE AS THE ROOT URL FOR THIS SCRIPT**

This is a quick script that takes a root url and a target url as input, then crawls the root url and logs all instances of links to the target url. This is extremely useful if you need to update or remove all instances of a link. The crawl does not follow external links and stays on the root domain, though the target link can be an external one. The crawl also excludes links which contain a query string (i.e. at least one instance of a question mark). I intend to create a second version of this script to identify any and all broken links, taking no target input. 

## Requirements

To run properly, this script requires Python 3 and the following modules:
- JupyterLab or Jupyter Notebook
- Requests
- bs4 (BeautifulSoup)
- the standard "time" and "sys" modules
