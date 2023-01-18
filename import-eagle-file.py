from requests_oauthlib import OAuth1Session
from datetime import datetime
from time import sleep
import os.path
import urllib.request
import json
import env
import glob
import requests

# import directory name
dirname = "twitter/2023/"


###################################

dirname_abs = os.path.dirname(os.path.abspath(__file__)) + "/download/" + dirname

def init_eagle_folder(folder_abs):
    print("[Eagle] check Folders : " + folder_abs)

    folders = folder_abs.split('/')
    response = requests.get('http://localhost:41595/api/folder/list')
    return make_eagle_folder(response.json()["data"], folders, 0, "")

def make_eagle_folder(r, folders, i, parent_id):
    item = next((item for item in r if item['name'] == folders[i]), None)
    if item:
            print("Folder Exists : "  + folders[i] + "(" + item['id'] + ")")
            i = i + 1
            if len(folders) -1 == i:
                return item['id']
            
            return make_eagle_folder(item['children'], folders, i, item['id'])


    else :
        print("Folder Not Exists : "  + folders[i])
        print("Folder Create =>" + folders[i])
        r = requests.post('http://localhost:41595/api/folder/create', json={
        "folderName": folders[i],
        "parent": parent_id
        })
        response = requests.get('http://localhost:41595/api/folder/list')
        r = response.json()
        return make_eagle_folder(r["data"], folders, 0, "")

def main():

    pathname = dirname_abs + "/**/"
    print("=> search directory :" + pathname)

    dirs = glob.glob(pathname)
    for dir in dirs:
        print(dir)

        folder_id=init_eagle_folder(dir.replace(os.path.dirname(os.path.abspath(__file__)) + "/download/", ""))

        pathname = dir + "*.json"
        print("==> search eagle file :" + pathname)
        files = glob.glob(pathname)
        for file in files:
            print(file)

            json_open = open(file, 'r')
            json_load = json.load(json_open)
            json_load["folderId"] = folder_id
            print(json_load)

            r = requests.post('http://localhost:41595/api/item/addFromPath', json=json_load)
            print(r.json())



if __name__ == "__main__":
    main()
