# This file contains the ProxyManager class which handle all the operations
# done in the proxy-settings page of the project

import os
# from database.database import Database
import datetime
import json

# This file contains the database handlers


class Database:

    def __init__(self, db): #'database.json'):
        self.db = db
        data = {}
        data['proxy_admins'] = [{'email': "admin", 'passw': "admin"}] # {'email: email, 'passw': passw}
        data['sites_blocked'] = [{'url': 'http://www.google.com'}]
        data['private_mode_auth'] = [] # {'email: email, 'passw': passw}
        data['managers_credentials'] = [{'email': "admin", 'passw': "admin"}] # {'email: email, 'passw': passw}
        data['history'] = [] # {'url': '', 'accessed': '', 'last_modified': ''}
        data['cache'] = [] # 'url': {last_modified': "date", 'html': "<html>"}

        if not os.path.isfile(db) or os.stat(db).st_size == 0:
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







class ProxyManager:
    DEBUG = False
    """
    Manages all the elements from cache and proxy-settings page
    """

    def __init__(self, db_file_path = 'database.json'):
        self.init_settings(db_file_path)

    def init_settings(self, path_to_db):
        self.db = Database(path_to_db)

    def add_admin(self, email, passw):
        self.db.write_to_db('proxy_admins', {'email': str(email), 'passw': str(passw)})

    def list_of_admins(self):
        return self.db.read_from_db('proxy_admins')

    def list_of_cached_sites(self):
        l = []
        for cache in self.db.read_from_db('cache'):
            l.append(cache['url'])
        return l

    def list_of_blocked_sites(self):
        l = []
        for site in self.db.read_from_db('sites_blocked'):
            l.append(site)
        return l

    def list_of_managers(self):
        l = []
        for manager in self.db.read_from_db('managers_credentials'):
            l.append(manager)
        return l

    def list_of_private_mode_users(self):
        l = []
        for user in self.db.read_from_db('private_mode_auth'):
            l.append(user)
        return l

    def list_of_manager_sites(self):
        # [issue], Confused on the permission levels....
        # adding sample data to show usage
        return ['www.manager.com', 'www.adminPortal.com']

    def is_admin(self, email, passw):
        for d in self.db.read_from_db('proxy_admins'):
            if d['email'] == email and d['passw'] == passw:
                return True  # Return True when is_admin
        return False

    def add_site_blocked(self, url):
        self.db.write_to_db('sites_blocked', url)

    def get_blocked_site(self, url):
        # is_private_mode = request['is_private_mode']
        
        for site in self.db.read_from_db('cache'):
            if site['url'] == url:
                return site['html']

        return "<html><body><h1>blocked site was not in the cache</h1></body></html>"

    def is_site_blocked(self, url):
        # is_private_mode = request['is_private_mode']
        for d in self.db.read_from_db('sites_blocked'):
            if d['url'] == url:
                return True
        return False

    def add_manager(self, email, password):
        #self.managers_credentials.append()
        self.db.write_to_db('managers_credentials', {'email': email, 'passw': password})

    def is_manager(self, email, password):
        for d in self.db.read_from_db('managers_credentials'):
            if d['email'] == email and d['passw'] == password:
                return True
        return False

    def is_cached(self, url):
        # url = request['url']
        # is_private_mode = request['is_private_mode']
        for cached_dict in self.db.read_from_db('cache'):
            if cached_dict['url'] == url:
                return True
        return False


    def add_cached_resource(self, url, last_modified, html):
        self.db.write_to_db('cache', {'url': str(url), 'last_modified': str(last_modified), 'html': str(html)})

    def get_cached_resource(self, url):
        # url = request['url']
        # is_private_mode = request['is_private_mode']
        for cached in self.db.read_from_db('cache'):
            if cached['url'] == url:
                try:
                    # update accessed timestamp
                    for history in self.db.read_from_db('history'):
                        if history['url'] == url:
                            self.db.write_to_db('history', {'url': url, 'accessed': str(datetime.datetime.now()), 'modified': history['modified']})
                    return cached #['html']
                except KeyError as e:
                    print("cached resource: " + url + " was requested but was not in the cache")

    def clear_cache(self):
        self.db.clear_cache()

    def clear_history(self):
        self.db.clear_history()

    def clear_all(self):
        self.db.clear_db()

DEBUG = False

if DEBUG:
    print("DEBUG Mode")
    pm = ProxyManager()
    pm.add_admin("sample@yahoo.com", "password")
    pm.add_manager("derp@yahoo.com", "password")
    pm.add_site_blocked({'url': "www.google.com"})
    # pm.clear_all()




