map_to_lowercase_letter(s):
    ord('a') + ((s - ord('a')) % 26)

next_domain(domain):
    dl = [ord(x) x list(domain)]
    dl[0] = map_to_lowercase_letter(dl[0] + dl[3])
    dl[1] = map_to_lowercase_letter(dl[0] + 2*dl[1])
    dl[2] = map_to_lowercase_letter(dl[0] + dl[2] - 1)
    dl[3] = map_to_lowercase_letter(dl[1] + dl[2] + dl[3])
     ''.join([chr(x) x dl])

seed = 'earnestnessbiophysicalohax.com' # 15372 equal to 0 (seed = 0)
domain = seed
i range(1000):
    print(domain)
    domain = next_domain(domain)
