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
    from sqlalchemy import String as VARCHAR, Integer

    class INTEGER(Integer):
        def __init__(self, *args, **kwargs):
            super(Integer, self).__init__()  # pylint: disable=bad-super-call


DECLARATIVE_BASE = declarative_base()


class Task(DECLARATIVE_BASE):

    __tablename__ = 'tasks'
    __table_args__ = (
        {'mysql_engine': 'ndbcluster', 'mysql_charset': 'utf8'}
    )

    id = Column(INTEGER, nullable=False, autoincrement=False, primary_key=True)  # pylint: disable=invalid-name
    title = Column(VARCHAR(45))
    description = Column(VARCHAR(45))
    notes = Column(INTEGER)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<Task(%(id)s)>" % self.__dict__


class Note(DECLARATIVE_BASE):

    __tablename__ = 'notes'
    __table_args__ = (
        {'mysql_engine': 'ndbcluster', 'mysql_charset': 'utf8'}
    )

    id = Column(  # pylint: disable=invalid-name
        VARCHAR(45), ForeignKey("tasks.notes", name="fk_notes_tasks"), nullable=False, autoincrement=False,
        primary_key=True
    )
    note = Column(VARCHAR(500))

    task = relationship("Task", foreign_keys=[id], backref="notes")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<Note(%(id)s)>" % self.__dict__


class User(DECLARATIVE_BASE):

    __tablename__ = 'users'
    __table_args__ = (
        {'mysql_engine': 'ndbcluster', 'mysql_charset': 'utf8'}
    )

    id = Column(INTEGER, nullable=False, autoincrement=False, primary_key=True)  # pylint: disable=invalid-name
    username = Column(VARCHAR(45))
    password = Column(VARCHAR(45))
    platforms_id = Column(
        INTEGER, ForeignKey("platforms.id", name="user_platform"), nullable=False, autoincrement=False,
        primary_key=True, index=True
    )

    platform = relationship("Platform", foreign_keys=[platforms_id], backref="users")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<User(%(id)s, %(platforms_id)s)>" % self.__dict__


class Platform(DECLARATIVE_BASE):

    __tablename__ = 'platforms'
    __table_args__ = (
        {'mysql_engine': 'ndbcluster', 'mysql_charset': 'utf8'}
    )

    id = Column(INTEGER, nullable=False, autoincrement=False, primary_key=True)  # pylint: disable=invalid-name
    name = Column(VARCHAR(45))
    notifications = Column(VARCHAR(45))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<Platform(%(id)s)>" % self.__dict__


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


class PlatformsHasNotification(DECLARATIVE_BASE):

    __tablename__ = 'platforms_has_notifications'
    __table_args__ = (
        {'mysql_engine': 'ndbcluster', 'mysql_charset': 'utf8'}
    )

    platforms_id = Column(
        INTEGER, ForeignKey("platforms.id", name="fk_platforms_has_notifications_platforms1"), nullable=False,
        autoincrement=False, primary_key=True, index=True
    )
    notifications_id = Column(
        INTEGER, ForeignKey("notifications.id", name="fk_platforms_has_notifications_notifications1"), nullable=False,
        autoincrement=False, primary_key=True, index=True
    )

    platform = relationship("Platform", foreign_keys=[platforms_id], backref="platformsHasNotifications")
    notification = relationship("Notification", foreign_keys=[notifications_id], backref="platformsHasNotifications")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<PlatformsHasNotification(%(platforms_id)s, %(notifications_id)s)>" % self.__dict__


class TasksUser(DECLARATIVE_BASE):

    __tablename__ = 'tasks_users'
    __table_args__ = (
        {'mysql_engine': 'ndbcluster', 'mysql_charset': 'utf8'}
    )

    id = Column(  # pylint: disable=invalid-name
        "task_id", INTEGER, ForeignKey("tasks.id", name="task_id"), nullable=False, autoincrement=False,
        primary_key=True
    )
    created_by = Column(INTEGER, ForeignKey("users.id", name="created_by"), nullable=False, index=True)
    started_by = Column(INTEGER, ForeignKey("users.id", name="started_by"), nullable=False, index=True)
    finished_by = Column(INTEGER, ForeignKey("users.id", name="finished_by"), nullable=False, index=True)

    task = relationship("Task", foreign_keys=[id], backref="tasksUsers")
    user = relationship("User", foreign_keys=[created_by], backref="tasksUsers")
    user = relationship("User", foreign_keys=[started_by], backref="tasksUsers")
    user = relationship("User", foreign_keys=[finished_by], backref="tasksUsers")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<TasksUser(%(id)s)>" % self.__dict__
