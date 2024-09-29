import jwt
import flask
from flask import Flask, g, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import parse_rss
import goog_llm
import goog_tts
import pg8000

load_dotenv()

app = Flask(__name__)
CORS(app)

# fetch environment variables
STORY_PER_SOURCE_COUNT = 3
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
if DB_USERNAME == None or DB_PASSWORD == None:
    raise Exception("DB_USERNAME or DB_PASSWORD env vars not set!")

# Database configuration
app.config['DB_HOST'] = '127.0.0.1'
app.config['DB_PORT'] = 5432
app.config['DB_USER'] = DB_USERNAME
app.config['DB_PASSWORD'] = DB_PASSWORD
app.config['DB_NAME'] = 'news_briefer'

def get_db():
    if 'db' not in g:
        g.db = pg8000.connect(
            host=app.config['DB_HOST'],
            port=app.config['DB_PORT'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            database=app.config['DB_NAME']
        )
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

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
    if decoded.get('email') is not None:
      g.current_user_email = decoded["email"]
      return True
    return False
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
  # TODO: do a lookup in mongodb, this is hardcoded
  if req_body and req_body['email'] == 'email' and req_body['password'] == 'pass':
    token = jwt.encode({'email': req_body['email']}, os.environ.get("JWT_SECRET_KEY"))
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

@app.route('/get-sources', methods=["GET"])
def get_soruces():
  req_body = request.json
  if not check_auth(req_body):
    return jsonify({'message': RESPONSE_MESSAGES['invalid_auth']})
  
  db = get_db()
  cursor = db.cursor()
  cursor.execute("select * from sources where email = " + g.current_user_email)
  
  results = cursor.fetchall() 
  # ^^ returns a tuple: (<email>, <source>)
  # ignoring the email field for now
  
  results = [src for _, src in results]
  return jsonify({"sources": results})

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
