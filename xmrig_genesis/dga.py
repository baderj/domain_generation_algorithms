import argparse
import hashlib
import itertools
import json
import os
import time
from datetime import date, datetime
from typing import Iterator, Union

import requests

LIMIT = 100
DB_PATH = "db.json"
BLOCK = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
PATTERN = '{"1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa":{"final_balance":FB,"n_tx":NTX,"total_received":FB}}'


def refresh_blockchain_db():
    offset = 0
    if os.path.exists(DB_PATH):
        with open(DB_PATH) as r:
            db = json.load(r)
    else:
        db = {}

    while True:
        url = f"https://blockchain.info/multiaddr?active={BLOCK}&limit={LIMIT}&offset={offset}"
        r = requests.get(url)

        data = r.json()
        error = data.get('error')
        if error:
            print(f"error updating blockchain balance: {data}")
            quit()
        txs = data["txs"]
        for tx in txs:
            h = tx['hash']
            if h in db:
                break
            db[h] = tx
        else:
            time.sleep(1)
            offset += LIMIT
            continue
        break
    with open(DB_PATH, "w") as w:
        json.dump(db, w, indent=2)


def get_blockchain_seed(when, updated: bool = False) -> str:

    if when > datetime.now():
        raise ValueError(
            "you can't generate the blockchain domains for the future!")

    with open(DB_PATH) as r:
        transactions = json.load(r)

    transactions = sorted(
        transactions.values(),
        key=lambda x: x['time'],
        reverse=True
    )
    ntx = len(transactions) + 1
    for i, transaction in enumerate(transactions):
        tt = transaction["time"]
        time = datetime.fromtimestamp(tt)

        if when < time:
            continue

        if i == 0 and not updated:
            """ if the desired date is later than the latest transaction,
                then update the transaction database to make sure it is
                the current transaction you like to access """
            refresh_blockchain_db()
            return get_blockchain_seed(when, updated=True)
        balance = transaction['balance']
        return PATTERN.replace("FB", str(balance)).replace("NTX", str(ntx-1))
    raise ValueError("the provided date is before the first transaction")


def dga(when: Union[date, datetime], blockchain: bool = False) -> Iterator[str]:
    for i in range(2):
        if i and not blockchain:
            return

        if i == 0:
            magic = when.strftime("%Y-%m-%d")
            seed = f"{magic}ojena.duckdns.org"
        else:
            magic = get_blockchain_seed(when)
            seed = f"{magic}"

        md5 = hashlib.md5(seed.encode("ascii")).hexdigest()
        slds = [md5[i:i+8] for i in range(0, len(md5), 8)]
        tlds = [".com", ".net", ".org", ".duckdns.org"]

        for sld, tld in itertools.product(slds, tlds):
            yield f"{sld}{tld}"


def date_parser(s):
    return datetime.strptime(s, "%Y-%m-%d")


if __name__ == "__main__":
    now = datetime.now().strftime("%Y-%m-%d")
    parser = argparse.ArgumentParser(
        description="XMRig malware with DGA based on Bitcoin Genesis Block"
    )
    parser.add_argument(
        "-d", "--date",
        help="date for which to generate domains, e.g., 2022-05-09",
        default=now,
        type=date_parser
    )
    parser.add_argument(
        "-b", "--blockchain",
        help="also generate blockchain domains, requires blockchain db",
        action='store_true'
    )
    args = parser.parse_args()

    for domain in dga(args.date, args.blockchain):
        print(domain)
