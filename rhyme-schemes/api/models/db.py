import sqlite3
from tkinter import W
from sqlalchemy.sql.expression import except_all 
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select, UniqueConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session
import random

DB = "bar.db"
COLORS = ["Aquamarine", "Coral", "CornflowerBlue", "DarkSeaGreen","DarkSlateBlue", "DarkSalmon", "HoneyDew", "LightSkyBlue", "LightYellow", "NavajoWhite", "Peru","Turquoise", "Tomato",  "YellowGreen", "SpringGreen" ]

def rand_color(c):
    i = random.randint(0,len(c)-1)
    return c[i]



def init():
    global engine 
    global Base 
    Base = declarative_base()
    engine = create_engine("sqlite:///" + DB, echo=True, future=True)

init()


class Lexicon(Base):
    __tablename__ = "lexicon"
    id = Column(Integer, primary_key=True)
    word = Column(String,  unique = True)    
    def __repr__(self):
        return f"Lexicon(word={self.word!r})"

class Words(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True)
    word = Column(String, ForeignKey("lexicon.word"))
    syllable = Column(String)
    sound = Column(String)
    stress = Column(Integer)
    
    def __repr__(self):
        return f"Words(id={self.id!r}, word={self.word!r}, syllable={self.syllable!r}, sound={self.sound!r}, stress={self.stress!r})"

Base.metadata.create_all(engine)


def add_word(w,syllables,sounds,stresses):

    with Session(engine) as session:

        try:
            stmt = Lexicon(word =w)
            session.add(stmt)
            session.commit()
        except:
            print(f"{w} already in  database")
            return

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
            )
        for word in session.scalars(statement):
            d = {}
            d["syllable"] = word.syllable
            d["sound"]= word.sound
            d["stress"] = word.stress
            words.append(d)
    res[w] = words
    return res

def generate_css():

    with open('css.txt', 'w') as f:
        with Session(engine) as session:
            statement = (
                select(Words.sound)
            )

        for s in list(set(session.scalars(statement))):
            f.write(

                f".{s}{{background-color: {rand_color(COLORS)} }}"
                f"\n"
                

            )

generate_css()