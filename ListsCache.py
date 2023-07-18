import pandas as pd

ListOfCur = []
ListOfCrypto = []

DictOfFlags = {}
EmptyDictOfFlags = {}
DictOfSymbols = {}
EmptyDictOfSymbols = {}

TokensForW2N = ""
ExceptionsForW2N = []

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

def SetDictOfSymbols(newDictOfSymbols: dict):
    global DictOfSymbols
    DictOfSymbols = newDictOfSymbols

def GetDictOfSymbols() -> dict:
    global DictOfSymbols
    return DictOfSymbols

def SetEmptyDictOfSymbols(newEmptyDictOfSymbols: dict):
    global EmptyDictOfSymbols
    EmptyDictOfSymbols = newEmptyDictOfSymbols

def GetEmptyDictOfSymbols() -> dict:
    global EmptyDictOfSymbols
    return EmptyDictOfSymbols

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
    TokensForW2N = pd.read_csv('Dictionaries/w2n_tokens.csv', sep=',')

def GetTokensForW2N() -> pd.DataFrame:
    global TokensForW2N
    return TokensForW2N

def SetExceptionsForW2N():
    global ExceptionsForW2N
    newExceptionsForW2N = []
    with open('Dictionaries/w2n_exceptions.txt', 'r') as file:
        for line in file:
            newExceptionsForW2N.append(line.replace("\n", ""))
    ExceptionsForW2N = newExceptionsForW2N

def GetExceptionsForW2N() -> list:
    global ExceptionsForW2N
    return ExceptionsForW2N