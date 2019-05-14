from flask import Flask
from app import app

if __name__ == "__main__":
#     app.secret_key = os.urandom(24)
    app.run(host="0.0.0.0", port=5003, debug=False, threaded=True)