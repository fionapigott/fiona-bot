# fiona-bot
Niche millennial content aggregation (i.e., make a basic Twitter bot)

# Call your senators (get_representatives_bot.py):
## A simple bot to Tweet the phone numbers of your elected representatives
### Requirements:
- Python3
- tweepy
- requests
- pyyaml

### Public Twitter API access
This code depends on you having set up access to the Twitter Public API, so do that first (look up twurl for some instructions). I'm going to use the default .twurlrc setup for a credentials file. If you already have a .twurlrc, it should work. Otherwise, create one. It should look like this:

    --- 
    configuration: 
      default_profile: 
      - < your screen name >
      - < CONSUMER KEY >
    profiles: 
      < your screen name >: 
        < CONSUMER KEY >: 
          username: < your screen name >
          token: < TOKEN >
          secret: < SECRET >
          consumer_secret: < CONSUMER SECRET >
          consumer_key: < CONSUMER KEY >

### Google Civic API Access
You'll also need access to the Google Civic Information API. Information on that is here: https://developers.google.com/civic-information/

### Run your bot
After that access is set up, you shouldn't have to change anything else. 
Run `python get_representatives_bot.py` and @-mention your bot (from a different account!) to try it out.

