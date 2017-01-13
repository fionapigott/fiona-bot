# Author: Fiona Pigott
# Date: 1/13/2017
import tweepy
import yaml
import requests
import re
import json
import random

# set up the Tweepy Twitter API access
# I assume that your creds file looks like the creds file that Twurl creates
creds = yaml.load(open("fionabot.creds"))
keys = creds["profiles"][creds["configuration"]["default_profile"][0]][creds["configuration"]["default_profile"][1]]

auth = tweepy.OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
auth.set_access_token(keys["token"], keys["secret"])
api = tweepy.API(auth, retry_delay = 5)

# access gov't data on Google's civic data API
# this entire file has one key, "key: < API key >"
google_key = yaml.load(open("google-civic-api.creds"))["key"]
base_civic_api_url = "https://www.googleapis.com/civicinfo/v2/representatives"

def get_zipcode(text):
    '''
    Get the zipcode from the Tweet
    '''
    regex_parsed = re.search('(\d{5})([- ])?(\d{4})?', text)
    if regex_parsed is None:
        return ""
    else:
        return regex_parsed.group(0).strip()

def get_official(zipcode, role = "United States House of Representatives"):
    '''
    Get the official that we want to Tweet
    '''
    response = requests.get(base_civic_api_url, 
            params = {"key":google_key,"address":zipcode})
    response_dict = json.loads(response.text)
    officials = []
    for office in response_dict["offices"]:
        if role in office["name"]:
            for i in office["officialIndices"]:
                officials.append(response_dict["officials"][i])
    return officials, role

def format_tweet(officials, role = "United States House of Representatives"):
    '''
    Create the text of the Tweet
    '''
    if "house" in role.lower():
        rep = "Your US House representative is {}!".format(officials[0]["name"])
        call = "Call them at: {}".format("or".join([x.replace(" ","") for x in officials[0]["phones"]]))
        tweet = rep + "\n" + call
    if "senate" in role.lower():
        tweet = "Your US Senate representatives are\n{}".format(
                "\nand\n".join([x["name"] + " at " + x["phones"][0] for x in officials]))
    return tweet

def non_zipcode_response():
    '''
    If we don't have a zipcode, prompt for one
    '''
    choices = ["I'm just a bot! Don't waste time talking to me, @ me with your zipcode and talk to your congressman instead!"]
    return(random.choice(choices))

class ZipcodeListener(tweepy.StreamListener):
    '''
    Listen for Tweets to my Twitter account
    '''
    def on_status(self, status):
        greeting = "Hi @" + status.author.screen_name + ",\n"
        zipcode = get_zipcode(status.text)
        if zipcode != "":
            for role_ in ["United States House of Representatives", "Senate"]:
                official, r = get_official(zipcode, role = role_)
                api.update_status(greeting + format_tweet(official, role = r)
                        , in_reply_to_status_id = status.id_str)
        else:
            api.update_status(greeting + non_zipcode_response(), 
                    in_reply_to_status_id = status.id_str)

zipcode_listener = ZipcodeListener()
zipcode_stream = tweepy.Stream(auth = api.auth, listener=zipcode_listener)

zipcode_stream.filter(track = [creds["configuration"]["default_profile"][0]])
