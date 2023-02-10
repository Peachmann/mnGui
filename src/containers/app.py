from flask import Flask
import socket
import hashlib
app = Flask(__name__)


@app.route("/")
def default():
    return f"You reached {socket.gethostname()}!\n"


@app.route("/hash/<text>")
def hash_to_sha256(text='sample'):
    try:
        m = hashlib.sha256()
        m.update(bytes(str(text), 'utf-8'))
    except ValueError:
        pass
    return f"{m.hexdigest()}\n"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
