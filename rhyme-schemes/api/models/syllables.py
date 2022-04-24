import re
from pathlib import Path

import pronouncing
import requests
import yaml

from .decorators import word_in_dictionary


def get_credentials():
    full_file_path = Path(__file__).parent.parent.joinpath('instance/credentials.yaml')
    with open(full_file_path) as credentials:
        credential_data = yaml.load(credentials, Loader=yaml.Loader)
    return credential_data

global credentials
credentials = get_credentials()
pattern  = r"([AEIOU]+.{2})\s?"
regex_pattern = re.compile(pattern)

def greedy_split(w,chunk):
    return [w[i:i+chunk] for i in range(0,len(w),chunk)]

@word_in_dictionary
def get_syllables(word, key = credentials["Dictionary"]["key"]):

    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={key}"
    try:
        r = requests.get(url)
    except:
        print("Please check API")
    
    if r.status_code == requests.codes.ok:
        r = r.json()
        try:
            v = r[0]["hwi"]["hw"].split("*")
            if "".join(v) == word:
                return v
            else:
                return greedy_split(word,len(word)//pronouncing.syllable_count(pronouncing.phones_for_word(word)[0]))
        except:
            return []

@word_in_dictionary
def get_sounds(word):
    pronounciation = pronouncing.phones_for_word(word)[0]
    return regex_pattern.findall(pronounciation), pronouncing.stresses(pronounciation)

