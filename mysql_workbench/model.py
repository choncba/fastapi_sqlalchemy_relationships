#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
This file has been automatically generated with workbench_alchemy v0.4
For more details please check here:
https://github.com/PiTiLeZarD/workbench_alchemy
"""

import os
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

if os.environ.get('DB_TYPE', 'MySQL') == 'MySQL':
    from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
else:
    from sqlalchemy import Integer, String as VARCHAR

    class INTEGER(Integer):
        def __init__(self, *args, **kwargs):
            super(Integer, self).__init__()  # pylint: disable=bad-super-call


DECLARATIVE_BASE = declarative_base()


class Notification(DECLARATIVE_BASE):

    __tablename__ = 'notifications'
    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    )

    id = Column(INTEGER, nullable=False, autoincrement=False, primary_key=True)  # pylint: disable=invalid-name
    name = Column(VARCHAR(45))
    type = Column(VARCHAR(45))
    email = Column(VARCHAR(45))
    url = Column(VARCHAR(45))
    webhook = Column(VARCHAR(45))
    token = Column(VARCHAR(45))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<Notification(%(id)s)>" % self.__dict__


class Task(DECLARATIVE_BASE):

    __tablename__ = 'tasks'
    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    )

    id = Column(INTEGER, nullable=False, autoincrement=False, primary_key=True)  # pylint: disable=invalid-name
    title = Column(VARCHAR(45))
    description = Column(VARCHAR(45))
    started_by_id = Column(
        INTEGER, ForeignKey("users.id", name="fk_started_by"), nullable=False, autoincrement=False, primary_key=True,
        index=True
    )

    user = relationship("User", foreign_keys=[started_by_id], backref="tasks")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<Task(%(id)s, %(started_by_id)s)>" % self.__dict__


class User(DECLARATIVE_BASE):

    __tablename__ = 'users'
    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    )

    id = Column(INTEGER, nullable=False, autoincrement=False, primary_key=True)  # pylint: disable=invalid-name
    username = Column(VARCHAR(45))
    password = Column(VARCHAR(45))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<User(%(id)s)>" % self.__dict__
