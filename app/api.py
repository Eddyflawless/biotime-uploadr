import sys
import requests

class Api:

    def __init__(self,base_url=None):
        self.base_url = base_url

    def get(self,endpoint,parameters={}, headers={}):
        url = self.construct_uri(endpoint)
        r = requests.get(url=url,params=parameters)
        
    def post(self,endpoint,data,headers={}):

        url = self.construct_uri(endpoint)
        r = requests.post(url=url,data=data,headers=headers)
        return r

    def construct_uri(self, endpoint):
        url = ""
        if self.base_url is None:
            url = endpoint
        else:
            url = self.base_url + "/" +endpoint      

        return url    


        