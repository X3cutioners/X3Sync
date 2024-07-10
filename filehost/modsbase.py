import requests, cloudscraper
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Cloudflare Bypass
scraper = cloudscraper.create_scraper()

# File Host Info
host_domain = "modsbase.com"
host_api_domain = "modsbase.com"

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
    "referer": "",
    "method_free": "",
    "method_premium": ""
    }
    response = scraper.post(f'https://{host_domain}', data=payload)
    soup = BeautifulSoup(response.text, 'html.parser')
    download_btn = soup.find('button', {'id': 'downloadbtn'})
    download_url = download_btn.find('a')['href']
    return {"file_url": download_url, 'status': 200}