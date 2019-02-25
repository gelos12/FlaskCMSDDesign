from flask import Flask, request
from Controllers.MemoController import memo_bp

from db import init_db

app = Flask(__name__)
app.register_blueprint(memo_bp)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    init_db()
    app.run('localhost', 1633, True)

