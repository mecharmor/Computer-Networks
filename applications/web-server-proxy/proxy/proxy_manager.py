# This file contains the ProxyManager class which handle all the operations
# done in the proxy-settings page of the project

import os
import datetime
import json

class Database:
    # inside are database handlers for proxy manager to interact with json database safely
    def __init__(self, db):
        self.db = db
        data = {}
        data['proxy_admins'] = [{'email': "admin", 'passw': "admin"}] # {'email: email, 'passw': passw}
        data['sites_blocked'] = ['http://www.google.com']
        data['private_mode_auth'] = [] # {'email: email, 'passw': passw}
        data['managers_credentials'] = [{'email': "manager", 'passw': "manager"}] # {'email: email, 'passw': passw}
        data['managers_sites'] = ['http://www.dolekemp96.org/main.htm']
        data['history'] = [] # {'url': '', 'accessed': '', 'last_modified': ''}
        data['cache'] = [] # 'url': {last_modified': "date", 'html': "<html>"}

        if not os.path.isfile(db) or os.stat(db).st_size == 0: # needed so database is not wiped on each server restart
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
        data['managers_sites'] = []

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
        data['managers_sites'] = self.read_from_db('managers_sites')
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
        data['managers_sites'] = self.read_from_db('managers_sites')
        data['history'] = self.read_from_db('history')
        data['cache'] = []

        with open(self.db, 'w') as f:
            json.dump(data, f)
        f.close()

    def url_in_list(self, url, l):
        for i in range(len(l)):
            if l[i]['url'] == url:
                return i
        return -1

    def write_to_db(self, key, val):
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
                print("write_to_db failed because key: " + str(key) + " not found. error: " + str(e))
        f.close()
        with open(self.db, 'w') as w:
            json.dump(data, w)
        w.close()
        
    def read_from_db(self, key):
        data = {}
        with open(self.db) as f:
            data = json.load(f)
            try:
                return data[key]
            except KeyError as e:
                print("read_from_db failed because key: " + str(key) + " not found. error: " + str(e))

class ProxyManager:
    DEBUG = False
    """
    Manages all the elements from cache and proxy-settings page
    """
    def __init__(self ,db_file_path='database.json'):
        self.init_settings(db_file_path)

    def init_settings(self, path_to_db):
        self.db = Database(path_to_db)

    def add_admin(self, email, passw):
        self.db.write_to_db('proxy_admins', {'email': str(email), 'passw': str(passw)})

    def list_of_admins(self):
        return self.db.read_from_db('proxy_admins')

    def list_of_cached_sites(self):
        list_of_urls = []
        for cache in self.db.read_from_db('cache'):
            list_of_urls.append(cache['url'])
        return list_of_urls

    def list_of_blocked_sites(self):
        return self.list_builder('sites_blocked')

    def list_of_managers(self):
        return self.list_builder('managers_credentials')

    def list_of_private_mode_users(self):
        return self.list_builder('private_mode_auth')

    def list_of_manager_sites(self):
        return self.list_builder('managers_sites')

    def list_builder(self, key):
        list_of_values = []
        for value in self.db.read_from_db(key):
            list_of_values.append(value)
        return list_of_values

    def is_admin(self, email, passw):
        for d in self.db.read_from_db('proxy_admins'):
            if d['email'] == email and d['passw'] == passw:
                return True  # Return True when is_admin
        return False

    def add_site_blocked(self, url):
        self.db.write_to_db('sites_blocked', url)

    def add_new_manager_site(self, url):
        self.db.write_to_db('managers_sites', url)

    def get_blocked_site(self, url):
        for site in self.db.read_from_db('cache'):
            if site['url'] == url:
                return site['html']

        return "<html><body><h1>blocked site was not in the cache</h1></body></html>"

    def is_site_blocked(self, url):
        for site in self.db.read_from_db('sites_blocked'):
            if site == url:
                return True
        return False

    def is_site_blocked_except_managers(self, url):
        for site_url in self.db.read_from_db('managers_sites'):
            if site_url == url:
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
        date_time = str(datetime.datetime.now())
        self.db.write_to_db('history', {'url': url, 'accessed': date_time, 'modified': date_time})
        self.db.write_to_db('cache', {'url': str(url), 'last_modified': str(last_modified), 'html': str(html)})

    def get_cached_resource(self, url):
        for cached in self.db.read_from_db('cache'):
            if cached['url'] == url:
                try:
                    # update accessed timestamp
                    for history in self.db.read_from_db('history'):
                        if history['url'] == url:
                            self.db.write_to_db('history', {'url': url, 'accessed': str(datetime.datetime.now()), 'modified': history['modified']})
                    return cached
                except KeyError as e:
                    print("cached resource: " + url + " was requested but was not in the cache")

    def clear_cache(self):
        self.db.clear_cache()

    def clear_history(self):
        self.db.clear_history()

    def clear_all(self):
        self.db.clear_db()