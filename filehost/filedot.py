import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# File Host Info
host_domain = "filedot.to"
host_api_domain = "filedot.to"

# File Host Headers
ua = UserAgent()
headers = {
    'User-Agent': ua.chrome
}

def extract_url(file_id):
    payload = {
    "op": "download2",
    "id": f"{file_id}",
    "rand": "",
    "referer": f"https://filedot.to/{file_id}",
    "method_free": "Free+Download",
    "method_premium": "",
    "adblock_detected": "0"
    }
    response = requests.post(f'https://{host_domain}/{file_id}', headers=headers, data=payload, cookies={'xfss':'updpq7shwoc3s2ps'})
    soup = BeautifulSoup(response.text, 'html.parser')
    download_btn = soup.find('td', {'class': 'bigres'}).find('a')
    download_url = download_btn['href']
    return {"file_url": download_url, 'status': 200}






