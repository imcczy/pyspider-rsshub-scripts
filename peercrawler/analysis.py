import json
import redis
import csv
import hashlib

DB_HOST = 'localhost'
DB_PORT = 6379
DB_SCHOOL_NAME = 0
DB_SCHOOL_COUNT = 1
DB_PEERS_COUNT = 2

def init_db(filepath):
    db_school_name = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_SCHOOL_NAME)
    with open(filepath,"r") as file:
        csv_data = csv.reader(file,delimiter=',', quotechar='|')
        for row in csv_data:
            if row[0] is not None:
                db_school_name.set(name=row[0],value=row[1])
                #print(row[0])


def analysis(filepath):
    db_school_name = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_SCHOOL_NAME)
    db_school_count = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_SCHOOL_COUNT)
    db_peers_count  =redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_PEERS_COUNT)
    with open(filepath, "r") as file:
        for line in file:
            json_data = json.loads(line)
            ips = json_data["result"]["ip"]
            ips_filter = list(set(ips))
            for ip in ips_filter:
                if ip_version6(ip):
                    ip = ip.upper()
                    ip_split = ip.split(":")
                    ip_pre = ":".join((ip_split[0],ip_split[1],ip_split[2].rjust(4,"0")))
                    if db_school_name.exists(ip_pre):
                        db_school_count.incr(name=ip_pre,amount=1)
                        db_peers_count.incr(name=ip,amount=1)


def ip_version6(ip):
    if ip.find(":") != -1:
        return True
    else:
        return False

def dump_db():
    db_school_name = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_SCHOOL_NAME)
    db_school_count = redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_SCHOOL_COUNT)
    db_peers_count  =redis.StrictRedis(host=DB_HOST, port=DB_PORT, db=DB_PEERS_COUNT)
    dump_school =  open("/Users/imcczy/Downloads/mteam_school.csv","w")
    dump_peer = open("/Users/imcczy/Downloads/mteam_peer.csv","w")
    dump_school.write("SCHOOL,COUNT\n")
    dump_peer.write("peer,COUNT\n")
    for key in db_school_name.keys():
        school = db_school_name.get(key).decode("UTF-8")
        school_count = db_school_count.get(key)
        if school_count is not None:
            school_count = school_count.decode("UTF-8")
        else:
            school_count = "0"
        dump_school.write("%s,%s\n" %(school,school_count))
    for key in db_peers_count.keys():
        peer_count = db_peers_count.get(key)
        if peer_count is not None:
            peer_count = peer_count.decode("UTF-8")
        else:
            peer_count = "0"
        dump_peer.write("%s,%s\n" %(key.decode("UTF-8"),peer_count))
    dump_peer.close()
    dump_school.close()


if __name__ == "__main__":
    #analysis("/Users/imcczy/Downloads/mteam.json")
    dump_db()