import json
from flask import Flask, request, jsonify
from models import syllables, db, decorators
from datetime import date, datetime
import logging

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

@app.route('/api/add')
def add_word():
    w = request.args.get("word")
    syl = syllables.get_syllables(w)
    sounds,stresses = syllables.get_sounds(w)

    if len(syl) == 0:
        return  jsonify({w:[]})

    db.add_word(w,syl,sounds,stresses) 
    return jsonify(db.get_word(w))

@app.route('/api/time')
def get_time():
    return jsonify({"time": str(datetime.now())})

@app.route('/api/get')
def get_word():
    w = request.args.get("word")
    
    return jsonify(db.get_word(w))
