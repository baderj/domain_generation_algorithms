import argparse
import hashlib
from datetime import datetime
from typing import Iterator


def dga(date: datetime, seed: str) -> Iterator[str]:
    data = f"{date.strftime('%Y-%m-%d')}{seed}".encode("ascii")
    sld = hashlib.md5(data).hexdigest()
    yield f"{sld}.tk"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DGA of MyDoom")
    parser.add_argument(
        "-d", "--date", help="date for which to generate domains, e.g., 2022-05-09"
    )
    parser.add_argument("-s", "--seed", help="DGA seed", default="verble")
    args = parser.parse_args()
    if args.date:
        date = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        date = datetime.now()

    for domain in dga(date=date, seed=args.seed):
        print(domain)
