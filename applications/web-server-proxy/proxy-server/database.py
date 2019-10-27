# This file contains the ProxyManager class which handle all the operations
# done in the proxy-settings page of the project

import os
import cache
from cache import *  # point of access to cache files
import json


class Database:

    def __init__(self, db = 'database.json'):
        self.db = db
        data = {}
        data['proxy_admins'] = [] # {'email: email, 'passw': passw}
        data['sites_blocked'] = []
        data['private_mode_auth'] = [] # {'email: email, 'passw': passw}
        data['managers_credentials'] = [] # {'email: email, 'passw': passw}
        data['cache'] = [] # 'url': {last_modified': "date", 'html': "<html>"}
        with open(self.db, 'w') as f:
            json.dump(data, f)
        f.close()
        #End Initialization

    def url_in_cache_list(self, url, cache_list):
        for i in range (len(cache_list)): # loop list
            if cache_list[i]['url'] == url:
                return i
        return -1

    def write_to_db(self, key, val):
        #{'url': "testURL", 'last_modified':  str(datetime.now()), 'html': "<html><body><h1> TEST DB LINK</h1></body></html>"}
        data = {}
        with open(self.db) as f:
            data = json.load(f)
            try:
                if key == 'cache':
                    # Check for duplicates
                    cache_index = self.url_in_cache_list(val['url'], data['cache'])
                    if cache_index >= 0:
                        data['cache'][cache_index] = val
                    else:
                        data[key].append(val)
                else:  
                    data[key].append(val)
            except KeyError as e:
                print("write_to_db failed because key: " + key + " not found. error: " + e)
        f.close()
        with open(self.db, 'w') as w:
            json.dump(data, w)
        w.close()
        
    def read_from_db(self, key):
        #{'url': "testURL", 'last_modified':  str(datetime.now()), 'html': "<html><body><h1> TEST DB LINK</h1></body></html>"}
        data = {}
        with open(self.db) as f:
            data = json.load(f)
            try:
                return data[key]
            except KeyError as e:
                print("read_from_db failed because key: " + key + " not found. error: " + e)

DEBUG = True

if DEBUG:
    db = Database()
    db.write_to_db('cache', {'url' : "www.google.com" ,'last_modified':  "10", 'html': "<html><body><h1> TEST DB LINK</h1></body></html>"})
    db.write_to_db('cache', {'url' : "www.google.com" ,'last_modified':  "11", 'html': "<html><body><h1> SHOULD REPLACE</h1></body></html>"})

    data = db.read_from_db('cache')
    for p in data:
        print('url: ' + p['url'])
        print('date: ' + p['last_modified'])
        print('html: \n' + p['html'])
        print('')





