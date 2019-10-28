# This file contains the ProxyManager class which handle all the operations
# done in the proxy-settings page of the project

import os
from database.database import Database
import datetime

class ProxyManager:
    DEBUG = True
    """
    Manages all the elements from cache and proxy-settings page
    """

    def __init__(self):
        self.init_settings()

    def init_settings(self):
        self.db = Database()

    def add_admin(self, email, passw):
        self.db.write_to_db('proxy_admins', {'email': str(email), 'passw': str(passw)})

    def list_of_admins(self):
        return self.db.read_from_db('proxy_admins')

    def is_admin(self, email, passw):
        for d in self.db.read_from_db('proxy_admins'):
            if d['email'] == email and d['passw'] == passw:
                return True  # Return True when is_admin
        return False

    def add_site_blocked(self, request):
        #[issue], might need to parse an http request for the url
        self.db.write_to_db('sites_blocked', request['url'])

    def get_blocked_site(self, request):
        url = request['url']
        is_private_mode = request['is_private_mode']
        
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
                    return cached['html']
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




