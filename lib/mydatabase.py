import mysql.connector
from mysql.connector import errorcode
from lib import myghdata
import sys
# insertRepo method inserts repo data from myfetchdata module into MySql database


def insertRepo(dbConfig, repoData):

    userData = myghdata.getUserInfo(repoData['owner']['login'])
    insertUser(dbConfig, userData)

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
    insertRepoCommits(dbConfig, repoCommitsData, repoData['id'])


def insertRepoCommits(dbConfig, repoCommitsData, repoId):
    print("\ndata reached in insert\n")
    print("Repo id is {}\n".format(repoId))

    try:
        cnx = mysql.connector.connect(**dbConfig)  # Connection creation
        print("\nConnection with Database Successful for Repo Commits Table\n")
        myCursor = cnx.cursor()  # Cursor Creation

        repoCommitsData[0]['repo_id'] = repoId
        repoCommitsData[0]['comment_count'] = repoCommitsData[0]['commit']['comment_count']
        repoCommitsData[0]['author_id'] = repoCommitsData[0]['author']['id']
        repoCommitsData[0]['committer_id'] = repoCommitsData[0]['committer']['id']
        repoCommitsData[0]['message'] = repoCommitsData[0]['commit']['message']

        ghAttribs = ['sha', 'repo_id', 'comment_count', 'author_id', 'committer_id', 'message']

        reqRepoCommitsData = {}

        for k in repoCommitsData[0]:
            if k in ghAttribs:
                reqRepoCommitsData[k] = repoCommitsData[0][k]

        for k in reqRepoCommitsData:
            if reqRepoCommitsData[k] == '':
                reqRepoCommitsData[k] = None

        for k, v in reqRepoCommitsData.items():
            print('{}:{}'.format(k, v))

        insertRepoCommitsQuery = """INSERT INTO commit (sha, repo_id, comment_count, author_id, committer_id, message)
             VALUES
             (%(sha)s, %(repo_id)s, %(comment_count)s, %(author_id)s, %(committer_id)s, %(message)s)"""

        myCursor.execute(insertRepoCommitsQuery, reqRepoCommitsData)
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
