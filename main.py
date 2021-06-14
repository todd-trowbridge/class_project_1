from Classes import Bot
from praw.models.util import stream_generator

# IMPORTANT:
# the first time running you'll need to create a setup.json file in the data directory
# copy the next line of code (line 7) inside data.json without the # 'pound' sign
# {"setup": [{"client_id": "", "client_secret": "", "password": "", "user_agent": "testscript by u/", "username": ""}]}
# fill in each empty "" with info from your reddit account, see https://redditclient.readthedocs.io/en/latest/oauth/ for more info

# setup
print('\nrunning setup')
bot = Bot()
comments = []
print('setup finished\n')

while True:
  # setup subreddit stream of comments
  for comment in bot.r.subreddit('dc_bot_testing').stream.comments(skip_existing=True):
    comment_id = comment.id
    comments.append(comment)
    for comment in comments:
      if comment.author != 'toddthestudent':
        comment = comments.pop()
        text_string_to_search = 'feet'
        converted_phrase = bot.parse_comment(comment, text_string_to_search)
        if converted_phrase == False:
          pass
        else:
          comment = bot.r.comment(id=comment_id)
          comment.reply(bot.list_to_comment(converted_phrase))
      else: comments.pop()