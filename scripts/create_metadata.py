#!/usr/bin/python3
import os
import requests
import json
from brownie import AdvancedCollectible, network
from metadata import sample_metadata
from scripts.helpful_scripts import get_breed_name
from pathlib import Path
from dotenv import load_dotenv
from scripts.dog_tokenURI_dict import tokenURI_mappings
from scripts.dog_imageURI_dict import imageURI_mappings
from scripts.upload_to_pinata import pinata_upload

load_dotenv()

def main():
    print("Working on " + network.show_active())
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_collectibles)
    )
    write_metadata(number_of_collectibles)

def write_metadata(token_id, folder_name="PUG"):
    # image_folder = "./img"
    # for folder_name in os.listdir(image_folder):
        breed_folder_location = f"./img/{folder_name}"
        for file_name in os.listdir(breed_folder_location):
            name = file_name.split(".")[0]
            print(name)
            collectible_metadata = sample_metadata.metadata_template
            metadata_file_name = (
                f"./metadata/{network.show_active()}/"
                + str(token_id)
                + "-"
                + folder_name
                + ".json"
            )
            if Path(metadata_file_name).exists():
                print(
                    f"{metadata_file_name} already exists, delete it to overwrite!"
                )
            else:
                print("Creating Metadata file: " + metadata_file_name)
                collectible_metadata["name"] = folder_name
                collectible_metadata["description"] = "An adorable {} pup!".format(collectible_metadata["name"])
                image_to_upload = None
                lowercase_name = ''
                image_path= ""
                if os.getenv("UPLOAD_TO_IPFS") == "true":
                    lowercase_name = name.lower().replace('_', '-')
                    image_path = f"./img/{folder_name}/{lowercase_name}.png"
                    image_to_upload = upload_to_ipfs(image_path, lowercase_name, folder_name)
                image_to_upload = (
                    imageURI_mappings[folder_name] if not image_to_upload else image_to_upload
                )
                collectible_metadata["image"] = image_to_upload
                if os.getenv("UPLOAD_TO_PINATA") == "true":
                    pinata_upload(image_path)
                with open(metadata_file_name, "w") as file:
                    json.dump(collectible_metadata, file)
                if os.getenv("UPLOAD_TO_IPFS") == "true":
                    upload_to_ipfs(metadata_file_name, lowercase_name, folder_name)
                    print("Metadata uploaded successfully!")


def upload_to_ipfs(filepath, file_name, folder_name):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = (
            os.getenv("IPFS_URL")
            if os.getenv("IPFS_URL")
            else "http://localhost:5001"
        )
        response = requests.post(ipfs_url + "/api/v0/add",
                                 files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        # file_name = filepath.split("/")[-1]
        file_uri = f"ipfs://{ipfs_hash}?filename={file_name}"
        file_extension = file_name.split(".")[-1]
        save_URI(folder_name, file_uri, file_extension)
        print(file_uri)
    return file_uri


def save_URI(name, uri, extension):
    if(extension == "json"):
        uriArray = tokenURI_mappings[name]
        uriArray.append(uri)
    else:
        uriArray = imageURI_mappings[name]
        uriArray.append(uri)




    
    
