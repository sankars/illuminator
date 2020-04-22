from flask import Flask, Response, request
from flask_cors import CORS
from api import google
from api import amazon
import logging

app = Flask(__name__)
CORS(app)


@app.route("/analyze/language", methods=['POST'])
def analyze_language():
    request_data = request.get_json()
    engine = request_data['engine']
    text = request_data['text']

    if str.lower(engine) == 'google':
        return Response(google.detect_language(text), mimetype="application/json")
    elif str.lower(engine) == 'amazon':
        return Response(amazon.detect_language(text), mimetype="application/json")


@app.route("/analyze/entities", methods=['POST'])
def analyze_entities():
    request_data = request.get_json()
    engine = request_data['engine']
    text = request_data['text']

    if str.lower(engine) == 'google':
        return Response(google.detect_entities(text), mimetype="application/json")
    elif str.lower(engine) == 'amazon':
        return Response(amazon.detect_entities(text), mimetype="application/json")


@app.route("/analyze/sentiment", methods=['POST'])
def detect_sentiment():
    request_data = request.get_json()
    engine = request_data['engine']
    text = request_data['text']

    if str.lower(engine) == 'google':
        return Response(google.detect_sentiment(text), mimetype="application/json")
    elif str.lower(engine) == 'amazon':
        return Response(amazon.detect_sentiment(text), mimetype="application/json")


@app.route("/analyze/syntax", methods=['POST'])
def analyze_syntax():
    request_data = request.get_json()
    engine = request_data['engine']
    text = request_data['text']

    if str.lower(engine) == 'google':
        return Response(google.detect_syntax(text), mimetype="application/json")
    elif str.lower(engine) == 'amazon':
        return Response(amazon.detect_syntax(text), mimetype="application/json")


@app.route("/translate", methods=['POST'])
def translate_text():
    request_data = request.get_json()
    engine = request_data['engine']
    text = request_data['text']
    target = request_data['target']

    if str.lower(engine) == 'google':
        return Response(google.translate_text(text, target), mimetype="application/json")
    elif str.lower(engine) == 'amazon':
        return Response(amazon.translate_text(text, target), mimetype="application/json")


if __name__ == "__main__":
    app.config['LOG_LEVEL'] = logging.WARNING
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
