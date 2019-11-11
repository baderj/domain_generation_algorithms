import time
import hashlib
import base64
import argparse
from datetime import datetime


TLDS =['cf', 'tk', 'ml', 'ga', 'gq', 'com', 'biz', 'org', 'de', 'rocks', 'mx', 'cn', 'top', 'nl', 'men', 'ws', 'se', 'info', 'xyz', 'net', 'today', 'ru', 'fi', 'name', 'to', 'in', 'com.ua', 'vg', 'vn', 'cd']
SEED = "IbjGOEgnuD"


def dga(date):
    def unix(date):
        unix = int(time.mktime(date.timetuple()))
        return unix

    HOUR = 3600
    DAY = 24*HOUR
    INTERVAL = 15*DAY
    for tld in TLDS:
        key = f"{unix(date)//INTERVAL}{SEED}{tld}\n".encode('ascii')
        key_hash = hashlib.sha1(key).digest()
        key_hash_b64 = base64.b64encode(key_hash).decode('ascii')
        key_hash_b64_noeq_lc = key_hash_b64.rstrip("=").lower()
        trantab = str.maketrans("-+/", "abc")
        hostname_src = key_hash_b64_noeq_lc.translate(trantab)
        for hostname_len in range(6, 11):
            hostname = hostname_src[:hostname_len]
            domain = f"{hostname}.{tld}"
            yield domain


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="QSnatch dga")
    parser.add_argument(
        "-d", "--datetime",
        help="date time for which to generate domains, e.g., "
             "2019-11-11 18:00:00")
    args = parser.parse_args()
    if args.datetime:
        d = datetime.strptime(args.datetime, "%Y-%m-%d %H:%M:%S")
    else:
        d = datetime.now()
    for domain in dga(d):
        print(domain)
