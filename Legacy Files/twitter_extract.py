import tweepy as tw
import pandas as pd
from dotenv import load_dotenv
import os 
from datetime import datetime

# 1. Add your own Twitter keys/secrets to a .env file in this directory
# 2. ensure the correct start date and quantity of tweets to collect
# 3. copy/paste hashtags into list space below

date_since = "2021-03-01"
how_many_tweets = 4000

### LIMITED KEYWORD LIST, KM BATCH
# keywordlist = """
# covid_19 astrazeneca
# corona astrazeneca
# coronavirus astrazeneca
# coronavirusupdates astrazeneca
# cepi
# coronavaccine
# coronavirusvaccine
# covax
# covid19vaccine
# covidvaccine
# gavi
# glyphosate
# mrna
# nvic
# oxfordvaccine
# pharmagreed
# rna
# sputnikv
# vaccinessavelives
# """

keywordlist = """
vaccine
vaccination
vaccinate
pfizerbiontech
pfizercovidvaccine
pfizervaccine
covid pfizer
covid19 pfizer
covid-19 pfizer
covid_19 pfizer
corona pfizer
covidvaccine pfizer
coronavirus pfizer
coronavirusupdates pfizer
modernavaccine
modernacovidvaccine
covid moderna
covid19 moderna
covid-19 moderna
covid_19 moderna
corona moderna
coronavirus moderna
coronavirusupdates moderna
biontechvaccine
biontechcovidvaccine
covid biontech
covid19 biontech
covid-19 biontech
covid_19 biontech
corona biontech
coronavirus biontech
coronavirusupdates biontech
azvaccine
astrazenecacovidvaccine
astrazenecavaccine
covid astrazeneca
covid19 astrazeneca
covid-19 astrazeneca
covid_19 astrazeneca
corona astrazeneca
coronavirus astrazeneca
coronavirusupdates astrazeneca
cepi
coronavaccine
coronavirusvaccine
covax
covid19vaccine
covidvaccine
gavi
glyphosate
mrna
nvic
oxfordvaccine
pharmagreed
rna
sputnikv
vaccinessavelives
vax
vaxx
vaxxx
covidiots
getvaccinated
iwillgetvaccinated
thisisourshot
vaccineworks
vaccinessavelives
depopulation
eugenics
greatreset
notocoronavirusvaccines
mybodymychoice
peoplesbodyyourchoice
iwillnotcomply
endthelockdown
kungflu
plandemic
"""

#set current working directory to where this file is saved
#thisdir = globals()['_dh'][0] + "\\"  ##jupyter notebook
thisdir = os.path.dirname(os.path.abspath(__file__)) + "\\" 
os.chdir(thisdir)

#load hidden credentials and values
load_dotenv() 

# ADD YOUR OWN KEYS/SECRETS TO A .env FILE IN THIS DIRECTORY
apikey = os.getenv("apikey")
apisecret = os.getenv("apisecret")
accesstoken = os.getenv("accesstoken")
accesssecret = os.getenv("accesssecret")

# connect to twitter using creds above
auth = tw.OAuthHandler(apikey, apisecret)
auth.set_access_token(accesstoken, accesssecret)
api = tw.API(auth, wait_on_rate_limit=True)

# split new line delimited list above into clean list
keywordlist = keywordlist.split('\n')
keywordlist = [x.strip() for x in keywordlist if x.strip()]

## OPTIONAL CODE TO CONVERT KEYWORDS TO HASHTAGS. NOT DONE BY COVAXXY PROJECT
# hashtaglist = [' '.join(["#"+y for y in x.split(' ')]) for x in keywordlist]

# iterate through words, collect tweets, save as dicts in a list
dict_list = []
counter = 0
for search_words in keywordlist:
    print(search_words)
    try:
        # Collect tweets
        tweets = tw.Cursor(api.search,
                    q=search_words,
                    lang="en",
                    since=date_since).items(how_many_tweets)

        # Iterate and print tweets
        for tweet in tweets:
            try:
                thed = dict(tweet._json)
                cleand = {'scraped_hashtag': search_words.strip(),
                    'scraped_order': counter}

                keepers = ['created_at', 'id_str', 'text', 'truncated', 
                            'in_reply_to_screen_name', 
                            'retweet_count', 'favorite_count', 'lang']
                for k in keepers:
                    cleand[k] = thed[k]

                cleand['screen_name'] = thed['user']['screen_name']
                cleand['user_name'] = thed['user']['name']
                cleand['user_description'] = thed['user']['description']
                cleand['user_verified'] = thed['user']['verified']
                cleand['user_followers_count'] = thed['user']['followers_count']

                cleand['hashtags'] = [x['text'] for x in thed['entities']['hashtags']]
                cleand['symbols'] = thed['entities']['symbols']

                if 'retweeted_status' in thed.keys():
                    p1 = thed['retweeted_status']['user']['screen_name']
                    cleand['og_tweet_by'] = p1 + "; " + thed['retweeted_status']['user']['name']
                    cleand['og_tweet_truncated'] = thed['retweeted_status']['truncated']

                dict_list.append(cleand)
            except:
                pass
        counter += 1
    except:
        pass

# convert list of collected dicts into dataframe, 
# then save as file with datetime in this directory
df = pd.DataFrame(dict_list)
dt = datetime.now().strftime("%y%m%d_%H%M")
df.to_csv(f'hashtag_output_{dt}.csv', encoding="utf-8")
