#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from datetime import datetime
from sqlalchemy import (Column, DateTime, Integer, String)
from sqlalchemy import exc
from sqlalchemy.orm import exc as orm_exc
from lib.exceptions import APIException
from lib import (Base, session)
# from lib.constants import BASE_URL, QUESTION
# from app.tasks import question as QuestionTask


class Question(Base):
    __tablename__ = 'questions'

    question_id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    interview_id = Column(Integer, nullable=False)
    question = Column(String, nullable=False)

    @staticmethod
    def create(i_question):
        try:
            question = Question(**i_question)
            session.add(question)
            session.commit()
            session.refresh(question)
            return question
        except exc.IntegrityError as err:
            raise APIException("", "", err.message)

    @staticmethod
    def get(**kwargs):
        try:
            return session.query(Question).filter_by(**kwargs).one()
        except orm_exc.NoResultFound:
            raise APIException("", "")

    @staticmethod
    def list(interview_id):
        return session.query(Recording).filter(interview_id=interview_id)
