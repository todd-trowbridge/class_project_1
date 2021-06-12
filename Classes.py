import praw
import json

class Setup:
  def __init__(self):
    self.data = {}
    self.client_id = None
    self.client_secret = None
    self.password = None
    self.user_agent = None
    self.username = None
    self.setup()
  
  def setup(self):
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