#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# md6hash for Python 2, 3
#
# Usage:
#     md6 = md6hash()
#     data = "md6 FTW"
#     result = md6.hex(data)
#     print(result)
#
# modified
# https://github.com/Snack-X/md6/blob/master/md6.py


import binascii


class md6hash():
    def __to_word(self, i_byte):
        length = len(i_byte)
        o_word = []

        for i in range(0, length, 8):
            o_word.append(
                ((i_byte[i + 0] & 0xff) << 56) |
                ((i_byte[i + 1] & 0xff) << 48) |
                ((i_byte[i + 2] & 0xff) << 40) |
                ((i_byte[i + 3] & 0xff) << 32) |
                ((i_byte[i + 4] & 0xff) << 24) |
                ((i_byte[i + 5] & 0xff) << 16) |
                ((i_byte[i + 6] & 0xff) << 8) |
                ((i_byte[i + 7] & 0xff) << 0)
            )

        return o_word

    def __from_word(self, i_word):
        length = len(i_word)
        o_byte = []

        for i in range(length):
            o_byte.append((i_word[i] >> 56) & 0xff)
            o_byte.append((i_word[i] >> 48) & 0xff)
            o_byte.append((i_word[i] >> 40) & 0xff)
            o_byte.append((i_word[i] >> 32) & 0xff)
            o_byte.append((i_word[i] >> 24) & 0xff)
            o_byte.append((i_word[i] >> 16) & 0xff)
            o_byte.append((i_word[i] >> 8) & 0xff)
            o_byte.append((i_word[i] >> 0) & 0xff)

        return o_byte

    def __crop(self, size, data, right):
        length = int((size + 7) / 8)
        remain = size % 8

        if right:
            data = data[len(data) - length:]
        else:
            data = data[:length]

        if remain > 0:
            data[length - 1] &= (0xff << (8 - remain)) & 0xff

        return data

    def __hash(self, size, data, key, levels):
        b = 512
        c = 128
        n = 89
        d = size
        M = data

        K = key[:64]
        k = len(K)

        while len(K) < 64:
            K.append(0x00)

        K = self.__to_word(K)

        r = max(80 if k else 0, 40 + int(d / 4))

        L = levels
        ell = 0

        S0 = 0x0123456789abcdef
        Sm = 0x7311c2812425cfa0

        Q = [
            0x7311c2812425cfa0, 0x6432286434aac8e7, 0xb60450e9ef68b7c1,
            0xe8fb23908d9f06f1, 0xdd2e76cba691e5bf, 0x0cd0d63b2c30bc41,
            0x1f8ccf6823058f8a, 0x54e5ed5b88e3775d, 0x4ad12aae0a6d6031,
            0x3e7f16bb88222e0d, 0x8af8671d3fb50c2c, 0x995ad1178bd25c31,
            0xc878c1dd04c4b633, 0x3b72066c7a1552ac, 0x0d6f3522631effcb
        ]

        t = [17, 18, 21, 31, 67, 89]
        rs = [10,  5, 13, 10, 11, 12,  2,  7, 14, 15,  7, 13, 11,  7,  6, 12]
        ls = [11, 24,  9, 16, 15,  9, 27, 15,  6,  2, 29,  8, 15,  5, 31,  9]

        def f(N):
            S = S0
            A = list(N)

            j = 0
            i = n

            while j < r:
                for s in range(16):
                    x = S
                    x ^= A[i + s - t[5]]
                    x ^= A[i + s - t[0]]
                    x ^= A[i + s - t[1]] & A[i + s - t[2]]
                    x ^= A[i + s - t[3]] & A[i + s - t[4]]
                    x ^= x >> rs[s]

                    if len(A) <= i + s:
                        while len(A) <= i + s:
                            A.append(0x00)

                    A[i + s] = x ^ ((x << ls[s]) & 0xffffffffffffffff)

                S = (((S << 1) & 0xffffffffffffffff) ^ (S >> 63)) ^ (S & Sm)

                j += 1
                i += 16

            return A[(len(A) - 16):]

        def mid(B, C, i, p, z):
            U = ((ell & 0xff) << 56) | i & 0xffffffffffffff
            V = ((r & 0xfff) << 48) | ((L & 0xff) << 40) | ((z & 0xf) << 36) | (
                (p & 0xffff) << 20) | ((k & 0xff) << 12) | (d & 0xfff)

            return f(Q + K + [U, V] + C + B)

        def par(M):
            P = 0
            B = []
            C = []
            z = 0 if len(M) > b else 1

            while len(M) < 1 or (len(M) % b) > 0:
                M.append(0x00)
                P += 8

            M = self.__to_word(M)

            while len(M) > 0:
                B.append(M[:int(b / 8)])
                M = M[int(b / 8):]

            i = 0
            p = 0
            l = len(B)

            while i < l:
                p = P if i == (len(B) - 1) else 0
                C += mid(B[i], [], i, p, z)

                i += 1
                p = 0

            return self.__from_word(C)

        def seq(M):
            P = 0
            B = []
            C = [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
                 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]

            while len(M) < 1 or (len(M) % (b - c)) > 0:
                M.append(0x00)
                P += 8

            M = self.__to_word(M)

            while len(M) > 0:
                B.append(M[:int((b - c) / 8)])
                M = M[int((b - c) / 8):]

            i = 0
            p = 0
            l = len(B)

            while i < l:
                p = P if i == (len(B) - 1) else 0
                z = 1 if i == (len(B) - 1) else 0
                C = mid(B[i], C, i, p, z)

                i += 1
                p = 0

            return self.__from_word(C)

        while True:
            ell += 1
            M = seq(M) if ell > L else par(M)

            if len(M) == c:
                break

        return self.__crop(d, M, True)

    def __bytes(self, b):
        o_byte = list(b)
        return o_byte

    def __prehash(self, data, size, key, levels):
        data = self.__bytes(data)
        key = self.__bytes(key)

        if size <= 0:
            size = 1
        elif size > 512:
            size = 512

        return self.__hash(size, data, key, levels)

    def hex(self, data=b"", size=256, key="", levels=64):
        byte = self.__prehash(data, size, key, levels)
        hexstr = ""

        for i in byte:
            hexstr += "%02x" % i

        return hexstr

    def raw(self, data=b"", size=256, key="", levels=64):
        byte = self.__prehash(data, size, key, levels)
        rawstr = ""
        return bytes(byte)
