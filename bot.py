import json
import tweepy
import time
from datetime import datetime
from settings import *

global IDS
IDS = []


class Bot():
  def __init__(self):
    try:
      self.keys = json.loads(open("keys.json", "r").read())
      auth = tweepy.OAuthHandler(self.keys['key'], self.keys['secret'])
      auth.set_access_token(self.keys['akey'], self.keys['asecret'])
      self.api = tweepy.API(auth)
    except Exception as e:
      print(e)

  def check_mentions(self):
    global IDS
    mentions = self.api.mentions_timeline()
    print("".join(["[", str(datetime.now().replace(microsecond=0)), "]: ", str(len(
        [x for x in mentions if x.id not in IDS])), " new mentions"]))
    for mention in mentions:
      if mention.id in IDS:
        continue
      IDS.append(mention.id)
      reply = []
      for media in mention._json['extended_entities']['media']:
        variants = media['video_info']['variants']
        for variant in variants:
          pass
          # print(variant)
        url = variants[-1]['url']
        reply.append(url)
      try:
        self.api.create_favorite(mention.id)
        self.api.update_status(
            "\n".join(reply), in_reply_to_status_id=mention.id)
      except Exception as e:
        print(e)
      # print(reply)


def server():
  b = Bot()
  while True:
    b.check_mentions()
    time.sleep(60 / TWITTER_RATE_LIMIT)


if __name__ == "__main__":
  try:
    IDS = json.loads(open("ids.json", "r").read())
  except Exception as e:
    pass
  print(IDS)
  from threading import Thread
  t = Thread(target=server)
  t.start()
  try:
    t.join()
  except KeyboardInterrupt as e:
    pass
  open("ids.json", "w").write(json.dumps(IDS))
