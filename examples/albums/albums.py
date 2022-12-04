import requests
from mastodon import Mastodon
import json
from time import sleep
import logging
import urllib.parse
import time
import random
import os
import modules.worker as worker
logging.basicConfig(level=logging.DEBUG)


def album():
    text = worker.getPrompts(model="gpt2-large",text="Music album title", min_length=10, max_length=50, no_repeat_ngram_size=1)
    print(text)
    '''
    theme = generate("gpt2-large","Title : How to cook a ", min_length=10, max_length=15, no_repeat_ngram_size=1)

    print(theme)

    recipe = generate("gpt2-large","to cook a " + theme + "\n 1.", min_length=60, max_length=100, no_repeat_ngram_size=1, top_p=0.5)

    print(recipe)'''
    
