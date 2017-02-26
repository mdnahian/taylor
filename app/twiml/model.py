#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from datetime import datetime
from sqlalchemy import (Column, DateTime, Integer, String)
from sqlalchemy import exc
from sqlalchemy.orm import exc as orm_exc
from lib.exceptions import APIException
from lib import (Base, session)


class Twiml(Base):
    __tablename__ = 'twimls'

    twiml_id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    xml = Column(String, nullable=False)

    @staticmethod
    def create(i_twiml):
        try:
            twiml = Twiml(**i_twiml)
            session.add(twiml)
            session.commit()
            session.refresh(twiml)
            return twiml
        except exc.IntegrityError as err:
            raise APIException("", "", err.message)

    @staticmethod
    def get(**kwargs):
        try:
            return session.query(Twiml).filter_by(**kwargs).one()
        except orm_exc.NoResultFound:
            raise APIException("", "")
