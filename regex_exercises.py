import regex as re

# control lists
phones = [
    '(210) 867 5309',
    '+1 210.867.5309',
    '867-5309',
    '210-867-5309'
]

dates = [
    '02/04/19',
    '02/05/19',
    '02/06/19',
    '02/07/19',
    '02/08/19',
    '02/09/19',
    '02/10/19'
]

requests = [
    'GET /api/v1/sales?page=86 [16/Apr/2019:193452+0000] HTTP/1.1 {200} 510348 "python-requests/2.21.0" 97.105.19.58',
    'POST /users_accounts/file-upload [16/Apr/2019:193452+0000] HTTP/1.1 {201} 42 "User-Agent: Mozilla/5.0 (X11; Fedora; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36" 97.105.19.58',
    'GET /api/v1/items?page=3 [16/Apr/2019:193453+0000] HTTP/1.1 {429} 3561 "python-requests/2.21.0" 97.105.19.58'

]

# exercise 1
def is_vowel(s:str):
    '''
    checks if the string is vowel
    Parameters: s : string.
    Returns: true if the string is 1 character and it is a vowel
    '''
    return bool(re.search(r'^[AEIOUaeiou]$', string))

# exercise 2
def is_valid_username(s:str) -> bool:
    '''
    Checks if the username is valid.
    A valid username starts with a lowercase letter, and only consists of lowercase letters, numbers, or the _ character
    Parameters:
        s: username, string
    Returns:
        True if the username is valid
        False if the username is unvalid
    '''
    if re.search(r'^[a-z][a-zA-Z0-9_]{,31}\b', s):
        return True
    else:
        return False

# exercise 3
def phone_number(s:str) -> bool:
    '''
    Checks if the phone number is a valid US phone number
    '''
    if re.search(r'((\+1)?\s?\(?\d{3}?\)?(\s|\.|-)?)?\d{3}(\s|\.|-)\d{4}', s):
        return True
    else:
        return False
### clas solution
def is_phone_number(string):
    phone_number_re = "(\+?\d+)?.?(\(?\d{3}\)?)?.?\d{3}.?\d{4}"
    
    return bool(re.search(phone_number_re, string))

# exercise 4
def transform_date(s:str) -> str:
    '''
    Accepts the string with the date in format mm/dd/yy
    Returns the same string in format yyyy-mm-dd
    '''
    date = re.findall('\d{2}', s)
    month = date[0]
    day = date[1]
    year = '20' + date[2]
    return f'{year}-{month}-{day}'
# class solution
pd.Series(dates).str.replace(r'(\d{2})/(\d{2})/(\d{2})', r'20\3-\1-\2', regex=True)

# exercise 5
def parse_log(requests:list) -> dict:
    '''
    Parameters: 
        requests: list of strings, each string is a log
    Returns:
        dictionary with parsed: method, path, time, http_version, status, bytes, user_agent, ip address
    '''
    regexes = {
        'method':r'[A-Z]{3,4} ',
        'path':r'\/[a-z0-9_?=\/-]* ',
        'time':r'\[\d{2}\/[A-Z][a-z]{2}\/\d{4}:\d{6}\+\d{4}\]',
        'http_version':r'[A-Z]{4,5}\/\d\.\d',
        'status':r'\{\d{3}\}',
        'bytes':r' \d{2,6} ',
        'user_agent':r'\".*\"',
        'ip':r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    }
    parse_dict = {
        'method':[],
        'path':[],
        'time':[],
        'http_version':[],
        'status':[],
        'bytes':[],
        'user_agent':[],
        'ip':[]
    }
    for s in requests:
        for key in regexes:
            parse_dict[key].append(re.search(regexes[key],s).group())
    return pd.DataFrame(parse_dict)

# class solution
logfile_re = r'''
^(?P<method>GET|POST)
\s+
(?P<path>.*?)
\s+
\[(?P<timestamp>.*?)\]
\s+
(?P<http_version>.*?)
\s+
\{(?P<status>\d+)\}
\s+
(?P<bytes>\d+)
\s+
"(?P<user_agent>.*)"
\s+
(?P<ip>.*)$
'''


pd.Series(requests).str.extract(logfile_re, re.VERBOSE)