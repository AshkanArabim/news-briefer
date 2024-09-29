import jwt
import flask
from flask import Flask, g, request, jsonify
from dotenv import load_dotenv
import os
import parse_rss
import goog_llm
import goog_tts
import pg8000

load_dotenv()

app = Flask(__name__)

# fetch environment variables
MAX_STORIES = 6
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
if DB_USERNAME == None or DB_PASSWORD == None:
    raise Exception("DB_USERNAME or DB_PASSWORD env vars not set!")


def get_db():
    if "db" not in g:
        g.db = pg8000.connect(
            host="127.0.0.1",
            port=5432,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database="news_briefer",
        )
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


if len(os.environ.get("JWT_SECRET_KEY")) == 0:
    print("jwt secret key not found")
    exit()

RESPONSE_MESSAGES = {
    "invalid_auth": "Invalid authentication token!",
    "valid_auth": "Token is valid. Welcome back!",  # this is mostly for debugging
}


# helpers
def check_auth(req_body):
    token = req_body.get("token")
    if not token:
        return False
    try:
        decoded = jwt.decode(
            token, os.environ.get("JWT_SECRET_KEY"), algorithms=["HS256"]
        )
        if decoded.get("email") is not None:
            g.current_user_email = decoded["email"]
            return True
        return False
    except jwt.InvalidTokenError:
        return False


def respond_invalid_auth():
    return jsonify({"message": RESPONSE_MESSAGES["invalid_auth"]}), 401


def respond_valid_auth():
    return jsonify({"message": RESPONSE_MESSAGES["valid_auth"]}), 200


# API endpoints
# TODO: make login generate a random RSA token
@app.route("/login", methods=["POST"])
def login():
    req_body = request.json
    # TODO: do a lookup in mongodb, this is hardcoded
    db = get_db()
    cursor = db.cursor()
    results = cursor.execute(
        "select * from users where email = %s and password = %s",
        (req_body["email"], req_body["password"]),
    )
    results = [r for r in results]
    email, password, lang = results[0] if len(results) > 0 else (None, None, None)

    if email != None:
        token = jwt.encode(
            {"email": email, "lang": lang}, os.environ.get("JWT_SECRET_KEY")
        )
        return jsonify({"token": token})

    return jsonify({"message": "Invalid credentials"}), 401


@app.route("/get-text", methods=["GET"])
def get_text():
    req_body = request.json
    if not check_auth(req_body):
        return respond_invalid_auth()
    
    # query db to get user's sources (assuming they're all valid rss feeds)
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
      "select * from sources where email = %s",
      (g.current_user_email,)
    )
    results = cursor.fetchall()
    sources = [source for _, source in results]
    
    # determine how many should be taken from each source
    items_per_src = MAX_STORIES // len(sources)
    
    news_stories = []
    for source in sources:
      # n param = number of articles to summarize, default is 5 articles
      news_stories.append(parse_rss.get_topn_articles(source, items_per_src + 1))

    text = "\n\n".join(news_stories)
    summary = goog_llm.summarize_news(text)

    return (jsonify({"summary": summary}), 200)


@app.route("/get-audio", methods=["GET"])
def get_audio():
    req_body = request.json
    if not check_auth(req_body):
        return jsonify({"message": RESPONSE_MESSAGES["invalid_auth"]})
    # link will be replaced by db query to sources
    text = parse_rss.get_topn_articles("https://www.cbsnews.com/latest/rss/politics")
    summary = goog_llm.summarize_news(text)

    # goog_tts.text_to_wav("name of voice model", text to say)
    # some voice models: en-US-Studio-O, fr-FR-Neural2-A.wav, es-ES-Standard-B

    voice_stream = goog_tts.text_to_audio_stream("en-US-Studio-O", summary)
    return voice_stream


@app.route("/get-sources", methods=["GET"])
def get_soruces():
    req_body = request.json
    if not check_auth(req_body):
        return jsonify({"message": RESPONSE_MESSAGES["invalid_auth"]})

    db = get_db()
    cursor = db.cursor()
    cursor.execute("select * from sources where email = " + g.current_user_email)

    results = cursor.fetchall()
    # ^^ returns a tuple: (<email>, <source>)
    # ignoring the email field for now

    results = [src for _, src in results]
    return jsonify({"sources": results})


@app.route("/add-source", methods=["POST"])
def add_source():
    req_body = request.json
    if not check_auth(req_body):
        return jsonify({"message": RESPONSE_MESSAGES["invalid_auth"]})
    # TODO: add to db
    return respond_valid_auth()


@app.route("/remove-source", methods=["POST"])
def remove_source():
    req_body = request.json
    if not check_auth(req_body):
        return jsonify({"message": RESPONSE_MESSAGES["invalid_auth"]})
    # TODO: remove source from db by its id?
    return respond_valid_auth()


if __name__ == "__main__":
    app.run(debug=True)  # TODO: remove in prod
