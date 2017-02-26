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


class Interview(Base):
    __tablename__ = 'interviews'

    interview_id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    status = Column(Integer, nullable=False, default=0)
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
    def action(interview_id, action):
        try:
            interview = Interview.get(interview_id=interview_id)
            call_sid = InterviewTask.init_call(BASE_URL + "/twimls/1.xml", "+16073388347")
            interview.call_sid = call_sid
            interview.status = INTERVIEW.STATUS.INIT
            session.commit()
            session.refresh(interview)
            return interview
        except exc.IntegrityError as err:
            raise APIException("", "", err.message)
