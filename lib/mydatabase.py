import mysql.connector
from mysql.connector import errorcode
from lib import myghdata
import sys
# insertRepo method inserts repo data from myfetchdata module into MySql database


def insertRepo(dbConfig, repoData):

    userData = myghdata.getUserInfo(repoData['owner']['login'])

    if userData is not None:
        print("\nWe got User data from GitHub\n")
        insertUser(dbConfig, userData)
    else:
        print("\nGitHub User Info API call returned None\n")
        sys.exit(1)

    try:
        cnx = mysql.connector.connect(**dbConfig)  # Connection creation
        print("\nConnection with Database Successful for Repo Table\n")
        myCursor = cnx.cursor()  # Cursor Creation
        # keys for fetchting only required keys

        repoData['user_id'] = repoData['owner']['id']

        if repoData['license'] != None:
            repoData['license'] = repoData['license']['key']

        ghAttribs = ['id', 'name', 'full_name', 'user_id', 'fork', 'created_at', 'updated_at', 'pushed_at', 'homepage', 'size', 'stargazers_count',
                     'subscribers_count', 'forks', 'language', 'has_issues', 'has_pages', 'has_wiki', 'archived', 'open_issues', 'license', 'network_count']

        reqRepoData = {}

        for k in repoData:
            if k in ghAttribs:
                reqRepoData[k] = repoData[k]

        for k in reqRepoData:
            if reqRepoData[k] == '':
                reqRepoData[k] = None

        # for k,v in reqRepoData.items():
        #     print('{}:{}'.format(k,v))

        insertRepoQuery = """INSERT INTO repo (id, name, full_name, user_id, is_fork, created_at,updated_at,
        pushed_at, homepage, size, stargazers_count, watchers_count, forks, primary_language, has_issues,
        has_pages, has_wiki, is_archived, open_issues, license, network_count)
        VALUES
        (%(id)s,%(name)s,%(full_name)s,%(user_id)s,%(fork)s,STR_TO_DATE(%(created_at)s, "%Y-%m-%dT%TZ"),
        STR_TO_DATE(%(updated_at)s, "%Y-%m-%dT%TZ"),STR_TO_DATE(%(pushed_at)s, "%Y-%m-%dT%TZ"),
        %(homepage)s,%(size)s,%(stargazers_count)s,%(subscribers_count)s,%(forks)s,%(language)s,%(has_issues)s,
        %(has_pages)s,%(has_wiki)s,%(archived)s,%(open_issues)s, %(license)s, %(network_count)s)"""

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

    repoCommitsData = myghdata.getRepoCommitsInfo(repoData['full_name'])

    if repoCommitsData is not None:
        print("\nWe got Repository Commits data from GitHub\n")
        insertRepoCommits(dbConfig, repoCommitsData, repoData['id'])
    else:
        print("\nGitHub Repo Commits Info API call returned None\n")
        sys.exit(1)

    repoContentsData = myghdata.getRepoContentsInfo(repoData['full_name'])

    if repoContentsData is not None:
        print("\nWe got Repository Contents data from GitHub\n")
        insertRepoContents(dbConfig, repoContentsData, repoData['id'])
    else:
        print("\nGitHub Repo Contents Info API call returned None\n")
        sys.exit(1)


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
                    reqRepoContentsData[k] = None

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
            forEachCommitRecord['author_date'] = repoCommitsData[k]['commit']['author']['date']
            forEachCommitRecord['committer_name'] = repoCommitsData[k]['commit']['committer']['name']
            forEachCommitRecord['committer_email'] = repoCommitsData[k]['commit']['committer']['email']
            forEachCommitRecord['committer_date'] = repoCommitsData[k]['commit']['committer']['date']
            reqRepoCommitsData.append(forEachCommitRecord)

        for k in range(0, len(reqRepoCommitsData)):
            for l in reqRepoCommitsData[k]:
                if reqRepoCommitsData[k][l] == '':
                    reqRepoCommitsData[k] = None

        insertRepoCommitsQuery = """INSERT INTO commit (sha, repo_id, comment_count, author_name, author_email, author_date, committer_name,committer_email,committer_date)
             VALUES
             (%(sha)s, %(repo_id)s, %(comment_count)s, %(author_name)s,%(author_email)s,
             STR_TO_DATE(%(author_date)s, "%Y-%m-%dT%TZ"), %(committer_name)s, %(committer_email)s,
             STR_TO_DATE(%(committer_date)s, "%Y-%m-%dT%TZ"))"""

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

        ghAttribs = ['id', 'login', 'name', 'company', 'blog', 'location', 'email', 'hireable',
                     'public_repos', 'public_gists', 'followers', 'following', 'created_at', 'updated_at']

        reqUserData = {}

        for k in userData:
            if k in ghAttribs:
                reqUserData[k] = userData[k]

        for k in reqUserData:
            if reqUserData[k] == '':
                reqUserData[k] = None

        # for k,v in reqUserData.items():
        #     print('{}:{}'.format(k,v))

        insertUserQuery = """INSERT INTO user (id, login, name, company, blog, location, email, hireable,
            public_repos, public_gists, followers, following, created_at, updated_at)
            VALUES
            (%(id)s, %(login)s, %(name)s, %(company)s, %(blog)s, %(location)s, %(email)s, %(hireable)s,
             %(public_repos)s, %(public_gists)s, %(followers)s, %(following)s,
             STR_TO_DATE(%(created_at)s, "%Y-%m-%dT%TZ"),STR_TO_DATE(%(updated_at)s, "%Y-%m-%dT%TZ"))"""

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
