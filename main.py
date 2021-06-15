from Classes import Bot
from praw.models.util import stream_generator
import sqlite3

# IMPORTANT:
# the first time running you'll need to create a setup.json file in the data directory
# copy the next line of code (line 7) inside data.json without the # 'pound' sign
# {"setup": [{"client_id": "", "client_secret": "", "password": "", "user_agent": "testscript by u/", "username": ""}]}
# fill in each empty "" with info from your reddit account, see https://redditclient.readthedocs.io/en/latest/oauth/ for more info

# setup
print('\nrunning setup')
bot = Bot()
list_of_unparsed_comments = []
print('setup finished\n')

while True:
  # setup subreddit stream of comments
  for comment in bot.r.subreddit('dc_bot_testing').stream.comments():
    list_of_unparsed_comments.append(comment)
    if comment.author != 'toddthestudent':
      unparsed_comment = list_of_unparsed_comments.pop()
      if bot.parse_comment(unparsed_comment):
        bot.save_comment_to_db(unparsed_comment)
        bot.r.comment(id=unparsed_comment.id)
        print(f'posting conversion to comment id = {unparsed_comment.id}')
        comment.reply(bot.list_to_comment())
        bot.reset_list()