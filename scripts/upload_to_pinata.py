import requests
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


PINATA_BASE_URL = 'https://api.pinata.cloud'
endpoint = '/pinning/pinFileToIPFS'
# Change this to upload a different file

headers = {'pinata_api_key': os.getenv('PINATA_API_KEY'),
           'pinata_secret_api_key': os.getenv('PINATA_API_SECRET')}


def pinata_upload(image_path):
    filename = image_path.split('/')[-1]
    with Path(image_path).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        print(response.json())



def main():
   pinata_upload()


# if __name__ == "__main__":
#     main()
