import json
import requests

baseUrl = 'https://api.github.com/'
username, password = 'jaspu', 'na1244pata'
headers = {'Content-Type': 'application/json',
           'User-Agent': 'Python Student',
           'Accept': 'application/vnd.github.v3+json'}


def getRepoCommitsInfo(ghFullRepoName):
    url = '{0}repos/{1}/commits'.format(baseUrl, ghFullRepoName)
    r = requests.get(url, auth=(username, password), headers=headers)
    if r.status_code == 200:
        print("Status code is 200 for repo commits data")
        return json.loads(r.text)
    else:
        return None


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
