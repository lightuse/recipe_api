# -*- encoding: utf-8 -*-
import datetime
import sys
from sqlalchemy import (Column, String, Text, ForeignKey,CHAR, VARCHAR, INT,  \
                create_engine, MetaData, DECIMAL, DATETIME, exc, event, Index, \
                and_)
from sqlalchemy.ext.declarative import declarative_base

sys.dont_write_bytecode = True

base = declarative_base()

class recipe(base):
    __tablename__ = 'recipes'
    id = Column(INT, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(100))
    making_time = Column(VARCHAR(100))
    serves = Column(VARCHAR(100))
    ingredients = Column(VARCHAR(300))
    cost = Column(INT)
    created_at = Column(DATETIME)
    updated_at = Column(DATETIME)

    def __init__(self):
        now_data_time = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        self.created_at =  now_data_time
        self.updated_at =  now_data_time
