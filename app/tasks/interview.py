#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8


from twilio.rest import TwilioRestClient
import requests

account_sid = "AC564a7022d50ef41d59bb316ec4f0aabd"  # Your Account SID from www.twilio.com/console
auth_token = "ebecd1386153ef898ff84afeb8f7b1c4"  # Your Auth Token from www.twilio.com/console
base_url = "https://api.twilio.com"

client = TwilioRestClient(account_sid, auth_token)


def init_call(url, to):
    call = client.calls.create(url=url, to=to, from_="+13232714335",
                               record=True, method="GET")
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
        rec = client.recordings.get(record['sid'])
        for t in rec.transcriptions.list():
            recording['text'] = t.transcription_text
        recordings.append(recording)
    return recordings
