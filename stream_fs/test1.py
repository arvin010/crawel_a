# -*- coding: utf-8 -*-
# @Author: SZW201208
# @Date:   2021-12-30 15:49:51
# @Last Modified by:   SZW201208
# @Last Modified time: 2022-02-11 15:50:21


# pip install pycryptodome


# # a.py
# from Crypto import Random
# from Crypto.PublicKey import RSA

# random_generator = Random.new().read
# rsa = RSA.generate(1024, random_generator)


# private_key = rsa.exportKey()
# with open('private.pem', 'w') as f:
#     f.write(private_key.decode('utf-8'))


# public_key = rsa.publickey().exportKey()
# with open('public.pem', 'w') as f:
#     f.write(public_key.decode('utf-8')
import collections


if __name__ == "__main__":
    print(1111111111)


def func1(p):
    print(p)


def a(fun, p):
    print(fun)
    fun(p)


print(eval('func' + '1'))
a(eval('func' + '1'), 1)
