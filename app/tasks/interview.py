#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8


from twilio.rest import TwilioRestClient

account_sid = "AC564a7022d50ef41d59bb316ec4f0aabd"  # Your Account SID from www.twilio.com/console
auth_token = "ebecd1386153ef898ff84afeb8f7b1c4"  # Your Auth Token from www.twilio.com/console
base_url = "https://api.twilio.com"

client = TwilioRestClient(account_sid, auth_token)


def init_call(url, to):
    call = client.calls.create(url=url, to=to, from_="+13232714335",
                               record=True, method="GET")
    return call.sid
