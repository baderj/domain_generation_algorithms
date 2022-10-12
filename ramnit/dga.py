#!/usr/bin/env /usr/local/bin/python3
"""
dga_ramnit
----------

Generate DNS queries using the ramnit DGA

See `The DGA of ramnit
<https://bin.re/blog/the-dga-of-ramnit/>`__ for a detailed explanation of the
algorithm.

The code below is almost fully based on `<https://github.com/baderj/domain_generation_algorithms/blob/master/ramnit/dga.py>`__ by `Johannes Bader
<https://github.com/baderj>`__.
"""
from secrets import token_hex, choice
import argparse
import sys

TLDS = ['click', 'com', 'eu', 'bid']
KNOWN_SEEDS = [
    '16647BB4', 'E7392D18', 'C129388E', 'E706B455', 'DC485593', 'EF214BBF',
    '28488EEA', '4BFCBC6A', '79159C10', '92F4BE35', '4302C04A', '52278648',
    '9753029A', 'A6EAB21A', '46CF1B28', '1CCEC41C', '0C5787AE2', '0FCFFD9E9',
    '75EA95C2', '8A0AEC7D', '1DF640A8', '14DF29DD', '8222270B', '55536A85',
    '5C39E467', 'D2B3C361', 'F318D47D', '231D9480', '13317EAC', '89547381',
    '6C36D41D'
]
SLD_MIN_LENGTH = 9
SLD_MAX_LENGTH = 25
NUMBER_DOMAINS = 10


class RandInt:
    """
    Generate random integers using a `Linear congruential generator
    <https://en.wikipedia.org/wiki/Linear_congruential_generator>`__
    """

    def __init__(self, seed=None):
        """
        :arg str seed:
            the seed for the LCG pseudo-random numbers generator
            if a seed is not provided, a random 8-hex digits seed is generated using the :meth:`secrets.token_hex` method
        """
        if seed is None:
            seed = int(token_hex(8), 16)
        self.value = seed

    def rand_int_modulus(self, modulus):
        """
        generate a random integer using a classic LGC generator, update the seed, and return the result of the modulo operation between the random integer and the `modulus` argument

        for example, if the `modulus` value is `12`, the return is a random
        integer from `0` to `11` (the possible results of a modulo `12` operation). the randomization is provided by the random integer
        subjected to the modulo operation.
        """
        lcg_random_int = 16807*(self.value % 127773) \
            - 2836*(self.value // 127773) & 0xFFFFFFFF
        self.value = lcg_random_int

        return lcg_random_int % modulus


def get_domains(
        seed=None, number_domains=NUMBER_DOMAINS, tlds=None,
        sld_min_length=SLD_MIN_LENGTH, sld_max_length=SLD_MAX_LENGTH):
    """
    generate a list of Ramnit domains

    :arg str seed:

    :arg int number_domains:

    :arg lst tlds:

    :arg int sld_min_length:

    :arg int sld_maxx_length:

    """
    if tlds is None:
        tlds = TLDS

    if not isinstance(tlds, (list, tuple)):
        tlds = [tlds]

    # validate the seed value if provide by the user; it must be a HEX digit
    if seed:
        try:
            seed = int(seed, 16)
        except ValueError as error:
            raise ValueError(
                f'invalid seed value:{seed} is not a HEX number'
            ) from error

    # clean up the TLDs if provided by the user; we don't want any [.] dots
    tlds = [tld.replace('.', '') for tld in tlds]

    random_int = RandInt(seed)

    for idx in range(number_domains):
        first_seed = random_int.value

        """
        the LCG generator returns a value between 0 and `modulus` - `1`. assuming it returns 0, the minimum length of the SLD is given by
        the value after the `+` sign in the code line below.
        the maximum length of the domain is determined by the largest value
        returned by the modulo operation in the LCG code. using the defaults from this code:
        - 9 characters are provided by the second term of the sum below
        - the rest of the characters up to the maximum length of 25 must come
          the random component. result of the modulus operation must pad the
          domain name with another 25 - 9 = 16 characters. the modulus operand
          that returns from 0 to 16 is 1 + (25 -9) = 17
        """
        domain_len = random_int.rand_int_modulus(
            1 + (sld_max_length - sld_min_length)
        ) + sld_min_length

        second_seed = random_int.value

        domain = ''.join(
            [
                chr(ord('a') + random_int.rand_int_modulus(25))
                for _ in range(domain_len)
            ]
        )

        domain = f'{domain}.{tlds[idx % len(tlds)]}'

        # we need to reseed the LCG for the next domain in the sequence
        reseed = first_seed * second_seed
        random_int.value = (reseed + reseed//(2**32)) % 2**32

        yield domain


def parse_args():
    """
    parse the command line
    """
    parser = argparse.ArgumentParser(description="generate Ramnit domains")

    choose_seed = parser.add_mutually_exclusive_group(required=True)
    choose_seed.add_argument(
        '-s', '--seed', dest='seed', action='store',
        help='seed as hex; a value is mandatory')
    choose_seed.add_argument(
        '-r', '--generate-random-seed', dest='random_seed', action='store_true',
        help='generate a random seed'
    )
    choose_seed.add_argument(
        '-k', '--random-known-seed', dest='known_seed', action='store_true',
        help='choose a random seed from the list of known seeds'
    )

    parser.add_argument(
        '-x', '-number-domains', dest='number_domains', type=int,
        default=NUMBER_DOMAINS,
        help='number of domains, default: %(default)s domains')
    parser.add_argument(
        '-t', '--tlds', dest='tlds', action='store', default=','.join(TLDS),
        help=(
            'list of tlds, comma or space separated string,'
            ' default: %(default)s')
    )
    parser.add_argument(
        '-m', '--min-length', dest='min_length', type=int,
        default=SLD_MIN_LENGTH,
        help='minimum length of the SLD, default: %(default)s'
    )
    parser.add_argument(
        '-M', '--max-length', dest='max_length', type=int,
        default=SLD_MAX_LENGTH,
        help='maximum length of the SLD, default: %(default)s'
    )

    return parser


def main():
    """main"""
    args = parse_args().parse_args()

    if args.random_seed:
        seed = None
    elif args.known_seed:
        seed = choice(KNOWN_SEEDS)
    else:
        seed = args.seed

    tlds = args.tlds.replace(' ', ',').split(',')

    print(*[
        domain for domain in get_domains(
            seed=seed, number_domains=args.number_domains, tlds=tlds,
            sld_min_length=args.min_length, sld_max_length=args.max_length
        )
    ], sep='\n', end='\n')


if __name__ == "__main__":

    try:
        main()
    except Exception as err:    # pylint disable=broad-except
        print(err)
        sys.exit(2)
    sys.exit(0)
