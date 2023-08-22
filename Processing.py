from TextHelper import GetText
from DBH import GetAllCrypto, GetAllCurrencies, GetExchangeRates, GetListOfCrypto, GetListOfCurrencies, GetDictOfFlags, GetSetting, GetIgnoredCurrencies
import GetExchangeRates
import ListsCache
import os
import unicodedata
import re
import json

ListEntry = {}
ListEqual = {}
ListCryptoEntry = {}
ListCryptoEqual = {}


def RemoveSeparator(match):
    return match.group(1).replace(" ", "")


def MessagePreparation(MesTxt: str) -> str:
    MesTxt = MesTxt.lower()
    indexOfAtSign = -1
    indexOfSpace = -1

    while MesTxt.find("\n") != -1: # Removing line breaks
        MesTxt = MesTxt.replace("\n", " , ")

    while MesTxt.find("@") != -1:
        indexOfAtSign = MesTxt.find("@")
        indexOfSpace = MesTxt.find(" ", indexOfAtSign)
        if indexOfSpace == -1:
            indexOfSpace = len(MesTxt)
        if indexOfSpace > indexOfAtSign:
            MesTxt = MesTxt[0:indexOfAtSign] + MesTxt[indexOfSpace:]
        else: 
            break

    pattern = r"\b(?:https?:\/\/|www\.)\S+\b|\b\S+\.com\S*\b"
    MesTxt = re.sub(pattern, "", MesTxt) # Removing links

    while MesTxt.find("  ") != -1: # Removing double spaces
        MesTxt = MesTxt.replace("  ", " ")

    while MesTxt.find("'") != -1: # Removing apostrophes
        MesTxt = MesTxt.replace("'", "")


    while MesTxt.find("\xa0") != -1: # Removing non-breaking spaces
        MesTxt = MesTxt.replace("\xa0", " ")

    MesTxt = "".join(c for c in MesTxt if unicodedata.category(c) not in ["No"])

    pattern = r"(?<=\d),(?=\d{3})"
    MesTxt = re.sub(pattern, "", MesTxt) # 1,000,000 to 1000000

    for i in range(len(MesTxt) - 2):
        if MesTxt[i].isdigit() and MesTxt[i + 2].isdigit() and MesTxt[i + 1] == ",":
            MesTxt = MesTxt[0:i + 1] + "." + MesTxt[i + 2:len(MesTxt)] # comma to dot

    pattern = r"(?<!\d)(\d{1,3}(?: \d{3})*(?:\.\d+)?)(?=(?:\s\d{3})*(?:\.\d+)?|\D|$)"
    MesTxt = re.sub(pattern, RemoveSeparator, MesTxt) # 1 000 000 to 1000000

    return MesTxt

def SpecialSplit(MesTxt: str) -> list:
    a = [] #The main array to which the result will be written
    start = 0
    end = 0
    for i in range(len(MesTxt)):
        if MesTxt[i] == " ":
            end = i
            a.append(MesTxt[start:end])
            start = end + 1
        elif i == len(MesTxt) - 1:
            end = len(MesTxt)
            a.append(MesTxt[start:end])
        elif MesTxt[i].isalpha() and not MesTxt[i + 1].isalpha() and not MesTxt[i + 1].isdigit(): #separating letters from symbols
            end = i + 1
            a.append(MesTxt[start:end])
            start = end
        elif MesTxt[i + 1].isalpha() and not MesTxt[i].isalpha() and not MesTxt[i].isdigit(): #separating symbols from letters
            end = i + 1
            a.append(MesTxt[start:end])
            start = end
        elif not MesTxt[i].isalpha() and not MesTxt[i].isdigit() and not MesTxt[i + 1].isalpha() and not MesTxt[i + 1].isdigit(): #separating symbols from letters
            end = i + 1
            a.append(MesTxt[start:end])
            start = end
        elif MesTxt[i].isdigit() and not MesTxt[i + 1].isdigit() and MesTxt[i + 1] != " " and MesTxt[i + 1] != ".": #separating a digit from a letter
            end = i + 1
            a.append(MesTxt[start:end])
            start = end
        elif not MesTxt[i].isdigit() and MesTxt[i + 1].isdigit() and MesTxt[i] != " " and MesTxt[i] != ".": #separating a letter from a digit
            end = i + 1
            a.append(MesTxt[start:end])
            start = end
    b = []
    for i in a:
        if i != "":
            b.append(i)
    
    c = []
    for i in b:
        if i[0].isdigit() and i.count(".") >= 2:
            pass
        else:
            c.append(i)

    return c

def LoadCurrencies():
    ListsCache.SetListOfCur(GetListOfCurrencies())

def LoadCrypto():
    ListsCache.SetListOfCrypto(GetListOfCrypto())

def LoadFlags():
    EmptyDictOfFlags = {}
    ListsCache.SetDictOfFlags(GetDictOfFlags())
    DictOfFlags = ListsCache.GetDictOfFlags()
    for i in DictOfFlags:
        EmptyDictOfFlags[i] = ""
    ListsCache.SetEmptyDictOfFlags(EmptyDictOfFlags)

def LoadSymbols():
    File = open("Dictionaries/currencies.json", "r")
    Dic = json.load(File)
    Dic = Dic["currencies"]
    DictOfSymbols = {}
    for i in Dic:
        DictOfSymbols[i["code"]] = i["symbol_native"]
    ListsCache.SetDictOfSymbols(DictOfSymbols)
    EmptyDictOfSymbols = {}
    for i in DictOfSymbols:
        EmptyDictOfSymbols[i] = ""
    ListsCache.SetEmptyDictOfSymbols(EmptyDictOfSymbols)

def LoadDictionaries():
    global ListEntry, ListEqual, ListCryptoEntry, ListCryptoEqual

    File = open("Dictionaries/currencies.json", "r")
    Dic = json.load(File)
    Dic = Dic["currencies"]
    for i in Dic:
        ListEqual[i["code"]] = i["equal"]
        ListEntry[i["code"]] = []
        for j in i["entry"]:
            ListEntry[i["code"]] = ListEntry[i["code"]] + i["entry"][j]
        ListEntry[i["code"]] = list(dict.fromkeys(ListEntry[i["code"]]))
        while ListEqual[i["code"]].count("") != 0:
            ListEqual[i["code"]].remove("")
        while ListEntry[i["code"]].count("") != 0:
            ListEntry[i["code"]].remove("")

    FileCrypto = open("Dictionaries/crypto.json", "r")
    DicCrypto = json.load(FileCrypto)
    DicCrypto = DicCrypto["crypto"]
    for i in DicCrypto:
        ListCryptoEqual[i["code"]] = i["equal"]
        ListCryptoEntry[i["code"]] = []
        for j in i["entry"]:
            ListCryptoEntry[i["code"]] = ListCryptoEntry[i["code"]] + i["entry"][j]
        ListCryptoEntry[i["code"]] = list(dict.fromkeys(ListCryptoEntry[i["code"]]))
        while ListCryptoEqual[i["code"]].count("") != 0:
            ListCryptoEqual[i["code"]].remove("")
        while ListCryptoEntry[i["code"]].count("") != 0:
            ListCryptoEntry[i["code"]].remove("")
        

def SearchCurrency(cur: str) -> int:
    for i in ListEntry:
        for j in range(len(ListEntry[i])):
            if cur.find(' ') != -1:
                if cur.find(ListEntry[i][j]) == 0 and ListEntry[i] != [''] and ListEntry[i][j].find(' ') != -1:
                    return i
            elif cur.find(ListEntry[i][j]) == 0 and ListEntry[i] != ['']:
                return i
    for i in ListEqual:
        for j in range(len(ListEqual[i])):
            if cur == ListEqual[i][j]:
                return i
    return -1

def SearchCrypto(cur: str) -> int:
    for i in ListCryptoEntry:
        for j in range(len(ListCryptoEntry[i])):
            if cur.find(' ') != -1:
                if cur.find(ListCryptoEntry[i][j]) == 0 and ListCryptoEntry[i] != [''] and ListCryptoEntry[i][j].find(' ') != -1:
                    return i
            elif cur.find(ListCryptoEntry[i][j]) == 0 and ListCryptoEntry[i] != ['']:
                return i
    for i in ListCryptoEqual:
        for j in range(len(ListCryptoEqual[i])):
            if cur == ListCryptoEqual[i][j]:
                return i
    return -1

def SearchValuesAndCurrencies(arr: list) -> list:
    Values = [] #values of national currencies
    CurCodes = [] #numbers of national currencies
    CryptoValues = [] #values of cryptocurrencies
    CryptoCodes = [] #codes of cryptocurrencies
    i = 0
    j = 0

    # search for national currencies
    for u in range(len(arr)):
        # if it is a range of numbers
        if u <= len(arr) - 3 and arr[u][0].isdigit() and arr[u + 2][0].isdigit() and arr[u + 1] == "-":
            # two words in the name of the currency
            u += 2
            if u <= len(arr) - 3:
                curCode = SearchCurrency(arr[u + 1] + " " + arr[u + 2])
                if curCode != -1:
                    Values.append(arr[u])
                    CurCodes.append(curCode)
                    Values.append(arr[u - 2])
                    CurCodes.append(curCode)
            u -= 2
            if u >= 2: 
                curCode = SearchCurrency(arr[u - 2] + " " + arr[u - 1])
                if curCode != -1:
                    Values.append(arr[u])
                    CurCodes.append(curCode)
                    Values.append(arr[u + 2])
                    CurCodes.append(curCode)
            # one word in the name of the currency
            u += 2
            if u <= len(arr) - 2: 
                curCode = SearchCurrency(arr[u + 1])
                if curCode != -1:
                    Values.append(arr[u])
                    CurCodes.append(curCode)
                    Values.append(arr[u - 2])
                    CurCodes.append(curCode)
            u -= 2
            if u >= 1:
                curCode = SearchCurrency(arr[u - 1])
                if curCode != -1:
                    Values.append(arr[u])
                    CurCodes.append(curCode)
                    Values.append(arr[u + 2])
                    CurCodes.append(curCode)
            u += 2
        elif arr[u][0].isdigit():
            # two words in the name of the currency
            if u <= len(arr) - 3: 
                curCode = SearchCurrency(arr[u + 1] + " " + arr[u + 2])
                if curCode != -1:
                    Values.append(arr[u])
                    CurCodes.append(curCode)
            if u >= 2:
                curCode = SearchCurrency(arr[u - 2] + " " + arr[u - 1])
                if curCode != -1:
                    Values.append(arr[u])
                    CurCodes.append(curCode)
            # one word in the name of the currency
            if u <= len(arr) - 2:
                curCode = SearchCurrency(arr[u + 1])
                if curCode != -1:
                    Values.append(arr[u])
                    CurCodes.append(curCode)
            if u >= 1:
                curCode = SearchCurrency(arr[u - 1])
                if curCode != -1:
                    Values.append(arr[u])
                    CurCodes.append(curCode)

    # search for cryptocurrencies
    for u in range(len(arr)):
        # if it is a range of numbers
        if u <= len(arr) - 3 and arr[u][0].isdigit() and arr[u + 2][0].isdigit() and arr[u + 1] == "-":
            # two words in the name of the currency
            u += 2
            if u <= len(arr) - 3: 
                cryptoCode = SearchCrypto(arr[u + 1] + " " + arr[u + 2]) 
                if cryptoCode != -1:
                    CryptoValues.append(arr[u])
                    CryptoCodes.append(cryptoCode)
                    CryptoValues.append(arr[u - 2])
                    CryptoCodes.append(cryptoCode)
            u -= 2
            if u >= 2:
                cryptoCode = SearchCrypto(arr[u - 2] + " " + arr[u - 1])
                if cryptoCode != -1:
                    CryptoValues.append(arr[u])
                    CryptoCodes.append(cryptoCode)
                    CryptoValues.append(arr[u + 2])
                    CryptoCodes.append(cryptoCode)
            # one word in the name of the currency
            u += 2
            if u <= len(arr) - 2:
                cryptoCode = SearchCrypto(arr[u + 1])
                if cryptoCode != -1:
                    CryptoValues.append(arr[u])
                    CryptoCodes.append(cryptoCode)
                    CryptoValues.append(arr[u - 2])
                    CryptoCodes.append(cryptoCode)
            u -= 2
            if u >= 1:
                cryptoCode = SearchCrypto(arr[u - 1])
                if cryptoCode != -1:
                    CryptoValues.append(arr[u])
                    CryptoCodes.append(cryptoCode)
                    CryptoValues.append(arr[u + 2])
                    CryptoCodes.append(cryptoCode)
            u += 2
        elif arr[u][0].isdigit():
            # two words in the name of the currency
            if u <= len(arr) - 3:
                cryptoCode = SearchCrypto(arr[u + 1] + " " + arr[u + 2])
                if cryptoCode != -1:
                    CryptoValues.append(arr[u])
                    CryptoCodes.append(cryptoCode)
            if u >= 2:
                cryptoCode = SearchCrypto(arr[u - 2] + " " + arr[u - 1])
                if cryptoCode != -1:
                    CryptoValues.append(arr[u])
                    CryptoCodes.append(cryptoCode)
            # one word in the name of the currency
            if u <= len(arr) - 2:
                cryptoCode = SearchCrypto(arr[u + 1])
                if cryptoCode != -1:
                    CryptoValues.append(arr[u])
                    CryptoCodes.append(cryptoCode)
            if u >= 1:
                cryptoCode = SearchCrypto(arr[u - 1])
                if cryptoCode != -1:
                    CryptoValues.append(arr[u])
                    CryptoCodes.append(cryptoCode)

    answ_ar = [Values, CurCodes, CryptoValues, CryptoCodes]
    if len(answ_ar[0]) == 0 and len(answ_ar[2]) == 0:
        return answ_ar
    #remove duplicates
    temp_arr = answ_ar.copy()
    answ_ar = [[], [], [], []]
    for i in range(len(temp_arr[0])):
        if len(answ_ar[0]) == 0 and len(temp_arr[0]) != 0:
            answ_ar[0].append(temp_arr[0][i])
            answ_ar[1].append(temp_arr[1][i])
        flag = False
        for j in range(len(answ_ar[0])):
            if temp_arr[0][i] == answ_ar[0][j] and temp_arr[1][i] == answ_ar[1][j]:
                flag = True
                break
        if flag == False:
            answ_ar[0].append(temp_arr[0][i])
            answ_ar[1].append(temp_arr[1][i])
    for i in range(len(temp_arr[2])):
        if len(answ_ar[2]) == 0 and len(temp_arr[2]) != 0:
            answ_ar[2].append(temp_arr[2][i])
            answ_ar[3].append(temp_arr[3][i])
        flag = False
        for j in range(len(answ_ar[2])):
            if temp_arr[2][i] == answ_ar[2][j] and temp_arr[3][i] == answ_ar[3][j]:
                flag = True
                break
        if flag == False:
            answ_ar[2].append(temp_arr[2][i])
            answ_ar[3].append(temp_arr[3][i])

    #remove 0 values
    n = len(answ_ar[0])
    i = 0
    while i < n:
        if answ_ar[0][i] == '0' or answ_ar[0][i] == '0.0':
            answ_ar[0].pop(i)
            answ_ar[1].pop(i)
            n -= 1
            i -= 1
        i += 1
    n = len(answ_ar[2])
    i = 0
    while i < n:
        if answ_ar[2][i] == '0' or answ_ar[2][i] == '0.0':
            answ_ar[2].pop(i)
            answ_ar[3].pop(i)
            n -= 1
            i -= 1
        i += 1    

    for i in range(len(answ_ar[0])):
        answ_ar[0][i] = float(answ_ar[0][i])
    for i in range(len(answ_ar[2])):
        answ_ar[2][i] = float(answ_ar[2][i])
    return answ_ar

def RemoveIgnored(arr: list, chatID: str) -> list:
    IgnoredCurrencies = GetIgnoredCurrencies(chatID)
    newarr = [[], [], [], []]
    for i in range(len(arr[1])):
        if arr[1][i] in IgnoredCurrencies:
            pass
        else:
            newarr[0].append(arr[0][i])
            newarr[1].append(arr[1][i])
    for i in range(len(arr[3])):
        if arr[3][i] in IgnoredCurrencies:
            pass
        else:
            newarr[2].append(arr[2][i])
            newarr[3].append(arr[3][i])
    return newarr
    
def AnswerText(Arr: list, chatID: str, chatType: str) -> str:
    def TwoZeroesToOne(s: str):
        while s.rfind("00") == len(s) - 2:
            s = s[:-1]
        return s

    DictOfFlagsForChat = {}
    DictofSymbolsForChat = {}

    if GetSetting(chatID, "flags", chatType):
        DictOfFlagsForChat = ListsCache.GetDictOfFlags()
    else:
        DictOfFlagsForChat = ListsCache.GetEmptyDictOfFlags()

    if GetSetting(chatID, "currencySymbol", chatType):
        DictofSymbolsForChat = ListsCache.GetDictOfSymbols()
    else:
        DictofSymbolsForChat = ListsCache.GetEmptyDictOfSymbols()

    isCryptoLink = False

    answer = ''
    for i in range(len(Arr[1])): #National currencies
        CurVault = float(Arr[0][i])
        CurCurrency = Arr[1][i]
        answer += "\n" + "======" + "\n"
        PartOfAnswer = DictOfFlagsForChat[CurCurrency] + str(f'{CurVault:,.2f}'.replace(","," ")) + DictofSymbolsForChat[CurCurrency] + " " + CurCurrency + "\n"
        
        ListOfChatCurrencies = GetAllCurrencies(chatID)
        ListOfChatCrypto = GetAllCrypto(chatID)

        for j in ListOfChatCurrencies: #National currencies
            if CurCurrency == j:
                pass
            elif j == 'EUR':
                Vault = round(CurVault / GetExchangeRates.exchangeRates[CurCurrency], 2)
                Vault = f'{Vault:,.2f}'.replace(","," ")
                PartOfAnswer += "\n" + DictOfFlagsForChat[j] + str(Vault) + DictofSymbolsForChat[j] + " " + j
            elif j != 'EUR':
                Vault = round(CurVault * (GetExchangeRates.exchangeRates[j] / GetExchangeRates.exchangeRates[CurCurrency]), 2)
                Vault = f'{Vault:,.2f}'.replace(","," ")
                PartOfAnswer += "\n" + DictOfFlagsForChat[j] + str(Vault) + DictofSymbolsForChat[j] + " " + j
        if CurCurrency == 'UAH' and CurVault == 40.0:
            PartOfAnswer += "\n👖1 штани"
        elif CurCurrency == 'USD' and CurVault == 300.0:
            PartOfAnswer += "\n🤛1"

        if len(ListOfChatCurrencies) != 0:
            PartOfAnswer += "\n"
        
        for j in ListOfChatCrypto: #Crypto
            isCryptoLink = True
            if CurCurrency == 'EUR':
                Vault = round(CurVault / GetExchangeRates.exchangeRates[CurCurrency] / GetExchangeRates.cryptoRates[j], 9)
                Vault = f'{Vault:,.9f}'.replace(","," ")
                PartOfAnswer += "\n" + TwoZeroesToOne(str(Vault)) + " " + j
            elif CurCurrency != 'EUR':
                Vault = round(CurVault * (GetExchangeRates.exchangeRates['USD'] / GetExchangeRates.exchangeRates[CurCurrency] / GetExchangeRates.cryptoRates[j]), 9)
                Vault = f'{Vault:,.9f}'.replace(","," ")
                PartOfAnswer += "\n" + TwoZeroesToOne(str(Vault)) + " " + j
        answer += PartOfAnswer + "\n"

    for i in range(len(Arr[3])): #Crypto
        isCryptoLink = True
        answer += "\n" + "======" + "\n"
        CurVault = float(Arr[2][i])
        CurCurrency = Arr[3][i]
        PartOfAnswer = TwoZeroesToOne(str(f'{CurVault:,.9f}'.replace(","," "))) + " " + CurCurrency + "\n"

        ListOfChatCurrencies = GetAllCurrencies(chatID)
        ListOfChatCrypto = GetAllCrypto(chatID)
                
        for j in ListOfChatCurrencies: #National currencies
            if j == 'EUR':
                Vault = round(CurVault * 1 / GetExchangeRates.exchangeRates['USD'] * GetExchangeRates.cryptoRates[CurCurrency], 2)
                Vault = f'{Vault:,.2f}'.replace(","," ")
                PartOfAnswer += "\n" + DictOfFlagsForChat[j] + str(Vault) + " " + j
            elif j != 'EUR':
                Vault = round(CurVault * GetExchangeRates.exchangeRates[j] / GetExchangeRates.exchangeRates['USD'] * GetExchangeRates.cryptoRates[CurCurrency], 2)
                Vault = f'{Vault:,.2f}'.replace(","," ")
                PartOfAnswer += "\n" + DictOfFlagsForChat[j] + str(Vault) + " " + j

        if len(ListOfChatCurrencies) != 0:
            PartOfAnswer += "\n"
        
        for j in ListOfChatCrypto: #Crypto
            if CurCurrency == j:
                pass
            else:
                Vault = round(CurVault * GetExchangeRates.cryptoRates[CurCurrency] / GetExchangeRates.cryptoRates[j], 9)
                Vault = f'{Vault:,.9f}'.replace(","," ")
                PartOfAnswer += "\n" + TwoZeroesToOne(str(Vault)) + " " + j
        answer += PartOfAnswer + "\n"

    if True:
        answer += "\n" + GetText(chatID, 'Crypto', chatType)

    return answer

def UpdateUsingStats():
    return None