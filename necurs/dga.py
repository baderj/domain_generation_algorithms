import argparse
from datetime import datetime

def generate_necurs_domain(sequence_nr, magic_nr, date):
    def pseudo_random(value):
        loops = (value & 0x7F) + 21
        for index in range(loops):
            value += ((value*7) ^ (value << 15)) + 8*index - (value >> 5)
            value &= ((1 << 64) - 1)

        return value

    def mod64(nr1, nr2):
        return nr1 % nr2

    n = pseudo_random(date.year)
    n = pseudo_random(n + date.month + 43690)
    n = pseudo_random(n + (date.day>>2))
    n = pseudo_random(n + sequence_nr)
    n = pseudo_random(n + magic_nr)
    domain_length = mod64(n, 15) + 7

    domain = ""
    for i in range(domain_length):
        n = pseudo_random(n+i) 
        ch = mod64(n, 25) + ord('a') 
        domain += chr(ch)
        n += 0xABBEDF
        n = pseudo_random(n) 

    tlds = ['tj','in','jp','tw','ac','cm','la','mn','so','sh','sc','nu','nf','mu',
    'ms','mx','ki','im','cx','cc','tv','bz','me','eu','de','ru','co','su','pw',
    'kz','sx','us','ug','ir','to','ga','com','net','org','biz','xxx','pro','bit']

    tld = tlds[mod64(n, 43)]
    domain += '.' + tld
    return domain

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="as YYYY-mm-dd")
    args = parser.parse_args()
    date_str = args.date
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        date = datetime.now() 

    for sequence_nr in range(2048):
        print(generate_necurs_domain(sequence_nr, 9, date))
