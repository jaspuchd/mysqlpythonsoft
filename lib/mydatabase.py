import mysql.connector
from mysql.connector import errorcode
from lib import myghdata
import sys
import datetime
# insertRepo method inserts repo data from myfetchdata module into MySql database


def insertRepo(dbConfig, repoData):

    # userData = myghdata.getUserInfo(repoData['owner']['login'])

    # if userData is not None:
    #     print("\nWe got User data from GitHub\n")
    #     insertUser(dbConfig, userData)
    # else:
    #     print("\nGitHub User Info API call returned None\n")
    #     sys.exit(1)

    try:
        cnx = mysql.connector.connect(**dbConfig)  # Connection creation
        print("\nConnection with Database Successful for Repo Table\n")
        myCursor = cnx.cursor()  # Cursor Creation
        # keys for fetchting only required keys

        reqRepoData = {}
        reqRepoData['id'] = repoData['id']
        reqRepoData['name'] = repoData['name']
        reqRepoData['full_name'] = repoData['full_name']
        reqRepoData['user_id'] = repoData['owner']['id']
        reqRepoData['is_fork'] = repoData['fork']
        reqRepoData['created_at'] = datetime.datetime.strptime(repoData['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        reqRepoData['updated_at'] = datetime.datetime.strptime(repoData['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
        reqRepoData['pushed_at'] = datetime.datetime.strptime(repoData['pushed_at'], "%Y-%m-%dT%H:%M:%SZ")
        reqRepoData['homepage'] = repoData['homepage']
        reqRepoData['size'] = repoData['size']
        reqRepoData['stargazers_count'] = repoData['stargazers_count']
        reqRepoData['watchers_count'] = repoData['subscribers_count']
        reqRepoData['forks'] = repoData['forks']
        reqRepoData['primary_language'] = repoData['language']
        reqRepoData['has_issues'] = repoData['has_issues']
        reqRepoData['has_pages'] = repoData['has_pages']
        reqRepoData['has_wiki'] = repoData['has_wiki']
        reqRepoData['is_archived'] = repoData['archived']
        reqRepoData['open_issues'] = repoData['open_issues']
        reqRepoData['license'] = repoData['license']['key'] if repoData['license'] else None
        reqRepoData['network_count'] = repoData['network_count']
        reqRepoData['parent_repo_id'] = repoData['parent']['id'] if 'parent' in repoData else None
        reqRepoData['parent_repo_full_name'] = repoData['parent']['full_name'] if 'parent' in repoData else None
        reqRepoData['parent_repo_owner_id'] = repoData['parent']['owner']['id'] if 'parent' in repoData else None
        reqRepoData['source_repo_id'] = repoData['source']['id'] if 'source' in repoData else None
        reqRepoData['source_repo_full_name'] = repoData['source']['full_name'] if 'source' in repoData else None
        reqRepoData['source_repo_owner_id'] = repoData['source']['owner']['id'] if 'source' in repoData else None

        for k in reqRepoData:
            if reqRepoData[k] == '':
                reqRepoData[k] = None

        insertRepoQuery = """INSERT INTO repo (id, name, full_name, user_id, is_fork, created_at,updated_at,
        pushed_at, homepage, size, stargazers_count, watchers_count, forks, primary_language, has_issues,
        has_pages, has_wiki, is_archived, open_issues, license, network_count, parent_repo_id, parent_repo_full_name,
        parent_repo_owner_id, source_repo_id, source_repo_full_name, source_repo_owner_id)
        VALUES
        (%(id)s,%(name)s,%(full_name)s,%(user_id)s,%(is_fork)s,%(created_at)s, %(updated_at)s,%(pushed_at)s,
        %(homepage)s,%(size)s,%(stargazers_count)s,%(watchers_count)s,%(forks)s,%(primary_language)s,%(has_issues)s,
        %(has_pages)s,%(has_wiki)s,%(is_archived)s,%(open_issues)s, %(license)s, %(network_count)s, %(parent_repo_id)s,
        %(parent_repo_full_name)s, %(parent_repo_owner_id)s, %(source_repo_id)s, %(source_repo_full_name)s,
        %(source_repo_owner_id)s)"""

        myCursor.execute(insertRepoQuery, reqRepoData)
        cnx.commit()
        myCursor.close()

        print("\nData Inserted Successfully in Repo Table\n")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Wrong Username of Password for Database Connection")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database {0} doesnt Exist".format(dbConfig['database']))
        else:
            print(err)
    else:
        cnx.close()

    # repoCommitsData = myghdata.getRepoCommitsInfo(repoData['full_name'])

    # if repoCommitsData is not None:
    #     print("\nWe got Repository Commits data from GitHub\n")
    #     insertRepoCommits(dbConfig, repoCommitsData, repoData['id'])
    # else:
    #     print("\nGitHub Repo Commits Info API call returned None\n")
    #     sys.exit(1)

    # repoContentsData = myghdata.getRepoContentsInfo(repoData['full_name'])

    # if repoContentsData is not None:
    #     print("\nWe got Repository Contents data from GitHub\n")
    #     insertRepoContents(dbConfig, repoContentsData, repoData['id'])
    # else:
    #     print("\nGitHub Repo Contents Info API call returned None\n")
    #     sys.exit(1)

    # repoIssuesData = myghdata.getRepoIssuesInfo(repoData['full_name'])

    # if repoIssuesData is not None:
    #     print("\nWe got Repository Issues data from GitHub\n")
    #     insertRepoIssues(dbConfig, repoIssuesData, repoData['id'])
    # else:
    #     print("\nGitHub Repo Issues Info API call returned None\n")
    #     sys.exit(1)

    repoLabelsData = myghdata.getRepoLabelsInfo(repoData['full_name'])

    if repoLabelsData is not None:
        print("\nWe got Repository Labels data from GitHub\n")
        insertRepoLabels(dbConfig, repoLabelsData, repoData['id'])
    else:
        print("\nGitHub Repo Labels Info API call returned None\n")
        sys.exit(1)


def insertRepoLabels(dbConfig, repoLabelsData, repoId):
    pass


def insertRepoIssues(dbConfig, repoIssuesData, repoId):
    try:
        cnx = mysql.connector.connect(**dbConfig)  # Connection creation
        print("\nConnection with Database Successful for Repo Issues Table")
        myCursor = cnx.cursor()  # Cursor Creation

        reqRepoIssuesData = []

        for k in range(0, len(repoIssuesData)):
            dictForEachIssueRecord = {}
            dictForEachIssueRecord['id'] = repoIssuesData[k]['id']
            dictForEachIssueRecord['number'] = repoIssuesData[k]['number']
            dictForEachIssueRecord['repo_id'] = repoId
            dictForEachIssueRecord['title'] = repoIssuesData[k]['title']
            dictForEachIssueRecord['created_by'] = repoIssuesData[k]['user']['id']
            dictForEachIssueRecord['state'] = repoIssuesData[k]['state']
            dictForEachIssueRecord['is_locked'] = repoIssuesData[k]['locked']
            dictForEachIssueRecord['milestone_id'] = repoIssuesData[k]['milestone']['id'] if repoIssuesData[k]['milestone'] else None
            dictForEachIssueRecord['is_pull_request'] = True if 'pull_request' in repoIssuesData[k] else False
            dictForEachIssueRecord['comments_count'] = repoIssuesData[k]['comments']
            dictForEachIssueRecord['created_at'] = datetime.datetime.strptime(repoIssuesData[k]['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            dictForEachIssueRecord['updated_at'] = datetime.datetime.strptime(repoIssuesData[k]['updated_at'], "%Y-%m-%dT%H:%M:%SZ")

            if repoIssuesData[k]['closed_at']:
                dictForEachIssueRecord['closed_at'] = datetime.datetime.strptime(repoIssuesData[k]['closed_at'], "%Y-%m-%dT%H:%M:%SZ")
            else:
                dictForEachIssueRecord['closed_at'] = None

            reqRepoIssuesData.append(dictForEachIssueRecord)

        for k in range(0, len(reqRepoIssuesData)):
            for l in reqRepoIssuesData[k]:
                if reqRepoIssuesData[k][l] == '':
                    reqRepoIssuesData[k][l] = None

        insertRepoIssuesQuery = """INSERT INTO issue (id, number, repo_id, title, created_by, state, is_locked, milestone_id, is_pull_request, comments_count, created_at, updated_at, closed_at)
             VALUES
             (%(id)s, %(number)s, %(repo_id)s, %(title)s, %(created_by)s, %(state)s, %(is_locked)s, %(milestone_id)s,
             %(is_pull_request)s, %(comments_count)s, %(created_at)s, %(updated_at)s, %(closed_at)s)"""

        myCursor.executemany(insertRepoIssuesQuery, reqRepoIssuesData)
        cnx.commit()
        myCursor.close()

        print("\nData Inserted Successfully in Repo Issues Table\n")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Wrong Username of Password for Database Connection")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database {0} doesnt Exist".format(dbConfig['database']))
        else:
            print(err)
            sys.exit(1)  # If data doesnt got inserted in issue table, system should
            # stop here, without automatically inserting data in further tables.
    else:
        cnx.close()


def insertRepoContents(dbConfig, repoContentsData, repoId):
    try:
        cnx = mysql.connector.connect(**dbConfig)  # Connection creation
        print("\nConnection with Database Successful for Repo Contents Table\n")
        myCursor = cnx.cursor()  # Cursor Creation
        # keys for fetchting only required keys

        reqRepoContentsData = []

        for k in range(0, len(repoContentsData)):
            forEachContentRecord = {}
            forEachContentRecord['sha'] = repoContentsData[k]['sha']
            forEachContentRecord['repo_id'] = repoId
            forEachContentRecord['name'] = repoContentsData[k]['name']
            forEachContentRecord['path'] = repoContentsData[k]['path']
            forEachContentRecord['size'] = repoContentsData[k]['size']
            forEachContentRecord['type'] = repoContentsData[k]['type']
            reqRepoContentsData.append(forEachContentRecord)

        for k in range(0, len(reqRepoContentsData)):
            for l in reqRepoContentsData[k]:
                if reqRepoContentsData[k][l] == '':
                    reqRepoContentsData[k][l] = None

        insertRepoContentsQuery = """INSERT INTO contents (sha, repo_id, name, path, size, type)
             VALUES
             (%(sha)s, %(repo_id)s, %(name)s, %(path)s,%(size)s, %(type)s)"""

        myCursor.executemany(insertRepoContentsQuery, reqRepoContentsData)
        cnx.commit()
        myCursor.close()

        print("\nData Inserted Successfully in Repo Contents Table\n")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Wrong Username of Password for Database Connection")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database {0} doesnt Exist".format(dbConfig['database']))
        else:
            print(err)
    else:
        cnx.close()


def insertRepoCommits(dbConfig, repoCommitsData, repoId):
    try:
        cnx = mysql.connector.connect(**dbConfig)  # Connection creation
        print("\nConnection with Database Successful for Repo Commits Table\n")
        myCursor = cnx.cursor()  # Cursor Creation

        reqRepoCommitsData = []

        for k in range(0, len(repoCommitsData)):
            forEachCommitRecord = {}
            forEachCommitRecord['sha'] = repoCommitsData[k]['sha']
            forEachCommitRecord['repo_id'] = repoId
            forEachCommitRecord['comment_count'] = repoCommitsData[k]['commit']['comment_count']
            forEachCommitRecord['author_name'] = repoCommitsData[k]['commit']['author']['name']
            forEachCommitRecord['author_email'] = repoCommitsData[k]['commit']['author']['email']
            forEachCommitRecord['author_date'] = datetime.datetime.strptime(repoCommitsData[k]['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")
            forEachCommitRecord['committer_name'] = repoCommitsData[k]['commit']['committer']['name']
            forEachCommitRecord['committer_email'] = repoCommitsData[k]['commit']['committer']['email']
            forEachCommitRecord['committer_date'] = datetime.datetime.strptime(repoCommitsData[k]['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")
            reqRepoCommitsData.append(forEachCommitRecord)

        for k in range(0, len(reqRepoCommitsData)):
            for l in reqRepoCommitsData[k]:
                if reqRepoCommitsData[k][l] == '':
                    reqRepoCommitsData[k][l] = None

        insertRepoCommitsQuery = """INSERT INTO commit (sha, repo_id, comment_count, author_name, author_email, author_date, committer_name,committer_email,committer_date)
             VALUES
             (%(sha)s, %(repo_id)s, %(comment_count)s, %(author_name)s,%(author_email)s, %(author_date)s, %(committer_name)s,
             %(committer_email)s, %(committer_date)s)"""

        myCursor.executemany(insertRepoCommitsQuery, reqRepoCommitsData)
        cnx.commit()
        myCursor.close()

        print("\nData Inserted Successfully in Repo Commits Table\n")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Wrong Username of Password for Database Connection")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database {0} doesnt Exist".format(dbConfig['database']))
        else:
            print(err)
            sys.exit(1)  # If data doesnt got inserted in user table, system should
            # stop here, without automatically inserting data in repo table.
    else:
        cnx.close()


def insertUser(dbConfig, userData):
    try:
        cnx = mysql.connector.connect(**dbConfig)  # Connection creation
        print("\nConnection with Database Successful for User Table\n")
        myCursor = cnx.cursor()  # Cursor Creation
        # keys for fetchting only required keys

        reqUserData = {}
        reqUserData['id'] = userData['id']
        reqUserData['login'] = userData['login']
        reqUserData['name'] = userData['name']
        reqUserData['company'] = userData['company']
        reqUserData['blog'] = userData['blog']
        reqUserData['location'] = userData['location']
        reqUserData['email'] = userData['email']
        reqUserData['hireable'] = userData['hireable']
        reqUserData['public_repos'] = userData['public_repos']
        reqUserData['public_gists'] = userData['public_gists']
        reqUserData['followers'] = userData['followers']
        reqUserData['following'] = userData['following']
        reqUserData['created_at'] = datetime.datetime.strptime(userData['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        reqUserData['updated_at'] = datetime.datetime.strptime(userData['updated_at'], "%Y-%m-%dT%H:%M:%SZ")

        for k in reqUserData:
            if reqUserData[k] == '':
                reqUserData[k] = None

        insertUserQuery = """INSERT INTO user (id, login, name, company, blog, location, email, hireable,
            public_repos, public_gists, followers, following, created_at, updated_at)
            VALUES
            (%(id)s, %(login)s, %(name)s, %(company)s, %(blog)s, %(location)s, %(email)s, %(hireable)s,
             %(public_repos)s, %(public_gists)s, %(followers)s, %(following)s, %(created_at)s, %(updated_at)s)"""

        myCursor.execute(insertUserQuery, reqUserData)
        cnx.commit()
        myCursor.close()

        print("\nData Inserted Successfully in User Table\n")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Wrong Username of Password for Database Connection")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database {0} doesnt Exist".format(dbConfig['database']))
        else:
            print(err)
            sys.exit(1)  # If data doesnt got inserted in user table, system shoudl
            # stop here, without automatically inserting data in repo table.
    else:
        cnx.close()
