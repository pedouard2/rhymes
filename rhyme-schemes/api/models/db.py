import sqlite3
from tkinter import W
from sqlalchemy.sql.expression import except_all 
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select, UniqueConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

DB = "bar.db"

Base = declarative_base()

class Sounds(Base):
    __tablename__ = "sounds"
    sound = Column(String, primary_key = True, unique = True)
    color = Column(String, unique = True)
    
    def __repr__(self):
        return f"Words(id={self.sound!r}, word={self.color!r})"

class Words(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True)
    word = Column(String)
    syllable = Column(String)
    sound = Column(String)
    stress = Column(Integer)
    
    def __repr__(self):
        return f"Words(id={self.id!r}, word={self.word!r}, syllable={self.syllable!r}, sound={self.sound!r}, stress={self.stress!r})"


def init():
    global engine 
    engine = create_engine("sqlite:///" + DB, echo=True, future=True)
    Base.metadata.create_all(engine)

def add_word(w,syllables,sounds,stresses):
    ## assert that they are all the same length 

    with Session(engine) as session:
        load = []
        for syll,sound,stress in zip(syllables,sounds,stresses):
            entry  = Words(
                word=w,
                syllable=syll,
                sound=sound,
                stress=stress
                )
            load.append(entry)
        session.add_all(load)
        session.commit()

    print(f"Successfully added {w} to database")

def get_word(w):
    res = {}
    
    words = []
    with Session(engine) as session:
        statement = (
            select(Words)
            .where(Words.word == w)
            # .where(Words.stress > 0)
            )
        for word in session.scalars(statement):
            d = {}
            d["syllable"] = word.syllable
            d["sound"]= word.sound
            d["stress"] = word.stress
            words.append(d)
    res[w] = words
    return res

 
init()

