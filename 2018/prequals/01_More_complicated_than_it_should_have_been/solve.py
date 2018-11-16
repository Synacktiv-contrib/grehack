# coding=utf-8


import jwt


print(jwt.encode({"admin": True, "user": 16}, '', None))
