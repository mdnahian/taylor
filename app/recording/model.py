#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from datetime import datetime
from sqlalchemy import (Column, DateTime, Integer, String)
from sqlalchemy import exc, UniqueConstraint
from sqlalchemy.orm import exc as orm_exc
from lib.exceptions import APIException
from lib import (Base, session)
from lib.constants import RECORDING
# from app.tasks import recording as RecordingTask


class Recording(Base):
    __tablename__ = 'recordings'

    recording_id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    status = Column(Integer, nullable=False, default=RECORDING.STATUS.PENDING)
    r_sid = Column(String, nullable=False, default="")
    call_sid = Column(String)
    url = Column(String, nullable=False, default="http://example.com")
    text = Column(String, default="")
    UniqueConstraint('r_sid', 'call_sid', name='r_sid_call_sid')

    @staticmethod
    def create(i_recording):
        try:
            recording = Recording(**i_recording)
            session.add(recording)
            session.commit()
            session.refresh(recording)
            return recording
        except exc.IntegrityError as err:
            raise APIException("", "", err.message)

    @staticmethod
    def get(**kwargs):
        try:
            return session.query(Recording).filter_by(**kwargs).one()
        except orm_exc.NoResultFound:
            raise APIException("", "")

    @staticmethod
    def action(recording_id, action):
        try:
            recording = Recording.get(recording_id=recording_id)
            recording.r_sid = ""
            recording.status = RECORDING.STATUS.COMPLETE
            session.commit()
            session.refresh(recording)
            return recording
        except exc.IntegrityError as err:
            raise APIException("", "", err.message)

    @staticmethod
    def list(call_sid):
        try:
            records = []
            for record in session.query(Recording).filter(call_sid==call_sid):
                records.append(record)
            return records
        except Exception:
            raise APIException("", "", err.message)
