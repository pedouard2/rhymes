import sqlite3
from sqlalchemy.sql.expression import except_all 
import pandas as pd
from sqlalchemy import create_engine, Table, Column, String, MetaData, select, UniqueConstraint
import os

class SQLAlchemyDB:

    def __init__(self, db_name):
        self.db = db_name
        self.metadata_obj = MetaData()
        print(f"Creating engine for {self.db}")
        try:
            self._engine = create_engine(self.db)
        except:
            print("Unable to connect to db")

    def create_table(self, table_name, columns, constraints = []):
        """
        Creates a Table object within catalog of MetaData 

        Params: {
        table_name: String
        column: List of Tuples in form ("column name", DataType)
        }
        Returns: Table object
        """

        table = Table(table_name, self.metadata_obj)

        for column in columns:
            table.append_column(Column(column[0], column[1]))

        for constraint in constraints:
            table.append_constraint(constraint)


        self.metadata_obj.create_all(self._engine)
        print(f"Created table {table_name}")

        return table

    def insert_into_table(self, table, values):

        """
        Inserts values into  a database table 

        Params: {
        table: Table
        values: List of Ditcionaries with distinct parameters
        }
        """
        conn = self._engine.connect()
        ins = table.insert()
        conn.execute(ins, values)

    def select_from_table(self, table, column = "all_columns"):
        """
        Selct rows from specified table 

        Params: {
        table: Table
        columns: (optional) String specified column names. Default all columns 
        }

        Return: List of Row objects
        """

        conn = self._engine.connect()

        if column == "all_columns":
            s = select(table)
            result = conn.execute(s)
            return result

        s = select(table.c[column])
        result  = conn.execute(s)
        return result


syllable_db = SQLAlchemyDB("sqlite:///" + "bar.sqlite")
syllable_table = syllable_db.create_table("syllables",[ ("word", String), ("pronunciation", String), ("syllables", String)], [UniqueConstraint("word")])
for row in syllable_db.select_from_table(syllable_table):
    print(row)