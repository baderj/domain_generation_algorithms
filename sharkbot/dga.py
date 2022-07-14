import argparse
import base64
import hashlib
from datetime import datetime


def dga(date: datetime, version: str):

    # this will actually be locale dependent, so be prepared for + or -
    # on week shifts
    week_of_year = date.isocalendar()[1]
    year = date.year
    if version in {"0.0", "1.63"}:
        tlds = [".top", ".xyz", ".cc", ".info", ".com", ".ru", ".net"]
    else:
        tlds = [".xyz", ".live", ".com", ".store", ".info", ".top", ".net"]

    for tld in tlds:
        if version == "2.8":
            s = f"{tld}{week_of_year}{year}"
            h = hashlib.md5(s.encode("ascii")).hexdigest()
            sld = h[:16]
        elif version == "2.1":
            s = f"{tld}{week_of_year}"
            h = hashlib.md5(s.encode("ascii")).hexdigest()
            t = f"{h}{year}"
            sld = t[:16]
        elif version == "1.63":
            s = f"{week_of_year + year}pojBI9LHGFdfgegjjsJ99hvVGHVOjhksdf"
            b = base64.b64encode(s.encode('ascii'))
            sld = b[:19].decode('ascii').lower()
        elif version == "0.0":
            s = f"{week_of_year}pojBI9LHGFdfgegjjsJ99hvVGHVOjhksdf"
            b = base64.b64encode(s.encode('ascii'))
            sld = b[:19].decode('ascii').lower()
        else:
            raise ValueError(f"invalid version {version}")
        yield f"{sld}{tld}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DGA of MyDoom")
    parser.add_argument(
        "-d", "--date", help="date for which to generate domains, e.g., 2022-05-09"
    )
    parser.add_argument(
        "-v", "--version", help="version of the dga", choices=["0.0", "1.63", "2.8", "2.1"], default="2.8"
    )
    args = parser.parse_args()
    if args.date:
        date = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        date = datetime.now()

    for domain in dga(date=date, version=args.version):
        print(domain)
