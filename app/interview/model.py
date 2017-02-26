#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from datetime import datetime
from sqlalchemy import (Column, DateTime, Integer, String)
from sqlalchemy import exc
from sqlalchemy.orm import exc as orm_exc
from lib.exceptions import APIException
from lib import (Base, session)
from lib.constants import BASE_URL, INTERVIEW
from app.tasks import interview as InterviewTask
from app.question.model import Question
from app.recording.model import Recording


class Interview(Base):
    __tablename__ = 'interviews'

    interview_id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    status = Column(Integer, nullable=False, default=INTERVIEW.STATUS.PENDING)
    name = Column(String)
    call_sid = Column(String)

    @staticmethod
    def create(i_interview):
        try:
            interview = Interview(**i_interview)
            session.add(interview)
            session.commit()
            session.refresh(interview)
            return interview
        except exc.IntegrityError as err:
            raise APIException("", "", err.message)

    @staticmethod
    def get(**kwargs):
        try:
            return session.query(Interview).filter_by(**kwargs).one()
        except orm_exc.NoResultFound:
            raise APIException("", "")

    @staticmethod
    def init_call(interview_id):
        try:
            interview = Interview.get(interview_id=interview_id)
            call_sid = InterviewTask.init_call(BASE_URL + "/questions/1.xml", "+16073388347", interview_id)
            interview.call_sid = call_sid
            interview.status = INTERVIEW.STATUS.INIT
            session.commit()
            session.refresh(interview)
            return interview
        except exc.IntegrityError as err:
            raise APIException("", "", err.message)

    @staticmethod
    def fetch_recordings(interview_id):
        try:
            interview = Interview.get(interview_id=interview_id)
            recordings_list = InterviewTask.fetch_recordings(interview.call_sid)
            for recording_item in recordings_list:
                Recording.create(recording_item)
            return Recording.list(interview.call_sid)
        except exc.IntegrityError as err:
            raise APIException("", "", err.message)

    @staticmethod
    def list_recordings(interview_id):
        interview = Interview.get(interview_id=interview_id)
        return Recording.list(interview.call_sid)

    @staticmethod
    def analyze(interview_id):
        interview = Interview.get(interview_id=interview_id)
        questions = Question.list(interview_id=interview_id)
        recordings = Recording.list(interview.call_sid)
        raw = {'sections': []}
        i = 0
        for question in questions:
            entry = {}
            question = questions[i]
            recording = recordings[i]
            entry['question'] = question.question
            entry['response'] = recording.text
            raw['sections'].append(entry)
            i += 1
        return InterviewTask.execute(raw)

    @staticmethod
    def get_stats(interview_id):
        interview = Interview.get(interview_id=interview_id)
        questions = Question.list(interview_id=interview_id)
        recordings = Recording.list(interview.call_sid)
        raw = {'sections': []}
        i = 0
        for question in questions:
            entry = {}
            question = questions[i]
            recording = recordings[i]
            entry['question'] = question.question
            entry['response'] = recording.text
            raw['sections'].append(entry)
            i += 1
        return interview, zip(questions, recordings), InterviewTask.execute(raw)

    @staticmethod
    def get_transcripts(interview_id):
        interview = Interview.get(interview_id=interview_id)
        questions = Question.list(interview_id=interview_id)
        recordings = Recording.list(interview.call_sid)
        analysis = Interview.analyze(interview_id)
        return zip(questions, recordings, analysis['sections'])
