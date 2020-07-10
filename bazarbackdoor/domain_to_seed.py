import argparse


def revert(domain):
    sld, tld = domain.split(".")
    if len(sld) != 12:
        raise ValueError("second level domain needs to be 12 chars")

    ds = ""
    valid_chars = [
      "abcde",
      "cdef",
      "efgh",
      "ghi",
      "ijk",
      "klm"
    ]
    invalid = "not a bazarloader domain"
    for i, s in enumerate(sld[:6]):
        if sld[i] not in valid_chars[i]:
            raise ValueError(invalid)
        d = ord(sld[i+6]) - ord(s)
        ds += chr(d + ord('0'))

    try:
        _ = int(ds)
    except ValueError:
        raise ValueError("is not a bazaar loader domain") 


    month = 12 - int(ds[:2])
    year = int(ds[2:]) + 18 

    if not 1 <= month <= 12 or not 1900 <= year <= 2100:
        raise ValueError(invalid + "range")
    
    return "month: {}, year: {}".format(month, year) 

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("domain")
    args = parser.parse_args()
    try: 
        print(revert(args.domain))
    except ValueError as e:
        print(e)
