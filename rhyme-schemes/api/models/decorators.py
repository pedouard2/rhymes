import functools
from winreg import KEY_WOW64_32KEY
import pronouncing 

def word_in_dictionary(func):
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        word  = str(args[0])
        if len(pronouncing.phones_for_word(word)) > 0:
            return func(*args, **kwargs)
        else:
            if func.__name__ == "get_sounds":
                return [],""
            else:
                return []
    
    return wrapper
    