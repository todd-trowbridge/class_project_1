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

while True:
  for mention in stream_generator(bot.r.inbox.mentions, skip_existing=True):
    bot.create_mention_db(mention.id)
    # step 0 (user not in db)
    if bot.check_if_first_contact(mention.author.name): print('first contact')
    step = bot.get_step_for_mention(mention.id)
    # step 1
    if step == 1:
      if bot.parse_mention_comment(mention.id, 'I bet'):
        print('offering bet')
        update_step = bot.update_mention_step(mention.id, 2)
        bot.db_connection.commit()
        print(f'update step = {update_step}')
    
    mention.mark_read()