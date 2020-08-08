from wandbox import wandbox
from app import webserver


if __name__ == '__main__':
#     code = ('''\
# # This file is a "Hello, world!" in Python language by CPython for wandbox.

# import json

# def f():
#     print('This is America!')

# d = json.dumps({'aa': 1})
# print("Hello, world!", d)
# f()

# # CPython references:
# #   https://www.python.org/
#     ''')
#     response = wandbox.compile(code)
#     print(response)
    webserver.start_webserver()