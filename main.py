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
    # create user if mention.author.name is not in users db
    if bot.check_if_first_contact(mention.author.name): print('first contact')
    # get step
    step1 = bot.get_step_for_mention(mention.id)
    # branch for step 1 (user makes an offer)
    if step1 == 1:
      if bot.parse_mention_comment(mention.id, 'I bet'):
        print('offering bet')
        update_step = bot.update_mention_step(mention.id, 2)
        bot.db_connection.commit()
        # todo update offered_bets table
        print(f'update step = {update_step}')
    # get step
    step2 = bot.get_step_for_mention(mention.id)
    # branch for step 2
    if step2 == 2:
      print('pick up here tomorrow')
    
    mention.mark_read()