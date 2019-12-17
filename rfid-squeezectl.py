#!/usr/bin/env python3

from urllib.request import urlopen
from urllib.error import HTTPError
from time import sleep

from pirc522 import RFID
rdr = RFID()

old_playlist_name = None
while True:
  rdr.wait_for_tag()
  (error, tag_type) = rdr.request()
  if not error:
    (error, uid) = rdr.anticoll()
    if not error:
      playlist_name = "-".join(str(i) for i in uid)
      if playlist_name == old_playlist_name:
        print("Playlist unchanged")
        sleep(2)
        continue
      old_playlist_name = playlist_name
      print(playlist_name)
      try:
        url = "http://{}/status?p0=playlist&p1=resume&p2={}&player={}".format("kueche:9000", playlist_name, "b8:27:eb:d0:cc:13")
        print(url)
        f = urlopen(url)
        print(f)
      except HTTPError as e:
        if e.code != 404:
          raise e
  sleep(2)

# Calls GPIO cleanup
rdr.cleanup()
