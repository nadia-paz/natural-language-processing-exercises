import regex as re

def is_vowel(s:str):
    if re.findall('[aeiou]', s, re.IGNORECASE):
        return True
    else:
        return False

def is_valid_username(s:str) -> bool:
    if re.search(r'^[a-z][a-zA-Z0-9_]{,31}\b', s):
        return True
    else:
        return False

def phone_number(s:str) -> bool:
    if re.search(r'((\+1)?\s?\(?\d{3}?\)?(\s|\.|-)?)?\d{3}(\s|\.|-)\d{4}', s):
        return True
    else:
        return False