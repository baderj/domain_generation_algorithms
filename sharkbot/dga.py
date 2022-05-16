import argparse
import hashlib
from datetime import datetime


def dga(date: datetime):
    tlds = [".xyz", ".live", ".com", ".store", ".info", ".top", ".net"]

    # this will actually be locale dependent, so be prepared for + or -
    # on week shifts
    week_of_year = date.isocalendar()[1]
    year = date.year
    for tld in tlds:
        s = f"{tld}{week_of_year}{year}"
        h = hashlib.md5(s.encode("ascii")).hexdigest()
        yield f"{h[:16]}{tld}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DGA of MyDoom")
    parser.add_argument(
        "-d", "--date", help="date for which to generate domains, e.g., 2022-05-09"
    )
    args = parser.parse_args()
    if args.date:
        date = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        date = datetime.now()

    for domain in dga(date=date):
        print(domain)
