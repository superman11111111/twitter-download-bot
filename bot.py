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
      mention = mention._json
      try:
        status_id = mention['in_reply_to_status_id']
        print(status_id)
        status = self.api.get_status(status_id)._json
        reply = [f"@{mention['user']['screen_name']}"]
        for media in status['extended_entities']['media']:
          variants = media['video_info']['variants']
          reply.append(variants[-1]['url'])
        print(reply)
        try:
          # self.api.create_favorite(mention['id'])
          self.api.update_status(
              status="\n".join(reply), in_reply_to_status_id=mention['id'], auto_populate_reply_metadata=True)
        except Exception as e:
          print(e)
      except Exception as e:
        print(e)
        try:
          # self.api.create_favorite(mention['id'])
          self.api.update_status(
              status=reply + " NO VIDEO FOUND", in_reply_to_status_id=mention['id'], auto_populate_reply_metadata=True)
        except Exception as e:
          print(e)


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
