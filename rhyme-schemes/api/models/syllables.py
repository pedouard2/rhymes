import yaml
from pathlib import Path
import requests
import re
import pronouncing

def get_credentials():
    full_file_path = Path(__file__).parent.parent.joinpath('instance/credentials.yaml')
    with open(full_file_path) as credentials:
        credential_data = yaml.load(credentials, Loader=yaml.Loader)
    return credential_data

global credentials
credentials = get_credentials()
pattern  = r"([AEIOU]+.{2})\s?"
regex_pattern = re.compile(pattern)


def get_syllables(word, key = credentials["Dictionary"]["key"]):

    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={key}"
    try:
        r = requests.get(url)
    except:
        print("Please check API")
    
    if r.status_code == requests.codes.ok:
        r = r.json()
        return r[0]["hwi"]["hw"].split("*")

def get_sounds(word):
    pronounciation = pronouncing.phones_for_word(word)[0]
    return regex_pattern.findall(pronounciation), pronouncing.stresses(pronounciation)
