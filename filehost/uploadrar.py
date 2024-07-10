import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# File Host Info
host_domain = "uploadrar.com"
host_api_domain = "uploadrar.com"

# File Host Headers
ua = UserAgent()
headers = {
    'User-Agent': ua.chrome
}

def check_access(api_key):
    response = requests.get(f'https://{host_api_domain}/api/account/info?key={api_key}', headers=headers).json()
    if response['status'] == 200:
        return True
    else:
        return False

def extract_url(file_id):
    payload = {
    "op": "download2",
    "id": file_id,
    "rand": "",
    "referer": "https://get.rahim-soft.com/sq3eiszm8g88",
    "method_free": "",
    "method_premium": "1",
    "adblock_detected": "0"
    }
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}

    response = requests.post("https://get.rahim-soft.com/art.html", data=payload, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    download_url = soup.find_all("a", {"id": "netTab"})[0]
    download_url = download_url['href']
    return download_url
