# -*- coding: utf-8 -*-
"""
@author: JosephNelson
"""


'''
Getting Data from APIs: Using authentication

We'll now perform the same process, but we'll make use of an authentication token.

Authentication tokens enable websites to:
-Easier control access to their data
-Monitor individual users of their API
-Rate limit individual users via their token IDs

Getting an API key from data.gov is easy. Sign up here: https://api.data.gov/signup/

It is incredibly important that you do not share your API key with anyone (especially important to not put it on your Github)

The API we're using is the Department of Commerce API: https://www.commerce.gov/page/api-documentation-commercegov

'''

import requests
import json
import pandas as pd

my_key = ########

# make a demo request
r = requests.get('https://api.data.gov/nrel/alt-fuel-stations/v1/nearest.json?api_key='+my_key+'&location=Denver+CO')

# check out status
r

# print the test
r.text

# format to json
json_data = json.loads(r.text)

# work with this json object
json_data['latitude']

'''
Let's get a bit more advanced!

Time to use the Dept of Commerce API
'''

r = requests.get('https://api.commerce.gov/api/blogs/?api_key='+my_key)

# let's identify data in our object
read_json(json_data['data'][0]['id'])

# how many responses are in data?
len(json_data['data'])

#Let's create an empty pandas dataframe with our columns
doc_data = pd.DataFrame(columns=["id_no"])

# let's make a df with all our new data
for x in range(0,len(json_data['data'])):
    id_no = json_data['data'][x]['id']
    doc_data.loc[len(doc_data)]=[int(id_no)]

# what's in our doc?
doc_data.head()
