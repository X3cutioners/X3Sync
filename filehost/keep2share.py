import requests
from fake_useragent import UserAgent

ua = UserAgent()
headers = {
    'User-Agent': ua.chrome,
    'Content-Type':"application/json"
}

host_api_domain = "keep2share.cc"

def get_upload_form_data(auth_token):
    data = {'auth_token':  auth_token}
    response = requests.post(f'https://{host_api_domain}/api/v2/getUploadFormData',headers=headers,json=data).json()
    if response['code'] == 200:
        return response
    else:
        return False

def upload_file(username=None,password=None,file_path=None):
   
    if username and password:
        if file_path:
            auth_token = get_auth_token(username=username,password=password)
            if auth_token:
                if get_upload_form_data(auth_token=auth_token):
                    form_data = get_upload_form_data(auth_token=auth_token)
                    file_field = form_data["file_field"]
                    ajax = form_data["form_data"]["ajax"]
                    params = form_data["form_data"]["params"]
                    sig = form_data["form_data"]["signature"]

                    files = {
                        file_field:open(file_path,'rb'),
                        "ajax": (None, ajax),
                        "signature": (None, sig),
                        "params": (None, params)
                    }
                    response = requests.post(form_data['form_action'],files=files).json()
                    if response['status_code'] == 200:
                        return {"file_url": response['link'], 'status': 200}
                    else:
                        return False
                else:
                    return {"error":"Couldn't get upload form data"}
            else:
                return {"error":"Couldn't get AuthToken, check credentials"}
        else:
            return {"error":"No file Path provided"}
    else:
        return {"error":"No credentials provided"} 
            
def get_auth_token(username,password):
    data = {"username": username, "password": password}
    response = requests.post(f'https://{host_api_domain}/api/v2/login',headers=headers,json=data).json()
    print(response)
    if response['code'] == 200:
        return response['auth_token']
    else:
        return False
            
def check_url(file_url):
    file_id = file_url.split("/")[4]
    data = {"id":file_id}
    response = requests.post(f'https://{host_api_domain}/api/v2/getFileStatus',headers=headers,json=data).json()
    if response['code'] == 200:
        return response['is_available']
    else:
        return False
    
def extract_url(file_url,username,password):
    if username and password:
        if file_url:
            if check_url(file_url):
                auth_token = get_auth_token(username=username,password=password)
                if auth_token:
                    file_id = file_url.split("/")[4]
                    data = {"auth_token":auth_token,"file_id":file_id}
                    response = requests.post(f'https://{host_api_domain}/api/v2/getUrl',headers=headers,json=data).json()
                    if response['code'] == 200:
                        return {"file_url":response['url'], 'status':200}
                    else:
                        return False
                else:
                    return {"error":"Couldn't get AuthToken, check credentials"}
            else:
                return {"error": "Invalid URL"}
        else:
            return {"error": "No URL provided"}
    else:
        return {"error": "No credentials provided"}
            
def upload_remote(file_url,username,password):
    if file_url:
        auth_token = get_auth_token(username=username,password=password)
        if auth_token:
            data = {"auth_token":auth_token,"urls":file_url}
            response = requests.post(f'https://{host_api_domain}/api/v2/remoteUploadAdd',headers=headers,json=data).json()
            if response['code'] != 200:
                return False;
            for url in response['acceptedUrls']:
                if url['url'] == file_url:
                    return "File Uploaded"
            return {"error":"URL Rejected"}
        else:
            return {"error":"Couldn't get AuthToken, check credentials"}
    else:
        return {"error":"No URL provided"}

    
    

    
    
    
    

# upload_file(api_key="45001454e3ffdc76bdb7ed7048934475ed9a1f53",file_path='test2')
print(extract_url(file_url="https://k2s.cc/file/b53e8a5a50c68/GM600.lnk",username="gijblyj@telegmail.com",password="Password@001"))
# print(check_url(file_url="https://k2s.cc/file/b53e8a5a50c68/GM600.lnk"))

# print(upload_remote(file_url="https://i.ibb.co/cDSFCXk/anime-girl-katana-tattoo-8k-wallpaper.jpg",username="gijblyjn@telegmail.com",password="Password@001"))