from django.conf import settings
import requests


project_base = '/home/rgocio'
project_name = 'ighor'
settings = 'ighor.settings.py'
project_repo = 'https://github.com/rubengocio/ighor.git'

domain = 'rgocio.pythonanywhere.com'
username = 'rgocio'
token = '09d89a5b0a0889e26d1c755b3dac45bb64f3609b'

print('Updating changes from repo')

response = requests.post(
    'https://www.pythonanywhere.com/api/v0/user/{username}/consoles/custom_scripts/9361/execute'.format(username=username),
    headers={'Authorization': 'Token {token}'.format(token=token)}
)
print(response)

# reload server
print('reload website...')
response = requests.post(
    'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain}/reload/'.format(
        username=username, domain=domain
    ),
    headers={'Authorization': 'Token {token}'.format(token=token)}
)
if response.status_code == 200:
    print('Finished OK')
else:
    print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))
