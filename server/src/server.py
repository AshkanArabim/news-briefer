import jwt
import flask
from flask import request, jsonify
from dotenv import load_dotenv
import os
import parse_rss
import goog_llm
import goog_tts

load_dotenv()

app = flask.Flask(__name__)

if len(os.environ.get("JWT_SECRET_KEY")) == 0:
  print("jwt secret key not found")
  exit()
  
RESPONSE_MESSAGES = {
  "invalid_auth": "Invalid authentication token!",
  "valid_auth": "Token is valid. Welcome back!" # this is mostly for debugging
}

# helpers
def check_auth(req_body):
  token = req_body.get('token')
  if not token:
    return False
  try:
    decoded = jwt.decode(token, os.environ.get("JWT_SECRET_KEY"), algorithms=["HS256"])
    return decoded.get('user') is not None
  except jwt.InvalidTokenError:
    return False
  
def respond_invalid_auth():
  return jsonify({'message': RESPONSE_MESSAGES["invalid_auth"]}), 401

def respond_valid_auth():
  return jsonify({'message': RESPONSE_MESSAGES["valid_auth"]}), 200

# API endpoints
# TODO: make login generate a random RSA token
@app.route('/login', methods=['POST'])
def login():
  req_body = request.json
  # TODO: do a lookup in mongodb
  if req_body and req_body['username'] == 'user' and req_body['password'] == 'pass':
    token = jwt.encode({'user': req_body['username']}, os.environ.get("JWT_SECRET_KEY"))
    return jsonify({'token': token})
  return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/get-text', methods=["GET"])
def get_text():
  req_body = request.json
  if not check_auth(req_body):
    return respond_invalid_auth()
  # link will be replaced by db query to sources
  # n param = number of articles to summarize, default is 5 articles
  text = parse_rss.get_topn_articles("https://www.cbsnews.com/latest/rss/politics")
  summary = goog_llm.summarize_news(text)

  return (jsonify({'summary': summary}), 200)
  
@app.route('/get-audio', methods=["GET"])
def get_audio():
  req_body = request.json
  if not check_auth(req_body):
    return jsonify({'message': RESPONSE_MESSAGES['invalid_auth']})
  # link will be replaced by db query to sources
  text = parse_rss.get_topn_articles("https://www.cbsnews.com/latest/rss/politics")
  summary = goog_llm.summarize_news(text)

  # goog_tts.text_to_wav("name of voice model", text to say)
  # some voice models: en-US-Studio-O, fr-FR-Neural2-A.wav, es-ES-Standard-B

  voice_stream = goog_tts.text_to_audio_stream("en-US-Studio-O", summary)
  return voice_stream

@app.route('/add-source', methods=["POST"])
def add_source():
  req_body = request.json
  if not check_auth(req_body):
    return jsonify({'message': RESPONSE_MESSAGES['invalid_auth']})
  # TODO: add to db
  return respond_valid_auth()

@app.route('/remove-source', methods=["POST"])
def remove_source():
  req_body = request.json
  if not check_auth(req_body):
    return jsonify({'message': RESPONSE_MESSAGES['invalid_auth']})
  # TODO: remove source from db by its id?
  return respond_valid_auth()

if __name__ == '__main__':
  app.run(debug=True) # TODO: remove in prod
