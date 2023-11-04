#!/usr/bin/python


import bcrypt

passwd = b'bob'

salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(passwd, salt)

if bcrypt.checkpw(passwd, hashed):
    print("match")
else:
    print("does not match")

print(hashed)

