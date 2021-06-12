import json
import os
import sqlite3

class Setup:
  def __init__(self):
    self.data = {}
    self.client_id = None
    self.client_secret = None
    self.password = None
    self.user_agent = None
    self.username = None
    self.setup_reddit()
    self.default_sql_path = os.path.join(os.path.dirname(__file__), 'data/database.sqlite3')
    self.db_connect()
  
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

  def db_connect(self):
    #the first time you run main.py a file named 'database.sqlite3' will be created in data/
    db_connection = sqlite3.connect(self.default_sql_path)
    return db_connection