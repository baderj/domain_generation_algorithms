"""
    generate domains according to: 
    - https://www.endgame.com/blog/malware-with-a-personal-touch.html
    - http://www.rsaconference.com/writable/presentations/file_upload/br-r01-end-to-end-analysis-of-a-domain-generating-algorithm-malware-family.pdf 

    requires words1.txt, words2.txt and words3.txt

    Thanks to Sándor Nemes who provided the third wordlist. It is taken
    from this sample:
    https://www.virustotal.com/en/file/4ee8484b95d924fe032feb8f26a44796f37fb45eca3593ab533a06785c6da8f8/analysis/
"""
import time
from datetime import datetime
import argparse

def generate_domains(time_, word_list):
    with open("words{}.txt".format(word_list), "r") as r:
        words = [w.strip() for w in r.readlines()]

    if not time_:
        time_ = time.time()
    seed = int(time_) >> 9
    for c in range(85):
        nr = seed
        res = 16*[0]
        shuffle = [3, 9, 13, 6, 2, 4, 11, 7, 14, 1, 10, 5, 8, 12, 0]
        for i in range(15):
            res[shuffle[i]] = nr % 2
            nr = nr >> 1

        first_word_index = 0
        for i in range(7):
            first_word_index <<= 1
            first_word_index ^= res[i]

        second_word_index = 0
        for i in range(7,15):
            second_word_index <<= 1
            second_word_index ^= res[i]
        second_word_index += 0x80

        first_word = words[first_word_index]
        second_word = words[second_word_index]
        tld = ".net"
        print("{}{}{}".format(first_word, second_word, tld))
        seed += 1

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    datefmt = "%Y-%m-%d %H:%M:%S"
    parser.add_argument('set', choices=[1,2,3], type=int, help="word list")
    parser.add_argument('-t', '--time', 
            help="time (default is now: %(default)s)",
            default=datetime.now().strftime(datefmt))
    args = parser.parse_args()
    time_ = time.mktime(datetime.strptime(args.time, datefmt).timetuple())
    generate_domains(time_, args.set)
