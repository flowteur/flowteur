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


def invoke():

    text = worker.getPrompts(model="gpt2-large",text="yassinbooth instagram description:", min_length=5, max_length=50, no_repeat_ngram_size=1)
    
    image = worker.getImage(text["result"],1)
    
    # save the byres to a file
   # save image to file with mimetype png
    with open("image.png", "wb") as f:
        f.write(image)
    
    # post to mastodon
    worker.postImage("image.png", text)
    
