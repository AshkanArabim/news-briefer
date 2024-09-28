import jwt
import flask
from flask import request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

app = flask.Flask(__name__)

if len(os.environ.get("JWT_SECRET_KEY")) == 0:
  print("jwt secret key not found")
  exit()

@app.route('/login', methods=['POST'])
def login():
  auth = request.json
  # TODO: do a lookup in mongodb
  if auth and auth['username'] == 'user' and auth['password'] == 'pass':
    token = jwt.encode({'user': auth['username']}, os.environ.get("JWT_SECRET_KEY"))
    return jsonify({'token': token})
  return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
  app.run(debug=True)
