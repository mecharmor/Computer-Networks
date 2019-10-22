# This file contains the ProxyManager class which handle all the operations
# done in the proxy-settings page of the project

import os
import cache
from cache import *  # point of access to cache files


class ProxyManager:
    """
    Manages all the elements from cache and proxy-settings page
    """

    def __init__(self):
        self.init_settings()

    def init_settings(self):
        # Credentials for admins allowed to edit the proxy seetings page
        # append data in the form {'email: email, 'passw': passw}
        self.proxy_admins = []
        self.sites_blocked = []
        # Credentials allowed employees that can browse in private mode
        # append data in the form {'email: email, 'passw': passw}
        self.private_mode_auth = []
        # Credentials  of upper division employess
        # append data in the form {'email: email, 'passw': passw}
        self.managers_credentials = []

    def add_admin(self, email, passw):
        self.proxy_admins.append({'email': email, 'passw': passw})
        return

    def list_of_admins(self):
        return self.proxy_admins

    def is_admin(self, email, passw):
        for d in self.proxy_admins:
            if d['email'] == email and d['passw'] == passw:
                return True  # Return True when is_admin
        return False

    def add_site_blocked(self, request):
        self.sites_blocked.append(request)

    def get_blocked_site(self, request):
        return self.sites_blocked

    def is_site_blocked(self, request):
        url = request['url']

        for d in self.sites_blocked:
            if d['url'] == url:
                return True
        return False

    def add_manager(self, email, password):
        self.managers_credentials.append({'email': email, 'passw': password})

    def is_manager(self, email, password):
        for d in self.managers_credentials:
            if d['email'] == email and d['passw'] == password:
                return True
        return False

    def is_cached(self, request):
        url = request['url']
        is_private_mode = request['is_private_mode']

        path_to_cache_files = os.getcwd() + "/cache/"
        path_to_resources = path_to_cache_files + "/resources/"

        return os.path.exists(path_to_cache_files + "tests.py") #replace test.py with the queried cache file
        # htmlBody = open( + url, "r").read()


        #Information regarding how to open and read files in python are here
        """
        Optional method but really helpful. 
        Checks if a url is already in the cache 
        1. Extract url and private mode status from the request 
        2. Go to cache folder and locate if the resources
           for that url exists in the cache
        request: the request data from the client 
        :return: if the url is cached return true. Otherwise, false
        """
        return 0

    def get_cached_resource(self, request):
        
        """
        1. Extract url and private mode status from the request 
        2. Go to cache folder and locate if the resources
           for that url exists in the cache
        request: the request data from the client 
        :return: The resource requested
        """
        return 0

    def clear_cache(self):
        """
        
        :return: VOID
        """
        return 0

    def clear_history(self):
        """
        
        :return: VOID
        """
        return 0

    def clear_all(self):
        """
        1. execute clear_cache
        2. execute clear_history
        :return: VOID
        """
        return 0

#
# print("TEST OUTPUT")
# manager = ProxyManager()
# print(manager.is_cached({'url': "www.google.com", 'is_private_mode': 0}))
