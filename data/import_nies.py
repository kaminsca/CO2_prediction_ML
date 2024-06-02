import requests
from requests.auth import HTTPBasicAuth
from tqdm import tqdm 
import tarfile

username = 'xxx'
password = 'xxx'

def download_file(url, local_filename):
    # Stream the download to handle large files
    with requests.get(url, auth=HTTPBasicAuth(username, password), stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            pbar = tqdm(total=int(r.headers['Content-Length']), unit='B', unit_scale=True, desc=local_filename)
            for chunk in r.iter_content(chunk_size=8192):
                pbar.update(len(chunk))
                f.write(chunk)
            pbar.close()
    return local_filename

def extract_tar_file(tar_file_name):
    with tarfile.open(tar_file_name, 'r') as tar:
        tar.extractall()
        print(f"Extracted {tar_file_name}")

with open('data/SWIRL3CO2_GU_V03.05.txt', 'r') as file:
    urls = [line.strip() for line in file]

for url in urls:
    # Extract filename from URL
    filename = url.split('/')[-1]
    try:
        print(f"Downloading {filename}...")
        download_file(url, filename)
        
        print(f"Extracting {filename}...")
        extract_tar_file(filename)
        
        print(f"Successfully downloaded and extracted {filename}!")
    except Exception as e:
        print(f"Failed to download or extract {filename}. Reason: {e}")