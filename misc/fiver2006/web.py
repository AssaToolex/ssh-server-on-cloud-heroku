# web.py

import datetime
import os
from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    tlink = 'http://t.me/The2007bot'
    return "Now {now}\n{tlink}".format(now=now, tlink=tlink)


if __name__ == '__main__':
    PORT = int(os.getenv('PORT', default=5000))
    app.run(threaded=True, port=PORT)
