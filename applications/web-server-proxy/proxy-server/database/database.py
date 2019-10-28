# This file contains the database handlers

import os
import json

class Database:

    def __init__(self, db = 'database.json'):
        self.db = db
        data = {}
        data['proxy_admins'] = [{'email': "admin", 'passw': "admin"}] # {'email: email, 'passw': passw}
        data['sites_blocked'] = []
        data['private_mode_auth'] = [] # {'email: email, 'passw': passw}
        data['managers_credentials'] = [{'email': "admin", 'passw': "admin"}] # {'email: email, 'passw': passw}
        data['history'] = [] # {'url': '', 'accessed': '', 'last_modified': ''}
        data['cache'] = [] # 'url': {last_modified': "date", 'html': "<html>"}

        if os.stat(db).st_size == 0:
            with open(self.db, 'w') as f:
                json.dump(data, f)
            f.close()

    def clear_db(self):
        data = {}
        data['proxy_admins'] = [] # {'email: email, 'passw': passw}
        data['sites_blocked'] = []
        data['private_mode_auth'] = [] # {'email: email, 'passw': passw}
        data['managers_credentials'] = [] # {'email: email, 'passw': passw}
        data['cache'] = [] # 'url': {last_modified': "date", 'html': "<html>"}
        data['history'] = [] # {'url': '', 'accessed': '', 'last_modified': ''}

        if os.stat(self.db).st_size >= 0:
            with open(self.db, 'w') as f:
                json.dump(data, f)
            f.close()
    def clear_history(self):
        data = {}
        data['proxy_admins'] = self.read_from_db('proxy_admins')
        data['sites_blocked'] = self.read_from_db('sites_blocked')
        data['private_mode_auth'] = self.read_from_db('private_mode_auth')
        data['managers_credentials'] = self.read_from_db('managers_credentials')
        data['history'] = []

        data['cache'] = self.read_from_db('cache')
        with open(self.db, 'w') as f:
            json.dump(data, f)
        f.close()

    def clear_cache(self):
        data = {}
        data['proxy_admins'] = self.read_from_db('proxy_admins')
        data['sites_blocked'] = self.read_from_db('sites_blocked')
        data['private_mode_auth'] = self.read_from_db('private_mode_auth')
        data['managers_credentials'] = self.read_from_db('managers_credentials')
        data['history'] = self.read_from_db('history')
        data['cache'] = []

        with open(self.db, 'w') as f:
            json.dump(data, f)
        f.close()


    def url_in_list(self, url, l):
        for i in range (len(l)): # loop list
            if l[i]['url'] == url:
                return i
        return -1

    def write_to_db(self, key, val):
        #{'url': "testURL", 'last_modified':  str(datetime.now()), 'html': "<html><body><h1> TEST DB LINK</h1></body></html>"}
        data = {}
        with open(self.db) as f:
            data = json.load(f)
            try:
                if key == 'cache' or key == 'history':
                    # Check for duplicates
                    cache_index = self.url_in_list(val['url'], data[key])
                    if cache_index >= 0:
                        data[key][cache_index] = val
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

DEBUG = False

if DEBUG:
    db = Database()
    db.write_to_db('cache', {'url' : "www.google.com" ,'last_modified':  "10", 'html': "<html><body><h1> TEST DB LINK</h1></body></html>"})
    db.write_to_db('cache', {'url' : "www.google.com" ,'last_modified':  "11", 'html': "<html><body><h1> SHOULD REPLACE</h1></body></html>"})
    db.write_to_db('cache', {'url' : "www.yahoo.com" ,'last_modified':  "just now", 'html': "<html><body><h1> welcome to yahoo</h1></body></html>"})

    data = db.read_from_db('cache')
    for p in data:
        print('url: ' + p['url'])
        print('date: ' + p['last_modified'])
        print('html: \n' + p['html'])
        print('')





