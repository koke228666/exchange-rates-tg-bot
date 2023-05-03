import pandas as pd

ListOfCur = []
ListOfCrypto = []

DictOfFlags = {}
EmptyDictOfFlags = {}

TokensForW2N = ""

def SetEmptyDictOfFlags(newEmptyDictOfFlags: dict):
    global EmptyDictOfFlags
    EmptyDictOfFlags = newEmptyDictOfFlags

def GetEmptyDictOfFlags() -> dict:
    global EmptyDictOfFlags
    return EmptyDictOfFlags

def SetDictOfFlags(newDictOfFlags: dict):
    global DictOfFlags
    DictOfFlags = newDictOfFlags

def GetDictOfFlags() -> dict:
    global DictOfFlags
    return DictOfFlags

def SetListOfCrypto(newListOfCrypto: list):
    global ListOfCrypto
    ListOfCrypto = newListOfCrypto
    
def GetListOfCrypto() -> list:
    global ListOfCrypto
    return ListOfCrypto

def SetListOfCur(newListOfCur: list):
    global ListOfCur
    ListOfCur = newListOfCur

def GetListOfCur() -> list:
    global ListOfCur
    return ListOfCur

def SetTokensForW2N():
    global TokensForW2N
    TokensForW2N = pd.read_csv('Dictionaries/w2n_tokens.csv', sep=';')

def GetTokensForW2N() -> pd.DataFrame:
    global TokensForW2N
    return TokensForW2N