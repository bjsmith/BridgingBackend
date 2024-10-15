from socket import gethostname
import yaml
from yaml.loader import SafeLoader
import os
import json

class Config:

    config = None

    def get_config(force_reload=False):

        if force_reload or Config.config is None:
            is_prod = os.environ.get('IS_HEROKU', None)=='True'
            if is_prod==True:
                print("loading config from heroku")
                #get all keys in the environment with os.environ
                all_environ = dict(os.environ)
                #now get the keys
                #coachcontext_environ = {k.replace("COACHCONTEXT_",""):v for k,v in all_environ.items() if k.startswith("COACHCONTEXT_")}
                
                #attempt to convert each value to json, if it fails, just use the string
                for k,v in all_environ.items():
                    try:
                        all_environ[k] = json.loads(v)
                    except ValueError:
                        pass
                
                Config.config = all_environ
                return Config.config


            with open('resources/config.yml') as f:
                    all_yaml = yaml.load(f, Loader=SafeLoader)
                    if gethostname() in all_yaml.keys():
                        Config.config = all_yaml[gethostname()]
                    else:
                        Config.config = all_yaml['default']
        
        return Config.config