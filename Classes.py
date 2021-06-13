import json
from re import sub
from sqlite3.dbapi2 import connect
import praw
import sqlite3

class Bot:
  #init
  def __init__(self):
    self.terminal_red = '\033[91m'
    self.client_id = None
    self.client_secret = None
    self.password = None
    self.user_agent = None
    self.username = None
    # r is short for reddit
    self.r = self.setup_reddit()
    self.default_sql_path = 'data/database.sqlite3'
    self.db_connection = self.db_connect()
  
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

# sql stuff

  # connect to database and keep connection alive inside self.db_connection
  def db_connect(self):
    connection = sqlite3.connect(self.default_sql_path)
    cursor = connection.cursor()
    cursor.execute('SELECT SQLITE_VERSION()')
    version = cursor.fetchone()[0]
    print("  SQLite3 version: " + version)
    return connection

  # (user=string, karma=)
  def create_user_db(self, user, karma = 1000):
    connection = self.db_connection
    cursor = connection.cursor()
    try:
      cursor.execute(f"""
      INSERT INTO users (name, karma)
      VALUES('{user}', {karma});""")
      cursor.connection.commit()
      print(f'created {user=}')
    except:
      print(f'{self.terminal_red} error adding {user}')
  
  def select_user_db(self, user):
    connection = self.db_connection
    cursor = connection.cursor()
    try:
      cursor.execute(f"SELECT * from users WHERE name ='{user}'")
      row = cursor.fetchone()
      return row # (name=string, karma=int)
    except:
      print(f'{self.terminal_red} error selecting {user=}')
      return False

  def create_mention_db(self, mention_id):
    connection = self.db_connection
    cursor = connection.cursor()
    try:
      cursor.execute(f"""
      INSERT INTO mentions (id)
      VALUES('{mention_id}');""")
      cursor.connection.commit()
      print(f'mention added to db {mention_id=}')
    except:
      print(f'{self.terminal_red} error adding {mention_id=}')

  def select_mention_db(self, mention_id):
    connection = self.db_connection
    cursor = connection.cursor()
    try:
      cursor.execute(f"SELECT * from mentions WHERE id ='{mention_id}'")
      mention = cursor.fetchone()
      print(mention['id'])
      return mention # (id=string)
    except:
      print(f'{self.terminal_red} error selecting {mention_id}')

  def check_if_first_contact(self, mention_author):
    if not self.select_user_db(mention_author):
      print(f'first contact with user {mention_author}')
      self.create_user_db(mention_author)
    else:
      print(f'not first contact with user {mention_author}')