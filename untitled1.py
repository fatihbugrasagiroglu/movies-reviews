# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 21:50:38 2021

@author: fatih
"""

from flask import Flask





app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route("/")
def hello():
	return "Hello World"





if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)