from google.cloud import language
from google.cloud import translate
from google.cloud.language import enums,types
import json

entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
               'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
           'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')


def detect_entities(text):
    client = language.LanguageServiceClient()
    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    entities = client.analyze_entities(document, encoding_type='UTF8').entities
    response = dict()
    entity_list = []
    for entity in entities:
        entity_dict = dict()
        entity_dict["Name"]= entity.name
        entity_dict["Type"]= entity_type[entity.type]
        entity_dict["BeginOffset"] = entity.mentions[0].text.begin_offset
        entity_list.append(entity_dict)
    response["Entities"] = entity_list
    return json.dumps(response)


def detect_language(text):
    client = translate.Client()
    language_response = client.detect_language(text)
    return '{ "Language" : "' + language_response['language'] + '" }'


def detect_sentiment(text):
    client = language.LanguageServiceClient()
    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document)
    return '{ "Sentiment" : "' + \
           ('POSITIVE' if sentiment.document_sentiment.score > 0.15 else \
            'NEGATIVE' if sentiment.document_sentiment.score < -0.1 else 'NEUTRAL') + '" }'


def detect_syntax(text):
    client = language.LanguageServiceClient()
    document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    tokens = client.analyze_syntax(document, encoding_type='UTF8').tokens
    response = dict()
    token_list = []
    for token in tokens:
        token_dict = dict()
        token_dict['Token']= token.text.content
        token_dict["Tag"]= pos_tag[token.part_of_speech.tag]
        token_dict["BeginOffset"] = token.text.begin_offset
        token_list.append(token_dict)

    response["Tokens"] = token_list
    return json.dumps(response)


def translate_text(text, target):
    client = translate.Client()
    translate_response = client.translate(text, target_language=target)

    response = dict()
    response['TranslatedText'] = translate_response['translatedText']
    response['DetectedSourceLanguge'] = translate_response['detectedSourceLanguage']

    return json.dumps(response)
