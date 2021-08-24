# input: zipcode
# zipcode -> google search(craigslist + zipcode) # search_distance = user_distance (default = 20)
# if craigslist.org in url, request.get(url)
# go to free page
# return results

# can increase range0

# # When searching for the correct craigslist, have options for the user to select
# # run server that is up 24/7 scanning for new free stuff for the zipcode

# use python for frontend + c++ backend for a basic app
from googlesearch import search
from requests import get 
from bs4 import BeautifulSoup


def craigslist(zipcode, query=None, distance=20):
    searches = search(f'Craigslist {zipcode}')
    for i in searches:
        if 'craigslist.org' in i:
            url = i
            break
    if not url:
        return "Sorry, there was an issue with retrieving the website!"
    
    # Need to find more proxy servers

    # http_proxy  = "http://10.10.1.10:3128"
    # https_proxy = "https://10.10.1.11:1080"
    # ftp_proxy   = "ftp://10.10.1.10:3128"
    # proxyDict = { 
    #             "http"  : http_proxy, 
    #             "https" : https_proxy, 
    #             "ftp"   : ftp_proxy
    #             }
    
    # The work-around is to tell the server not to bother with compression (https://stackoverflow.com/questions/27803503/get-html-using-python-requests):
    # headers = {'Accept-Encoding': 'identity'}

    
    if query:
        request = get(url+f'/d/free-stuff/search/zip?postal={zipcode}&search_distance={distance}')
    else:
        request = get(url+f'/search/zip?query={query}&search_distance={distance}&postal={zipcode}')
        
    soup = BeautifulSoup(request.text, 'lxml')
    posts = soup.find('ul', {'id': 'search-results'})
    posts = posts.find_all('li', {'class': 'result-row'})
    for post in posts:
        href = post.find('a')['href']
        image = post.find('a')
        info = post.find('div', {'class': 'result-info'})
        item = info.find('h3', {'class': 'result-heading'})
        date = info.find('time', {'class': 'result-date'})
        print(href, image, item.get_text(), date['datetime'])
        print('*'*40)
        yield [href, info, image, item.get_text(), date['datetime']]      
        
           
for post in craigslist(95608, query='couch'):
    print(post)
