import json
import requests
import re

baseUrl = 'https://api.github.com/'
username, password = 'jaspu', 'na1244pata'
headers = {'Content-Type': 'application/json',
           'User-Agent': 'Python Student',
           'Accept': 'application/vnd.github.v3+json'}


def findLastPageNo(link):
    lastPageNo = link.split(',')[1]
    lastPageNo = re.findall(r'<(.*?)>', lastPageNo)[0]
    lastPageNo = lastPageNo.split('?')[1]
    if '&' in lastPageNo:
        lastPageNo = lastPageNo.split('=')[2]
    else:
        lastPageNo = lastPageNo.split('=')[1]
    return int(lastPageNo)


def findNextUrl(link):
    nextUrl = link.split(',')[0]
    nextUrl = re.findall(r'<(.*?)>', nextUrl)[0]
    return nextUrl


def getRepoCommitsInfo(ghFullRepoName):

    url = '{0}repos/{1}/commits?per_page=100'.format(baseUrl, ghFullRepoName)
    r = requests.get(url, auth=(username, password), headers=headers)
    repoCommitsData = json.loads(r.text)
    print(len(repoCommitsData))
    link = r.headers.get('link', None)
    nextUrl = findNextUrl(link)
    lastPageNo = findLastPageNo(link)

    for i in range(2, lastPageNo + 1):
        r = requests.get(nextUrl, auth=(username, password), headers=headers)
        repoCommitsData.extend(json.loads(r.text))
        print("Records Fetched: {}".format(len(repoCommitsData)))
        link = r.headers.get('link', None)
        nextUrl = findNextUrl(link)

    return repoCommitsData


def getUserInfo(ghUserLogin):
    url = '{0}users/{1}'.format(baseUrl, ghUserLogin)
    r = requests.get(url, auth=(username, password), headers=headers)
    if r.status_code == 200:
        print("Status code is 200 for user data")
        return json.loads(r.text)
    else:
        return None


def getRepoInfo(ghFullRepoName):
    url = '{0}repos/{1}'.format(baseUrl, ghFullRepoName)
    r = requests.get(url, auth=(username, password), headers=headers)
    if r.status_code == 200:
        print("Status code is 200 for repo data")
        return json.loads(r.text)
    else:
        return None
