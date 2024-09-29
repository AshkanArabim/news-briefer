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
def check_auth(token):
    if not token:
        return False
    try:
        decoded = jwt.decode(
            token, os.environ.get("JWT_SECRET_KEY"), algorithms=["HS256"]
        )
        if decoded.get("email") is not None:
            g.current_user_email = decoded["email"]
            g.current_user_language = decoded["lang"]
            return True
        return False
    except jwt.InvalidTokenError:
        return False


def respond_invalid_auth():
    return jsonify({"message": RESPONSE_MESSAGES["invalid_auth"]}), 401


def respond_valid_auth():
    return jsonify({"message": RESPONSE_MESSAGES["valid_auth"]}), 200
  

def get_user_sources():
    # query db to get user's sources (assuming they're all valid rss feeds)
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select * from sources where email = %s", (g.current_user_email,))
    results = cursor.fetchall()
    return [source for _, source in results]


def get_all_sources_summary():
    sources = get_user_sources()

    # determine how many should be taken from each source
    items_per_src = MAX_STORIES // len(sources)

    news_stories = []
    for source in sources:
        # n param = number of articles to summarize, default is 5 articles
        news_stories.append(parse_rss.get_topn_articles(source, items_per_src + 1))

    text = "\n\n".join(news_stories)
    # TODO: add language support for spanish and french
    if g.current_user_language == "spanish":
        return goog_llm.summarize_news(text, "es")
    elif g.current_user_language == "french":
        return goog_llm.summarize_news(text, "fr")
    return goog_llm.summarize_news(text)


# API endpoints
# TODO: make login generate a random RSA token
@app.route("/login", methods=["POST"])
def login():
    req_body = request.json
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


@app.route("/signup", methods=["POST"])
def signup():
    req_body = request.json
    db = get_db()
    cursor = db.cursor()

    # check if user exists
    cursor.execute("select * from users where email = %s", (req_body["email"],))
    existing_user = cursor.fetchone()
    if existing_user is not None:
        return (
            jsonify(
                {"message": "account with that email already exists! please log in."}
            ),
            409,
        )

    # create the user
    cursor.execute(
        "insert into users (email, password, lang) values (%s, %s, %s)",
        (req_body["email"], req_body["password"], req_body["lang"]),
    )
    db.commit()

    return jsonify(
        {"message": "user created successfully. log in with your credentials"}
    )


@app.route("/get-text/<token>", methods=["GET"])
def get_text(token):
    if not check_auth(token):
        return respond_invalid_auth()

    summary = get_all_sources_summary()

    return jsonify({"summary": summary}), 200


@app.route("/get-headers/<token>", methods=['GET'])
def get_headers(token):
    if not check_auth(token):
        return respond_invalid_auth()

    sources = get_user_sources()

    # determine how many should be taken from each source
    items_per_src = MAX_STORIES // len(sources)

    news_headlines = []
    for source in sources:
        news_headlines.extend(parse_rss.get_topn_headlines(source, items_per_src + 1))

    return jsonify({"headlines": news_headlines})

@app.route("/get-audio/<token>", methods=["GET"])
def get_audio(token):
    if not check_auth(token):
        return jsonify({"message": RESPONSE_MESSAGES["invalid_auth"]})
    temp_audio_file_path = None
    summary = get_all_sources_summary()
    if g.current_user_language == "spanish":
        temp_audio_file_path = goog_tts.text_to_audio_stream("es-US-News-D", summary)
    elif g.current_user_language == "french":
        temp_audio_file_path = goog_tts.text_to_audio_stream("fr-FR-Neural2-A", summary)
    else:
        temp_audio_file_path = goog_tts.text_to_audio_stream("es-US-News-D", summary)

    return flask.send_file(temp_audio_file_path, mimetype="audio/mpeg")


@app.route("/get-sources/<token>", methods=["GET"])
def get_sources(token):
    if not check_auth(token):
        return jsonify({"message": RESPONSE_MESSAGES["invalid_auth"]})

    db = get_db()
    cursor = db.cursor()
    cursor.execute("select * from sources where email = %s", (g.current_user_email,))

    results = cursor.fetchall()
    # ^^ returns a tuple: (<email>, <source>)
    # ignoring the email field for now

    results = [src for _, src in results]
    return jsonify({"sources": results})


@app.route("/add-source/<token>", methods=["POST"])
def add_source(token):
    req_body = request.json
    if not check_auth(token):
        return jsonify({"message": RESPONSE_MESSAGES["invalid_auth"]})
    test = parse_rss.get_topn_headlines(req_body["source"])
    if len(test) == 0:
        return jsonify({"message": "invalid rss feed."}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "insert into sources values (%s, %s)",
        (g.current_user_email, req_body["source"]),
    )
    db.commit()

    return jsonify({"message": "source added successfully."})


@app.route("/remove-source/<token>", methods=["POST"])
def remove_source(token):
    req_body = request.json
    if not check_auth(token):
        return jsonify({"message": RESPONSE_MESSAGES["invalid_auth"]})

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "delete from sources where url = %s and email = %s",
        (req_body["source"], g.current_user_email),
    )
    db.commit()

    return jsonify({"message": f"source {req_body['source']} removed from database."})


if __name__ == "__main__":
    app.run(debug=True)  # TODO: remove in prod
