#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from datetime import datetime
from sqlalchemy import (Column, DateTime, Integer, String)
from sqlalchemy import exc
from sqlalchemy.orm import (backref, relationship)
from sqlalchemy.orm import exc as orm_exc
from lib.exceptions import APIException
from lib import (Base, session)


class Interview(Base):
    __tablename__ = 'interviews'

    interview_id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    stars = Column(Integer, nullable=False)

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
