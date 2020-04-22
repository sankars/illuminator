import boto3
import json

comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')


def detect_language(text):

    lang_response = comprehend.detect_dominant_language(Text=text)
    return '{ "Language" : "' + lang_response["Languages"][0]["LanguageCode"] + '"}'


def detect_entities(text):

    entity_response = comprehend.detect_entities(Text=text, LanguageCode='en')
    for entity in entity_response["Entities"]:
        entity.pop('Score', None)
        entity.pop('EndOffset', None)
    return json.dumps(dict(Entities = entity_response["Entities"]))


def detect_sentiment(text):

    sentiment_response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return '{ "Sentiment" : "' + sentiment_response["Sentiment"] + '"}'


def detect_key_phrases(text):

    phrases_response = comprehend.detect_key_phrases(Text=text, LanguageCode='en')
    return json.dumps(phrases_response["KeyPhrases"])


def detect_syntax(text):

    syntax_response = comprehend.detect_syntax(Text=text, LanguageCode='en')
    response = dict()
    token_list = []
    for token in syntax_response["SyntaxTokens"]:
        token_dict = dict()
        token_dict['Token'] = token['Text']
        token_dict['Tag'] = token['PartOfSpeech']['Tag']
        token_dict['BeginOffset'] = token['BeginOffset']
        token_list.append(token_dict)
    response["Tokens"] = token_list

    return json.dumps(response)


def translate_text(text, target):

    client = boto3.client('translate')
    translate_response = client.translate_text(
        Text=text,
        SourceLanguageCode='auto',
        TargetLanguageCode=target
    )
    response = dict()
    response['TranslatedText'] = translate_response['TranslatedText']
    response['DetectedSourceLanguge'] = translate_response['SourceLanguageCode']

    return json.dumps(response)
