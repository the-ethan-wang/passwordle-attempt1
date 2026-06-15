# Attempt 1:
# play like its hard mode wordle, search for guesses that satisfy previous knowledge

import hashlib

def get_hash(x: str):
    return hashlib.sha256(x.encode('utf-8')).hexdigest()

def satisfy_ruleset(hash: str, ruleset: list):
    pass
