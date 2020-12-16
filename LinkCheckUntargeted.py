import requests, time, sys
from bs4 import BeautifulSoup

# Function to attempt to retrieve, will return a response code or retry on errors as many times as "attempts" before returning "FAILED"
def get_attempt(base_url, get_params=None, attempts=10):
    for attempt in range(attempts):
        time.sleep(0.5)
        try:
            response = requests.get(base_url, params=get_params, allow_redirects=True)
            break
        except:
            if attempt == attempts - 1:
                response = "FAILED"
            continue
    return response

# Recursive function to crawl unseen links
def check_page(href, done_hrefs, true_domain, check_depth, f):
    check_depth += 1
    #print(check_depth)
    # Make fully qualified if not
    if href[:4] != "http":
        href = true_domain + href

    # Check if link is known broken
    if href in failed_hrefs.keys():
        check_depth -= 1
        return failed_hrefs['href']
    
    # Check if link is duplicate
    if href in done_hrefs:
        check_depth -= 1
        return

    # Check if link is internal
    internal = href[:len(true_domain)] == true_domain
    
    # # Print statement every ten pages processed
    # if len(done_hrefs) % 10 == 0:
    #     pass #print(f"Pages processed: {len(done_hrefs)}")

    # Add current page to done list and attempt to access

    # print(f"CHECKING {href}", file=f)

    done_hrefs.append(href)
    req = get_attempt(href, attempts=3)

    # Return if request failed
    if (req == "FAILED") or (req.status_code != 200):
        failed_hrefs['href'] = req
        check_depth -= 1
        return req

    # Only continue crawling if link was internal    
    if internal:
        html = req.content
        soup = BeautifulSoup(html, 'html.parser')
        anchors = soup.find_all("a")
        for item in anchors:
            if 'href' in item.attrs.keys():
                # Ignore any urls which include a query
                if item['href'].find('?') == -1 and item['href'].find('@') == -1:
                    if (ret_val := check_page(item['href'], done_hrefs, true_domain, check_depth, f)) is not None:
                        print(f"Link {item['href']} failed, response {ret_val}", file=f)
                        print(f"    on page {href}", file=f)
                        print(f"    in element {item.parent} \n", file=f)
    check_depth -= 1
    return

# Initial inputs - root supplied by user
root_url = input("Please enter a root url: ")

# Get actual root of domain
true_domain = "/".join(root_url.split("/")[:3])

# Set root_url to end with slash and add version without slash to done hrefs
if root_url[-1] != "/":
    root_url = root_url + "/"
done_hrefs = [root_url[:-1]]
failed_hrefs = dict()
check_depth = 0
f = open("/Users/benjaminpeck/Desktop/Stuff/LinkCheck/link_check_output.txt", 'w', buffering=1)
print("Link Check Output:", file=f)

# Attempt to access user-supplied root url, exit if not usable
check_page(root_url, done_hrefs, true_domain, check_depth, f)

f.close()