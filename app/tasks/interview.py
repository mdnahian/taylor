#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8


from twilio.rest import TwilioRestClient
from lib.constants import BASE_URL
import requests

account_sid = "AC564a7022d50ef41d59bb316ec4f0aabd"  # Your Account SID from www.twilio.com/console
auth_token = "ebecd1386153ef898ff84afeb8f7b1c4"  # Your Auth Token from www.twilio.com/console
base_url = "https://api.twilio.com"

client = TwilioRestClient(account_sid, auth_token)


def send_url_sms(interview_id):
    client.messages.create(
        to="+16073388347",
        from_="+13232714335",
        body="Your interview analysis is available at " + BASE_URL + "/interviews/" + interview_id + "/stats",
    )


def init_call(url, to, interview_id):
    call = client.calls.create(url=url, to=to, from_="+13232714335",
                               record=True, method="GET",
                               recording_status_callback=BASE_URL + "/interviews/" + interview_id + "/actions/fetch_recordings",
                               recording_status_callback_method="POST",
                               recording_status_events=["completed"])
    return call.sid


def fetch_recordings(call_sid):
    recording_url = base_url + "/2010-04-01/Accounts/%s/Calls/%s/Recordings.json" % (account_sid, call_sid)
    r = requests.get(recording_url, auth=(account_sid, auth_token))
    recording_json = r.json()
    recordings = []
    for record in recording_json['recordings']:
        if record['source'] != 'RecordVerb':
            continue
        recording = {}
        recording['url'] = base_url + record['uri'][:-5]
        recording['r_sid'] = record['sid']
        recording['call_sid'] = call_sid
        rec = client.recordings.get(record['sid'])
        for t in rec.transcriptions.list():
            recording['text'] = t.transcription_text
            recordings.append(recording)
    return recordings


import json
import language_check
from os.path import join, dirname
from watson_developer_cloud import AlchemyLanguageV1


fillers = ['like', 'umm', 'ah', 'you know', 'ok so']

tool = language_check.LanguageTool('en-US')


def execute(raw):
    num_filler_words = 0
    num_grammatical_errors = 0
    raw_sections = raw
    sections = raw_sections['sections']
    result = '''
    {
    "sections": [
    '''
    for i in range(0, len(sections)):
        section = sections[i]
        question = section['question']
        response = section['response']
        result += '''
        {
        "question":"'''+question+'''",
        "response":"'''+response+'''",
        '''
        sentences = response.split('.')
        new_response = ''
        result += '''
        "grammatical_errors": [
        '''
        for sentence in sentences:
            sentence = sentence.strip()
            # num_filler_words_in_response = 0
            for filler_word in fillers:
                if filler_word in sentence:
                    num_filler_words += 1
                    # num_filler_words_in_response += 1
                    sentence.replace(filler_word, '')
            new_response += sentence + '. '
            grammer_matches = tool.check(sentence)

            if len(grammer_matches) > 0:
                result += '''
                {
                '''
                num_grammatical_errors += len(grammer_matches)
                result += '''
                "errors": [
                '''

                for i in range(0, len(grammer_matches)):
                    result += '''
                    {
                    "suggestion":"'''+grammer_matches[i].msg+'''",
                    "replacements":"'''+''.join(grammer_matches[i].replacements)+'''"
                    }
                    '''

                    if i < len(grammer_matches) - 1:
                        result += ','

                result += '''
                ],
                "sentence":"'''+sentence+'''",
                "corrected":"'''+language_check.correct(sentence.strip(), grammer_matches)+'''"
                }
                '''

        result += '''
        ],
        '''

        raw_text_analytics = getTextAnalytics(new_response)

        score = '0'
        try:
            score = raw_text_analytics['docSentiment']['score']
        except:
            pass

        result += '''
        "response_sentiment": {
        "score": "'''+score+'''",
        "type": "'''+raw_text_analytics['docSentiment']['type']+'''"
        },
        "emotions": {
        "anger": "'''+raw_text_analytics['docEmotions']['anger']+'''",
        "joy": "'''+raw_text_analytics['docEmotions']['joy']+'''",
        "fear": "'''+raw_text_analytics['docEmotions']['fear']+'''",
        "sadness": "'''+raw_text_analytics['docEmotions']['sadness']+'''",
        "disgust": "'''+raw_text_analytics['docEmotions']['disgust']+'''"
        }
        '''

        result += '''
        }
        '''

        if i < len(sections) - 1:
            result += ','

    result += '''
    ],
    "stats": {
    "num_filler_words": '''+str(num_filler_words)+''',
    "num_grammatical_errors": '''+str(num_grammatical_errors)+'''
    }
    }
    '''

    return json.loads(result)
    # return result.encode('ascii', 'ignore').decode('ascii')


def getTextAnalytics(text):
    alchemy_language = AlchemyLanguageV1(api_key='2a244174a9a41c43e449cf387a107093e50bdd64')
    combined_operations = ['entity', 'keyword', 'concept', 'doc-emotion', 'doc-sentiment']

    return alchemy_language.combined(text=text, extract=combined_operations)
