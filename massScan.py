import random
import masscan
import threading
from mcstatus import JavaServer
from pymongo import MongoClient


def connectMongo():
    CONNECTION_STRING = "mongodb://root:example@127.0.0.1:27017"
    client = MongoClient(CONNECTION_STRING)
    return client['minecraft']

def massScan(database):

    collection = database["possible_servers"]

    print("Starting scan")

    # #ip ranges
    # A = list(range(1, 255))
    # B = list(range(1, 255))
    # random.shuffle(A)
    # random.shuffle(B)

    # ip_ranges = []

    # for a in A:
    #     for b in B:
    #         ip_range = f"{a}.{b}.0.0/16"
    #         ip_ranges.append(ip_range)

    ip_ranges = [
        '116.202.0.0/16',
        '116.203.0.0/16',
        '128.140.0.0/17',
        '135.181.0.0/16',
        '136.243.0.0/16',
        '138.201.0.0/16',
        '142.132.128.0/17',
        '144.76.0.0/16',
        '148.251.0.0/16',
        '157.90.0.0/16'
    ]

    while True:
        random.shuffle(ip_ranges)

        for ip_range in ip_ranges:
            try:
                mas = masscan.PortScanner()
                print(f"Scanning {ip_range}")
                mas.scan(ip_range, ports='25565', arguments='--max-rate 200000')
                ips = list(mas._scan_result['scan'].keys())
                if ips:    
                    print(ips)
                    for ip in ips:
                        collection.update_one({'ip': ip},{ "$set": { 'ip': ip }}, upsert=True)


            except Exception as e:
                print(f"Scan exception: {e}")

        print("Finished scan, go again")
        


if __name__ == "__main__":

    database = connectMongo()
    massScan(database)