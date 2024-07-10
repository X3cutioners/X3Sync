import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# File Host Info
host_domain = "dosya.co"
host_api_domain = "dosya.co"

# File Host Headers
ua = UserAgent()
headers = {
    'User-Agent': ua.chrome
}

def extract_url(file_id):
    response = requests.get(f'https://{host_domain}/{file_id}', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    rand_token = soup.find('input', {'name': 'rand'})['value']
    payload = {
        "op": "download2",
        "id": f"{file_id}",
        "rand": f"{rand_token}",
        "referer": "",
        "method_free": "",
        "method_premium": ""
    }
    response = requests.post(f'https://{host_domain}/{file_id}', data=payload, allow_redirects=False, headers=headers)
    download_url = response.headers['Location']
    return {"file_url": download_url, 'status': 200}