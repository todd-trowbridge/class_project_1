import json
import re
from sqlite3.dbapi2 import connect
import praw
import sqlite3
# import uuid

class Bot:
  #init
  def __init__(self):
    self.client_id = None
    self.client_secret = None
    self.password = None
    self.user_agent = None
    self.username = None
    # r is short for reddit
    self.r = self.setup_reddit()
  
  # setup (ran once on start of main.py)
  def setup_reddit(self):
    # load init with data from data/setup.txt
    with open('data/setup.json') as json_file:
      self.data = json.load(json_file)
      for item in self.data['setup']:
        self.client_id = item['client_id']
        self.client_secret = item['client_secret']
        self.password = item['password']
        self.user_agent = item['user_agent']
        self.username = item['username']
        print('  client_id: ' + str(self.client_id))
        print('  client_secret: **************')
        print('  username: ' + str(self.username))
        print('  user_agent: ' + str(self.user_agent))
        return praw.Reddit(client_id=self.client_id, client_secret=self.client_secret, user_agent = self.user_agent, username = self.username, password = self.password)
        # comment the above line and uncomment the two lines below to check reddit connection
        # reddit = praw.Reddit(client_id=self.client_id, client_secret=self.client_secret, user_agent = self.user_agent, username = self.username, password = self.password)
        # print('  from reddit.com: logged in as ' + str(reddit.user.me()))

  def parse_comment_for_keyword(self, comment, text):
    # split text into a list of words
    word_list = []
    converted_phrase = ()
    original_number = None
    # search the words for the text paramater
    for word in word_list:
      if word == text:
        print(f'found {word}')
        if converted_phrase[1] == 'feet': converted_phrase[1] = 'meters'
        else: converted_phrase[1] = word
        index_of_match = word_list.index(word)
        # check if the preceeding word is a number
        possible_number = word_list.pop(index_of_match - 1)
        if possible_number.isnumeric():
          original_number = int(possible_number)
          converted_phrase[0] = self.feet_to_meters(original_number)
      print(f'{original_number} feet is {converted_phrase[0]} {converted_phrase[1]}')
    return converted_phrase

  def feet_to_meters(self, feet):
    return feet * 0.3048




# old / unused functions

  #setup sql (add to init)
  # self.default_sql_path = 'data/database.sqlite3'
  # self.db_connection = self.db_connect()

  # def generate_uuid(self):
  #   return uuid.uuid4()

  # # returns T/F
  # def check_if_first_contact(self, mention_author):
  #   if not self.select_user_db(mention_author):
  #     print(f'{mention_author} is making a first bet')
  #     self.create_user_db(mention_author)
  #     return True
  #   else:
  #     print(f'{mention_author} is making a new bet')
  #     return False

  # def reply_to_message(self, message, uuid_text):
  #   uuid, text = uuid_text
  #   # reddit.redditor("spez").message("TEST", "test message from PRAW")
  #   comment = self.r.comment(id=message.id)
  #   comment.reply(text)
  #   return uuid

  # # connect to database and keep connection alive inside self.db_connection
  # def db_connect(self):
  #   connection = sqlite3.connect(self.default_sql_path)
  #   cursor = connection.cursor()
  #   cursor.execute('SELECT SQLITE_VERSION()')
  #   version = cursor.fetchone()[0]
  #   print("  SQLite3 version: " + version)
  #   return connection

  # # (user=string, cash=)
  # def create_user_db(self, user, cash = 1000):
  #   connection = self.db_connection
  #   cursor = connection.cursor()
  #   try:
  #     cursor.execute(f"""
  #     INSERT INTO users (name, cash)
  #     VALUES('{user}', {cash});""")
  #     cursor.connection.commit()
  #     print(f'created {user=}')
  #   except:
  #     print(f'{self.terminal_red} error adding {user}')

  # def select_user_db(self, user):
  #   connection = self.db_connection
  #   cursor = connection.cursor()
  #   try:
  #     cursor.execute(f"SELECT * from users WHERE name ='{user}'")
  #     row = cursor.fetchone()
  #     return row # (name=string, cash=int)
  #   except:
  #     print(f'{self.terminal_red} error selecting {user=}')
  #     return False

  # def select_mention_db(self, mention_id):
  #   connection = self.db_connection
  #   cursor = connection.cursor()
  #   try:
  #     cursor.execute(f"SELECT * from mentions WHERE id ='{mention_id}'")
  #     mention = cursor.fetchone()
  #     print(mention)
  #   except:
  #     print(f'{self.terminal_red} error selecting {mention_id}')

  # def create_bet_db(self, mention, uuid=None):
  #   connection = self.db_connection
  #   cursor = connection.cursor()
  #   try:
  #     cursor.execute(f"""
  #     INSERT INTO bets (uuid))
  #     VALUES('{uuid}');""")
  #     cursor.connection.commit()
  #     print(f'bet added to db, {uuid=}')
  #   except:
  #     print(f'{self.terminal_red} error adding {mention.id=}')

  # def reply_to_mention(self, mention, text):
  #   self.parse_comment(mention.body,)
  #   # reddit.redditor("spez").message("TEST", "test message from PRAW")
  #   self.r.redditor(mention.author).message('you rang?', text)
  #   self.create_bet_db(mention, uuid)
  #   return uuid