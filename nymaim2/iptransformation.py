import argparse


def iptoval(ip):
    els = [int(_) for _ in ip.split(".")]
    v = 0
    for el in els[::-1]:
        v <<= 8
        v += el
    return v


def valtoip(v):
    els = []
    for i in range(4):
        els.append(str(v & 0xFF))
        v >>= 8
    return ".".join(els)


def step(ip, reverse=False):
    v = iptoval(ip)
    if reverse:
        v ^= 0x18482642
        v = (v + 0x78643587) & 0xFFFFFFFF
        v ^= 0x87568289
    else:
        v ^= 0x87568289
        v = (v - 0x78643587) & 0xFFFFFFFF
        v ^= 0x18482642
    return valtoip(v)


def transform(ip, iterations=16, reverse=False):
    for _ in range(iterations):
        ip = step(ip, reverse=reverse)
    return ip


def checksum(pairs, index):
    checksum = 0
    for i, p in enumerate(pairs):
        if i == index:
            continue
        checksum += iptoval(p[1])
    return checksum & 0xFFFFFFFF


def findip(pairs):
    for i, p in enumerate(pairs):
        c = checksum(pairs, i)
        if c == iptoval(p[1]):
            return p[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", nargs="+")
    parser.add_argument("-r", "--reverse", help="reverse transformation",
                        action="store_true")
    parser.add_argument("-c", "--checksum", help="test checksum",
                        action="store_true")
    args = parser.parse_args()

    pairs = []
    for ip_src in args.ip:
        ip_dst = transform(ip_src, reverse=args.reverse)
        pair = (ip_src, ip_dst)
        d = "-->"
        if args.reverse:
            pair = pair[::-1]
            d = "<--"
        pairs.append(pair)
        if not args.checksum:
            print("{} {} {}".format(ip_src, d, ip_dst))

    fmt = "| {:4} | {:15} | {:15} | {:10} |"
    fmt2 = "| {:4} | {:15} | {:15} | 0x{:08X} |"
    if args.checksum:
        print(fmt.format("", "IP", "IP'", "value"))
        print(fmt.format(*4 * ["---"]))
        ok_ip = findip(pairs)

        for ip, ipp in pairs:
            if ip == ok_ip:
                continue
            print(fmt2.format("", ip, ipp, iptoval(ipp)))

        for ip, ipp in pairs:
            if ip != ok_ip:
                continue
            print(fmt2.format("x", ip, ipp, iptoval(ipp)))

        if not ok_ip:
            print("No IP matches checksum")
        else:
            print("The IP marked x matches the checksum of remaining IPs, "
                  "it is removed.")
