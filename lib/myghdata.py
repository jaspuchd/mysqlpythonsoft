import json
import requests
import re

baseUrl = 'https://api.github.com/'
username, password = 'jaspu', 'na1244pata'
headers = {'Content-Type': 'application/json',
           'User-Agent': 'Python Student',
           'Accept': 'application/vnd.github.v3+json'}


def getRepoLabelsInfo(ghFullRepoName):

    url = '{0}repos/{1}/labels'.format(baseUrl, ghFullRepoName)
    payload = {'per_page': 100}
    r = requests.get(url, auth=(username, password), headers=headers, params=payload)
    if r.status_code == 200:
        print("\nStatus code is 200 for Repo Labels data\n")
        repoLabelsData = json.loads(r.text)
        print("Number of Label Records Fetched: {}".format(len(repoLabelsData)))
        link = r.headers.get('link', None)

        if link is not None:
            lastPageNo = int(r.links['last']['url'].split('=')[-1])

            for i in range(2, lastPageNo + 1):
                nextUrl = r.links['next']['url']
                r = requests.get(nextUrl, auth=(username, password), headers=headers)
                repoLabelsData.extend(json.loads(r.text))
                print("Number of Label Records Fetched: {}".format(len(repoLabelsData)))

        return repoLabelsData
    else:
        return None


def getRepoCommitsInfo(ghFullRepoName):

    url = '{0}repos/{1}/commits'.format(baseUrl, ghFullRepoName)
    payload = {'per_page': 100}
    r = requests.get(url, auth=(username, password), headers=headers, params=payload)
    if r.status_code == 200:
        print("\nStatus code is 200 for Repo Commits data\n")
        repoCommitsData = json.loads(r.text)
        print("Number of Commit Records Fetched: {}".format(len(repoCommitsData)))
        link = r.headers.get('link', None)
        if link is not None:
            lastPageNo = int(r.links['last']['url'].split('=')[-1])

            for i in range(2, lastPageNo + 1):
                nextUrl = r.links['next']['url']
                r = requests.get(nextUrl, auth=(username, password), headers=headers)
                repoCommitsData.extend(json.loads(r.text))
                print("Number of Commit Records Fetched: {}".format(len(repoCommitsData)))

        return repoCommitsData
    else:
        return None


def getRepoIssuesInfo(ghFullRepoName):

    url = '{0}repos/{1}/issues'.format(baseUrl, ghFullRepoName)
    payload = {'state': 'all', 'per_page': 100}
    r = requests.get(url, auth=(username, password), headers=headers, params=payload)
    if r.status_code == 200:
        print("\nStatus code is 200 for Repo Issues data\n")
        repoIssuesData = json.loads(r.text)
        print("Number of Issue Records Fetched: {}".format(len(repoIssuesData)))
        link = r.headers.get('link', None)
        if link is not None:
            lastPageNo = int(r.links['last']['url'].split('=')[-1])

            for i in range(2, lastPageNo + 1):
                nextUrl = r.links['next']['url']
                r = requests.get(nextUrl, auth=(username, password), headers=headers)
                repoIssuesData.extend(json.loads(r.text))
                print("Number of Issue Records Fetched: {}".format(len(repoIssuesData)))

        return repoIssuesData
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


def getRepoContentsInfo(ghFullRepoName):
    url = '{0}repos/{1}/contents'.format(baseUrl, ghFullRepoName)
    r = requests.get(url, auth=(username, password), headers=headers)
    if r.status_code == 200:
        print("Status code is 200 for repo contents data")
        return json.loads(r.text)
    else:
        return None
