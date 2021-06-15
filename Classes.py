import json
import sqlite3
import praw

class Bot:
  def __init__(self):
    self.client_id = None
    self.client_secret = None
    self.password = None
    self.user_agent = None
    self.username = None
    self.list_of_conversions = ['feet', 'meter', 'meters', 'celsius', 'fahrenheit']
    self.phrase = [0, 1, 2, 3]
    self.db = self.setup_db()
    self.list_of_parsed_comments = []
    # run setup and assign praw reddit to self.r
    self.r = self.setup()
  
  # setup (ran once on start of main.py)
  def setup(self):
    self.list_of_parsed_comments = self.load_data()
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

  def parse_comment(self, comment):
    # split text into a list of words
    body = comment.body
    word_list = body.split(' ') 
    # search the words for the text paramater
    try:
      for word in word_list:
        if word.lower() in self.list_of_conversions:
          # get index of preceding word
          preceding_word_index = word_list.index(word)
          preceding_word_index -= 1
          possible_float = word_list[preceding_word_index]
          # check if preceding word is a float
          # if float() fails return False
          if word.lower() == 'feet':
            self.phrase[0] = possible_float
            float(possible_float)
            self.phrase[1] = 'feet'
            self.phrase[2] = self.feet_to_meters()
            self.phrase[3] = 'meters'
            return True
          elif word.lower() == 'meters':
            self.phrase[0] = possible_float
            float(possible_float)
            self.phrase[1] = 'meters'
            self.phrase[2] = self.meters_to_feet()
            self.phrase[3] = 'feet'
            return True
          elif word.lower() == 'celsius':
            self.phrase[0] = possible_float
            float(possible_float)
            self.phrase[1] = 'celsius'
            self.phrase[2] = self.celsius_to_fahrenheit()
            self.phrase[3] = 'fahrenheit'
            print(f'{self.phrase[2]}')
            return True
          elif word.lower() == 'fahrenheit':
            self.phrase[0] = possible_float
            float(possible_float)
            self.phrase[1] = 'celsius'
            self.phrase[2] = self.celsius_to_fahrenheit()
            self.phrase[3] = 'fahrenheit'
            print(f'{self.phrase[2]}')
            return True
          else:
            return False
    except:
      return False

  def feet_to_meters(self):
    print('converting feet to meters')
    number_to_convert = float(self.phrase[0])
    return round(number_to_convert * 0.3408, 2)

  def meters_to_feet(self):
    print('converting meters to feet')
    number_to_convert = float(self.phrase[0])
    return round(number_to_convert / 0.3408, 2)

  def celsius_to_fahrenheit(self):
    print('converting celsius to fahrenheit')
    number_to_convert = float(self.phrase[0])
    converted_number = (((number_to_convert/5)*9)+32)
    return round(converted_number, 2)

  def fahrenheit_to_celsius(self):
    print('converting fahrenheit to celsius')
    number_to_convert = float(self.phrase[0])
    converted_number = (((number_to_convert-32)*5)/9)
    return round(converted_number, 2)

  def list_to_comment(self):
    if self.phrase[1] == 'celsius' or 'fahrenheit':
      return f'{self.phrase[0]}° {self.phrase[1]} equals {self.phrase[2]}° {self.phrase[3]}'
    else:
      return f'{self.phrase[0]} {self.phrase[1]} equals {self.phrase[2]} {self.phrase[3]}'

  def reset_list(self):
    self.phrase = [0, 1, 2, 3]

  def setup_db(self):
    return sqlite3.connect("data/db.sqlite3")

  def load_data(self):
    cursor = self.db.cursor()
    cursor.execute('SELECT * from comments;')
    comments = cursor.fetchall()
    print(comments)
    return comments

  def save_comment_to_db(self, comment):
    try:
      comment_id = comment.id
      cursor = self.db.cursor()
      cursor.execute(f"INSERT INTO comments (id) values ( '{comment_id}' );")
      self.db.commit()
      self.list_of_parsed_comments.append(comment.id)
      print('commited to db')
    except(sqlite3.IntegrityError):
        print('error adding comment')