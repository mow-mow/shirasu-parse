from requests_oauthlib import OAuth1Session
from datetime import datetime
from time import sleep
import os.path
import urllib.request
import json
import env

# twitter search word
search_text = "#ケイ生誕祭2023 -filter:retweet min_faves:100"
# Add Eagle Default Tag
default_tags= ["ガールズ&パンツァー", "ケイ"]
# Save Directory Name
save_folder="2023/ケイ生誕祭2023"


#################################################
user_id = env.USER_ID
CONSUMER_KEY = env.CONSUMER_KEY
CONSUMER_SECRET = env.CONSUMER_SECRET
ACCESS_TOKEN = env.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = env.ACCESS_TOKEN_SECRET

dirname = "/download/twitter/" + save_folder
dirname_abs = os.path.dirname(os.path.abspath(__file__)) + dirname

os.makedirs(dirname_abs, exist_ok=True)


twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

def download_image_by_id(id):
    url = "https://api.twitter.com/1.1/statuses/show.json"
    res = twitter.get(url, params={'id': id})

    print('status:', id)
    print("---------------")
    print(res)
    if res.status_code != 200:
        print ("HTTP Staus Error!")
        return False

    if 'media_url_https' not in res.text:
        print ("No media_url_https!")
        return False

    r = json.loads(res.text)

    try:
        medias = r["extended_entities"]["media"]
    except KeyError:
        return False

    print(json.dumps(r, indent=2))

    tags = [hashtag["text"] for hashtag in r["entities"]["hashtags"]]            
    print("[tags]", default_tags + tags)
    
    annotation= r["user"]["name"]
    print("[annotation]", annotation)
    print("* ", r["user"]["screen_name"])

    print("====> Start Save File")
    print("Media File found :", len(medias))
    print("------------")
    for i, media in enumerate(medias):
        print("<<Media Info>")
        pathname = dirname_abs + "/" + name[-1]
        print("[path]", pathname)
        website = media["expanded_url"]
        print("[website]", website)

        url = media["media_url_https"]
        name = url.split("/")

        print("------")
        print("Download Media File :", url, "=> ", pathname)
        urllib.request.urlretrieve(url + ":large", pathname)


        str = {
            "name": os.path.splitext(name[-1])[0],
            "website": website,
            "tags": default_tags + tags,
            "annotation": annotation,
            "path": pathname
        }
        eagle_file_pathname = dirname_abs + "/" + os.path.splitext(name[-1])[0] + ".json"
        print("------")
        print("Create Eagle File :", eagle_file_pathname)
        with open(eagle_file_pathname, 'w') as f:
            json.dump(str, f, ensure_ascii=False, indent=4)
        print("------")

    sleep(3)
    print("[", i+1, "/", len(medias), "] Download Complete")
    print("------------")
    return False



def search_tweet_list():

    print("Search Tweet :" + search_text)
    url = "https://api.twitter.com/1.1/search/tweets.json"
    params = {
            "q": search_text,
            "count" : 100,
            "lang": "ja",
        }

    res = twitter.get(url, params=params)

    print(res)
    if res.status_code != 200:
        print("Tweet Search Error !")
        return False
    
    print("Tweet Search Succucess!")
    r = json.loads(res.text)
    return [tweet["id"] for tweet in r["statuses"] if 'id_str' in tweet]


def main():
    ids = search_tweet_list()
    if ids :
        print("Find ", len(ids), " tweet")
        for i, id in enumerate(ids):
            print("------------------")
            print ("[", i+1, "/", len(ids), " ] Download Image Start ! ", id)
            print("------------------")
            download_image_by_id(id)
                
    print("Processing Exit !!")

if __name__ == "__main__":
    main()
