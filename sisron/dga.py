from datetime import datetime, timedelta
import base64 
import argparse 

def dga(d, day_index, tld_index):
    tlds = [x.encode('ascii') for x in [".com", ".org", ".net", ".info"]]
    d -= timedelta(days=day_index)
    ds = d.strftime("%d%m%Y").encode('latin1')
    domain = base64.b64encode(ds).lower().replace(b"=",b"a") + tlds[tld_index]
    return domain.decode('latin1')

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date for which to generate domains")
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    for i in range(40):
        print(dga(d, i%10, i//10))

