import requests, time, sys
from bs4 import BeautifulSoup
pages_processed = 0

class LinkClass:
    def __init__(self, response=None, parents=dict()):
        self.response = response
        self.parents = parents

# Function to attempt to retrieve, will return a response code or retry on errors as many times as "attempts" before returning "FAILED"
def get_attempt(base_url, get_params=None, attempts=10):
    for attempt in range(attempts):
        time.sleep(0.5)
        try:
            response = requests.get(base_url, params=get_params, allow_redirects=True, stream=True, timeout=6)
            break
        except:
            if attempt == attempts - 1:
                response = "FAILED"
            continue
    return response

# Recursive function to crawl unseen links
def check_page(href, links, true_domain):
    global pages_processed

    # Make fully qualified if not
    if href[:4] != "http":
        href = true_domain + href

    # Check response of link and instantiate if not in list
    if href in links.keys():
        if links[href].response is not None:
            return links[href].response
    else:
        links[href] = LinkClass()

    # Check if link is internal
    internal = href[:len(true_domain)] == true_domain
    
    # # Verbose output for debugging only
    # print(f"CHECKING {href}")

    # Attempt to access
    req = get_attempt(href, attempts=3)
    pages_processed += 1

    # Print statement every ten pages processed
    if pages_processed % 10 == 0:
        print(f"Pages processed: {pages_processed}")


    if req != "FAILED":
        req_status = req.status_code
    else:
        req_status = "FAILED"

    links[href].response = req_status

    # Return if request failed
    if req_status != 200:
        if req != "FAILED":
            req.close()
        return req_status

    # Only continue crawling if link was internal    
    if internal:
        html = req.content
        soup = BeautifulSoup(html, 'html.parser')
        anchors = soup.find_all("a")
        for item in anchors:
            if 'href' in item.attrs.keys():
                # Ignore any urls which include a query or fragment identifier
                if item['href'].find('?') == -1 and item['href'].find('@') == -1 and item['href'].find('#') == -1 and item['href'].find('javascript:') == -1:
                    # Check for new internal links and log for later checks
                    if item['href'][:len(true_domain)] == true_domain:
                        if item['href'] not in links.keys():
                            links[(item['href'])] = LinkClass(None, {href: item.parent})
                        else:
                            #links[(item['href'])].parents.update({href: item.parent})
                            apple = item['href']
                            orange = links[apple]
                            banana = orange.parents
                            pineapple = item.parent
                            banana.update({href: pineapple})
                        continue
                    if item['href'][:4] != "http":
                        if (true_domain + item['href']) not in links.keys():
                            links[true_domain + item['href']] = LinkClass(None, {href: item.parent})
                        else:
                            links[true_domain + item['href']].parents.update({href: item.parent})
                        continue
                    if (ret_val := check_page(item['href'], links, true_domain)) != 200:
                        links[(item['href'])].parents.update({href: item.parent})
    req.close()
    return 200

# Initial inputs - root supplied by user
root_url = input("Please enter a root url: ")

# Get actual root of domain
true_domain = "/".join(root_url.split("/")[:3])

# Set root_url to end with slash and add version without slash to done hrefs
if root_url[-1] != "/":
    root_url = root_url + "/"
links = dict()
links[root_url[:-1]] = LinkClass()



# Attempt to access user-supplied root url, exit if not usable
i = 0
while i < len(links):
    check_page(list(links)[i], links, true_domain)
    i += 1
f = open("/Users/benjaminpeck/Desktop/Stuff/LinkCheck/link_check_output.txt", 'w', buffering=1)
print("Link Check Output: \n", file=f)
for link in list(links):
    if links[link].response != 200:
        print(f"Link {link} failed, response {links[link].response}", file=f)
        for parent in links[link].parents.keys():
            print(f"    on page {parent}", file=f)
            print(f"    in element {links[link].parents[parent]}", file=f)
        print("\n", file=f)
f.close()