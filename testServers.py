import time
import masscan
from mcstatus import JavaServer
from pymongo import MongoClient
from multiprocessing import Pool


def connectMongo():
    CONNECTION_STRING = "mongodb://root:example@127.0.0.1:27017"
    client = MongoClient(CONNECTION_STRING)
    return client['minecraft']

def pingMinecraftServer(ip):
    retry = 1
    while retry <= 3:
        try:
            server = JavaServer.lookup(ip)
            status = server.status()
            players = []        
            if status.players.sample:
                players = [{'id': player.id, 'name': player.name} for player in status.players.sample]

            servers_collection.update_one ({'ip': ip }, { "$set": {'ip': ip, 'version': status.version.name,'motd': status.description, 'raw_status': status.raw}, "$push": { "players": {'$each': players} } },upsert = True)
            print(f"{ip} is a minecraft server")
            break
        except Exception as e:
            if str(e) == 'Server did not respond with any information!':
                break
            retry += 1
    if retry == 3:
        print(f"{ip} is NOT a minecraft server")


database = connectMongo()
possible_servers_collection = database['possible_servers']
servers_collection = database['servers']

if __name__ == "__main__":
    
    while True:
        possible_servers = possible_servers_collection.find(limit=100)
        ips = [server['ip'] for server in possible_servers]
        if len(ips) > 0:
            print("---------------------------------")
            print(f"Got possible server list. len: {len(ips)}")

            with Pool(len(ips)) as p:
                p.map(pingMinecraftServer, ips)

            print("---------------------------------")
            print("Removing scanned servers")
            possible_servers_collection.delete_many({'ip': {'$in': ips}})

        else:
            print("No ips to scan, waiting 10")
            time.sleep(10)

   