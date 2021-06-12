from Classes import Setup

# IMPORTANT:
# the first time running you'll need to create a setup.txt file in the data directory
# copy the following line inside data.txt without the # 'pound' sign:
# {"setup": [{"client_id": "", "client_secret": "", "password": "", "user_agent": "testscript by u/", "username": ""}]}
# fill in each empty "" with info from your reddit account, see https://redditclient.readthedocs.io/en/latest/oauth/ for more info

# setup
print('running setup')
setup = Setup()

# program loop