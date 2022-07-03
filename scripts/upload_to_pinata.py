import requests
import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import json

load_dotenv()

PINATA_BASE_URL = 'https://api.pinata.cloud'


def pinata_image_upload(image_path):
    file_endpoint = '/pinning/pinFileToIPFS'
    headers = {'pinata_api_key': os.getenv('PINATA_API_KEY'),
           'pinata_secret_api_key': os.getenv('PINATA_API_SECRET')
        }
    filename = image_path.split('/')[-1]
    with Path(image_path).open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + file_endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        print(response.json())

def pinata_json_upload(json_path, collectible_metadata):
    json_endpoint = "/pinning/pinJSONToIPFS"
    headers = {'Content-Type': 'application/json',
        'pinata_api_key': os.getenv('PINATA_API_KEY'),
        'pinata_secret_api_key': os.getenv('PINATA_API_SECRET')
        }
    filename = json_path.lower().split('/')[-1]

    payload = json.dumps({
    "pinataOptions": {
        "cidVersion": 1
    },
    "pinataMetadata": {
        "name": filename,
    },
    "pinataContent": {
        "name": collectible_metadata["name"],
        "description": collectible_metadata["description"],
        "image": collectible_metadata["image"],
        "attributes": [{"trait_type": "cuteness", "value": 100}],
    }
    })
    
    print(collectible_metadata["name"])
    response = requests.request("POST", PINATA_BASE_URL + json_endpoint, headers=headers, data=payload)
    print(response.text)



# def main():
#    pinata_image_upload()
#    pinata_json_upload()


# if __name__ == "__main__":
#     main()
