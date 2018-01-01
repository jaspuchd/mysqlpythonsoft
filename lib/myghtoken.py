import requests
import json
from urllib.parse import urljoin

GITHUB_API = 'https://api.github.com'


def main():
    # username = input('Github Username: ')
    # password = input('Github Password: ')

    url = urljoin(GITHUB_API, 'authorizations')
    # payload = {"client_secret": "a46f6528b06d4d26701491ac95ca1c86a4164bfd",
    # "scopes": ["public_repo"], "note": "admin script", }

    r = requests.get(url, auth=('jaspu', 'na1244pata'))
    print(r.text)
    j = json.loads(r.text)

    if r.status_code >= 400:
        msg = j.get('message', 'UNDEFINED ERROR (no error description from server)')
        print(msg)
        return
    token = j['token']
    print('New token: {}'.format(token))


if __name__ == '__main__':
    main()
