from Classes import Bot
import praw

# IMPORTANT:
# the first time running you'll need to create a setup.json file in the data directory
# copy the next line of code (line 7) inside data.json without the # 'pound' sign
# {"setup": [{"client_id": "", "client_secret": "", "password": "", "user_agent": "testscript by u/", "username": ""}]}
# fill in each empty "" with info from your reddit account, see https://redditclient.readthedocs.io/en/latest/oauth/ for more info

# setup
print('\n running setup')
bot = Bot()
print('setup finished \n')

while True:
  # setup subreddit stream of comments
  for comment in bot.r.subreddit(bot.subreddits).stream.comments():
    bot.process_comments(comment)