from Classes import Bot
from praw.models.util import stream_generator

# IMPORTANT:
# the first time running you'll need to create a setup.json file in the data directory
# copy the next line of code (line 7) inside data.json without the # 'pound' sign
# {"setup": [{"client_id": "", "client_secret": "", "password": "", "user_agent": "testscript by u/", "username": ""}]}
# fill in each empty "" with info from your reddit account, see https://redditclient.readthedocs.io/en/latest/oauth/ for more info

# setup
print('running setup')
bot = Bot()

# todo program loop

# testing:
while True:
  for mention in stream_generator(bot.r.inbox.mentions, skip_existing=True):
    mention.mark_read()
    print(mention.id)
    print(mention.submission)
    bot.create_mention_db(mention.id)