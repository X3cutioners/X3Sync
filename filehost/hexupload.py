import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# File Host Info
host_domain = "hexload.com"
host_api_domain = "hexupload.net"

# File Host Headers
ua = UserAgent()
headers = {
    'User-Agent': ua.chrome
}

# Sample Key : 184577lf6oolhfhjviny

def check_access(api_key):
    response = requests.get(f'https://{host_api_domain}/api/account/info?key={api_key}', headers=headers).json()
    if response['status'] == 200:
        return True
    else:
        return False

def get_upload_server(api_key):
    response = requests.get(f'https://{host_api_domain}/api/upload/server?key={api_key}', headers=headers).json()
    if response['status'] == 200:
        return response
    else:
        return False

def upload_file(api_key=None, file_path=None, file_url=None):
    if api_key:
        if check_access(api_key):
            upload_server_data = get_upload_server(api_key)
            if file_path:
                files = {'file': f'{open(file_path, "rb")}'}
                payload = {'sess_id': upload_server_data['sess_id']}
                response = requests.post(upload_server_data['url'], data=payload, files=files).json()
                if response['file_status'] == 'OK':
                    return {"file_url": f'https://{host_domain}/{response['file_code']}', 'status': 200}
                else:
                    return False
            elif file_url:
                return {"error": "Remote Upload Not Supported by HexUpload/HexLoad", 'status': 503}
            else:
                return {"error": "No File Path or URL Provided"}
        else:
            return {"error": "Invalid API Key"}
    else:
        return {"error": "No API Key Provided"}
    
def extract_url(file_id):
    payload = {
    "op": "download3",
    "id": f"{file_id}",
    "ajax": "1",
    "method_free": "1"
    }
    headers['content-type'] = "application/x-www-form-urlencoded"
    headers['Accept'] = "application/json"
    response = requests.post(f'https://{host_domain}/download', data=payload, headers=headers, proxies={'https': '104.199.205.181:3128'})
    return response.json()