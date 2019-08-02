""" Base App Config file """
from flask import Flask, Response

# Init App
app = Flask(__name__)


# Index "Hello World"
@app.route('/', methods=['GET'])
def get():
    return Response("Hello Worlds", mimetype='text/html', status=200)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
