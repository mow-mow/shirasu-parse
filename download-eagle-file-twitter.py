from requests_oauthlib import OAuth1Session
from datetime import datetime
from time import sleep
import os.path
import urllib.request
import json
import env

# twitter search word
search_text = "#カトラス生誕祭2023 -filter:retweet min_faves:100"
# Add Eagle Default Tag
default_tags= ["ガールズ&パンツァー", "カトラス"]
# Save Directory Name
save_folder="2023/カトラス生誕祭2023"


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

    print('status:' , id)
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
    print(default_tags + tags)
    
    annotation= r["user"]["name"]
    print(annotation)

    print(r["user"]["screen_name"])


    for media in medias:
        url = media["media_url_https"]

        name = url.split("/")
        pathname = dirname_abs + "/" + name[-1]
        print(pathname)
        urllib.request.urlretrieve(url + ":large", pathname)
        website = media["expanded_url"]


        str = {
            "name": os.path.splitext(name[-1])[0],
            "website": website,
            "tags": default_tags + tags,
            "annotation": annotation,
            "path": pathname
        }
        with open(dirname_abs + "/" + os.path.splitext(name[-1])[0] + ".json", 'w') as f:
            json.dump(str, f, ensure_ascii=False, indent=4)

        sleep(3)

    return False



def search_tweet_list():

    print("Search Tweet :" + search_text)
    url = "https://api.twitter.com/1.1/search/tweets.json"
    params = {
            "q": search_text,
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
        since_id = ids[0]
        for tweet_id in ids:
            download_image_by_id(tweet_id)
                
    print("Processing Exit !!")

if __name__ == "__main__":
    main()
