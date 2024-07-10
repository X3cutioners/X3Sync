import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# File Host Info
host_domain = "krakenfiles.com"
host_api_domain = "krakenfiles.com"

# File Host Headers
ua = UserAgent()
headers = {
    'User-Agent': ua.chrome
}

def check_access(api_key):
    headers['X-AUTH-TOKEN'] = api_key
    params = {
        "page": "1",
        "perPage": "1"
    }
    response = requests.get(f'https://{host_api_domain}/api/file', headers=headers, params=params)
    if response.status_code == 200:
        return True
    else:
        return False

def get_upload_server(api_key):
    response = requests.get(f'https://{host_api_domain}/api/server/available', headers=headers).json()
    if response['status'] == 200:
        return response
    else:
        return False

def upload_file(api_key=None, file_path=None, file_url=None):
    if api_key:
        if check_access(api_key):
            upload_server_data = get_upload_server(api_key)
            if upload_server_data:
                if file_path:
                    files = {'file': open(file_path, 'rb')}
                    headers['X-AUTH-TOKEN'] = api_key
                    payload = { "serverAccessToken": upload_server_data['serverAccessToken'] }
                    response = requests.post(upload_server_data['url'], files=files, data=payload, headers=headers).json()
                    if response['status'] == 200:
                        return {"file_url": response['data']['url'], 'status': 200}
                    else:
                        return False

def extract_url(file_url):
    file_id = file_url.split("/")[-2]
    headers['x-requested-with'] = "XMLHttpRequest"
    response = requests.get(file_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    kraken_token = soup.find("input", {"id": "dl-token"})['value']
    payload = { "token": f"{kraken_token}" }
    response = requests.post(f'https://{host_api_domain}/download/{file_id}', data=payload, headers=headers)
    return response.json()