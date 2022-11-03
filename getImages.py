import base64
import json
import time
from pymongo import MongoClient


CONNECTION_STRING = "mongodb://root:example@127.0.0.1:27017"


client = MongoClient(CONNECTION_STRING)
collection = client['minecraft']['servers']

# while True:

servers_raw = collection.find({"version" : { "$regex": "1\.19\.2" },"raw_status.favicon": { "$regex": "data:" }})
servers = [{"ip": server["ip"], "favicon": server["raw_status"]["favicon"] } for server in servers_raw]

for server in servers:
    favicon = server['favicon'].replace("data:image/png;base64,", "")
    image_data = base64.b64decode(favicon)

    with open(f"favicons/{server['ip']}.png", "wb+") as fh:
        fh.write(image_data)

# print("Updated images, sleeping for 60")
# time.sleep(60)