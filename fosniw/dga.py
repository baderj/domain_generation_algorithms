import argparse

PATTERNS = {
    "koreasys": "appx.koreasys{}.com",
    "winsoft": "app2.winsoft{}.com"
}

def dga(prefix):
    pattern = PATTERNS.get(prefix)
    if not pattern:
        raise ValueError("unsupported pattern {}".format(prefix))

    for i in range(101):
        yield pattern.format(i) 

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", choices=["winsoft", "koreasys"], default="winsoft")
    args = parser.parse_args()
    for domain in dga(args.prefix):
        print(domain)
    
