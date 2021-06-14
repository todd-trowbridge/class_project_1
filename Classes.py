import json
import praw

class Bot:
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

  def parse_comment(self, comment, search_term):
    # split text into a list of words
    body = comment.body
    word_list = body.split(' ')
    # number, original_unit_of_measure, new_number, new_unit_of_measure
    phrase = [0, 1, 2, 3]
    # search the words for the text paramater
    for word in word_list:
      if word == search_term:
        print('converting unit of measure')
        # set original_unit_of_measure in phrase
        phrase[1] = word
        # get index of preceding word
        preceding_word_index = word_list.index(word) - 1
        possible_int = word_list[preceding_word_index]
        if possible_int.isnumeric():
          # add number to phrase
          phrase[0] = possible_int
          if word == 'feet':
            phrase[1] = 'feet'
            phrase[2] = self.feet_to_meters(phrase[0])
            phrase[3] = 'meters'
            return phrase
          elif word == 'meters':
            phrase[1] = 'meters'
            phrase[1] = self.meters_to_feet(phrase[0])
            phrase[3] = 'feet'
            return phrase
        else: return False

  def feet_to_meters(self, feet):
    return round(float(feet) * 0.3048, 2)

  def meters_to_feet(self, meters):
    return round(float(meters / 0.3048), 2)

  def list_to_comment(self, list):
    original_number = list[0]
    original_unit_of_measure = list[1]
    new_number = list[2]
    new_unit_of_measure = list[3]

    return f'{original_number} {original_unit_of_measure} equals {new_number} {new_unit_of_measure}'