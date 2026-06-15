# Attempt 1:
# play like its hard mode wordle, search for guesses that satisfy previous knowledge

from itertools import product
import hashlib

def get_hash(x: str):
    return hashlib.sha256(x.encode('utf-8')).hexdigest()

def satisfy_ruleset(hash: str, ruleset: dict) -> bool:
    for green in ruleset["greens"]:
        if hash[green[0]]!=green[1]:
            return False
    return True

"""
ruleset is just a dict with greens for now
greens is a list of green
each green is a tuple of index 0 to 63 to a hex character
"""

def search_for_satisfy(ruleset: dict, maxlen: int=5, last: str="") -> str:
    assert maxlen>0
    characterset = [chr(i) for i in range(32, 127)]

    for length in range(1, maxlen + 1):
        print(f"Searching for {length}")
        for item in product(characterset, repeat=length):
            utf8_string = "".join(item)
            if satisfy_ruleset(get_hash(utf8_string), ruleset):
                if utf8_string==last:continue
                return utf8_string
            
    return ""

def add_information(ruleset: dict, guess_hash: str, guess_result: list[int]):
    """in guess_result, 0 = gray, 1 = yellow, 2 = green"""
    for i, result in enumerate(guess_result):
        if result==2:
            ruleset["greens"].append((i, guess_hash[i]))
    return ruleset

def str_to_list(guess_result_str):
    ans=[]
    for char in guess_result_str:
        match char:
            case "Y":
                ans.append(1)
            case "G":
                ans.append(2)
            case "B":
                ans.append(0)
    return ans


ruleset = {
    "greens": []
}

result=str_to_list("YYYYYYGYYYYYYYBYYYBYYBYYYBYYYBYBGYYYYYYYBYBBYYBYYYYYBBYYBYYYBBYY")

ruleset = add_information(ruleset, guess_hash=get_hash("a"), guess_result=result)

result_b=str_to_list("YYYYYYGGYYGYYYYYYYYYYBYYYYYGYYYGGBYYYBYBBBGYGGBYBYBYBBGBYYYYYYBB")

ruleset = add_information(ruleset, guess_hash=get_hash("%"), guess_result=result_b)
print(len(ruleset["greens"]))
print("'"+search_for_satisfy(
    ruleset,
    maxlen=50,
    last="%"
)+"'") # wow this will take too long