"""
    DGA of sample:
    md5:         e66e3879700f88182bd92c7d3a00e9e4
    sha256:      0f3af9d2d7ca113704f4411185518ab41a63e8003b7e06ff21f805f11af50ab7
    malwr:       https://malwr.com/analysis/OThiMWQ1ZTE2OThkNDU4MmI2Y2U0YzE0MjdjOWVmNDk/
    virustotal:  https://virustotal.com/en/file/0f3af9d2d7ca113704f4411185518ab41a63e8003b7e06ff21f805f11af50ab7/analysis/1471447632/
"""

from itertools import permutations

"""
    hardcoded seed in binary
    seed in sample is already sorted, but malware will sort the seed
    to get all permutations in lexicographical order
"""
seed = "ddktn"

for p in permutations(''.join(sorted(seed))):
    print("{}.github.io".format(''.join(p)))
    """ malware tries to download the file at:
        <subdomain>.github.io/c2/config.dat
    """
