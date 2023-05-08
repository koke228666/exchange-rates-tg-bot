from TextHelper import GetText
from NewPrint import Print
from DBH import GetAllCrypto, GetAllCurrencies, GetExchangeRates, GetListOfCrypto, GetListOfCurrencies, GetDictOfFlags, GetSetting
import GetExchangeRates
import ListsCache

ListEntry = []
ListEqual = []
ListCryptoEntry = []
ListCryptoEqual = []

_eng_chars = u"`qwertyuiop[]asdfghjkl;'zxcvbnm,.QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM,."
_rus_chars = u"ёйцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"
_ukr_chars = u"'йцукенгшщзхїфівапролджєячсмитьбюЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ"

def RemoveLinksAndWords(MesTxt: str) -> str:
    indexOfAtSign = -1
    indexOfSpace = -1
    while MesTxt.find("@") != -1:
        if MesTxt.find("@") != len(MesTxt) - 1:
            indexOfAtSign = MesTxt.find("@")
            indexOfSpace = MesTxt.find(" ", indexOfAtSign)
            MesTxt = MesTxt[0:indexOfAtSign] + MesTxt[indexOfSpace:]
        else:
            MesTxt = MesTxt[0:-1]

    while MesTxt.find("http") != -1:
        if MesTxt.find("@") != len(MesTxt) - 1:
            indexOfAtSign = MesTxt.find("http")
            indexOfSpace = MesTxt.find(" ", indexOfAtSign)
            MesTxt = MesTxt[0:indexOfAtSign] + MesTxt[indexOfSpace:]
        else:
            MesTxt = MesTxt[0:-1]

    return MesTxt

def SpecialSplit(MesTxt: str) -> list:
    MesTxt = MesTxt.replace("\n", " , ") # Replace hyphenation with dot

    while MesTxt.find("  ") != -1: # Removing double spaces
        MesTxt = MesTxt.replace("  ", " ")

    while MesTxt.find("'") != -1: # Removing apostrophes
        MesTxt = MesTxt.replace("'", "")

    for i in range(len(MesTxt) - 2):
        if MesTxt[i].isdigit() and MesTxt[i + 2].isdigit() and MesTxt[i + 1] == ",":
            MesTxt = MesTxt[0:i + 1] + "." + MesTxt[i + 2:len(MesTxt)] # comma to dot

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
    
    for i in range(len(b)):
        if b[i][0].isdigit() and b[i].count(".") >= 2:
            while b[i].find(".") != -1:
                b[i] = b[i].replace(".", "")

    return b

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

def LoadDictionaries():
    global ListEntry, ListEqual, ListCryptoEntry, ListCryptoEqual

    DicEntry = open("Dictionaries/CurEntry.txt", "r")
    ListEntry = DicEntry.readlines()
    DicEntry.close()
    for i in range(len(ListEntry)):
        if ListEntry[i].find(","):
            ListEntry[i] = ListEntry[i].split(",")
        elif ListEntry == "":
            ListEntry[i] = []
        else:
            ListEntry[i] = [ListEntry[i]]
        ListEntry[i][len(ListEntry[i]) - 1] = ListEntry[i][len(ListEntry[i]) - 1].replace("\n", "")
    for i in range(len(ListEntry)):
        if ListEntry[i] == ['']:
            pass
        else:
            for j in range(len(ListEntry[i])):
                word = ListEntry[i][j]
                if word[0] in _eng_chars:
                    newRUword = ''
                    newUAword = ''
                    for k in range(len(word)):
                        index = _eng_chars.find(word[k])
                        newRUword += _rus_chars[index]
                        newUAword += _ukr_chars[index]
                    if newRUword not in ListEntry[i]:
                        ListEntry[i].append(newRUword)
                    if newUAword not in ListEntry[i]:
                        ListEntry[i].append(newUAword)
                elif word[0] in _rus_chars:
                    newENword = ''
                    newUAword = ''
                    for k in range(len(word)):
                        index = _rus_chars.find(word[k])
                        newENword += _eng_chars[index]
                        newUAword += _ukr_chars[index]
                    if newENword not in ListEntry[i]:
                        ListEntry[i].append(newENword)
                    if newUAword not in ListEntry[i]:
                        ListEntry[i].append(newUAword)
                elif word[0] in _ukr_chars:
                    newENword = ''
                    newRUword = ''
                    for k in range(len(word)):
                        index = _ukr_chars.find(word[k])
                        newENword += _eng_chars[index]
                        newRUword += _rus_chars[index]
                    if newENword not in ListEntry[i]:
                        ListEntry[i].append(newENword)
                    if newRUword not in ListEntry[i]:    
                        ListEntry[i].append(newRUword)

    DicEqual = open("Dictionaries/CurEqual.txt", "r")
    ListEqual = DicEqual.readlines()
    DicEqual.close()
    for i in range(len(ListEqual)):
        if ListEqual[i].find(","):
            ListEqual[i] = ListEqual[i].split(",")
        elif ListEqual == "":
            ListEqual[i] = []
        else:
            ListEqual[i] = [ListEqual[i]]
        ListEqual[i][len(ListEqual[i]) - 1] = ListEqual[i][len(ListEqual[i]) - 1].replace("\n", "")

    DicCryptoEntry = open("Dictionaries/CryptoEntry.txt", "r")
    ListCryptoEntry = DicCryptoEntry.readlines()
    DicCryptoEntry.close()
    for i in range(len(ListCryptoEntry)):
        if ListCryptoEntry[i].find(","):
            ListCryptoEntry[i] = ListCryptoEntry[i].split(",")
        elif ListCryptoEntry == "":
            ListCryptoEntry[i] = []
        else:
            ListCryptoEntry[i] = [ListCryptoEntry[i]]
        ListCryptoEntry[i][len(ListCryptoEntry[i]) - 1] = ListCryptoEntry[i][len(ListCryptoEntry[i]) - 1].replace("\n", "")
    for i in range(len(ListCryptoEntry)):
        if ListCryptoEntry[i] == ['']:
            pass
        else:
            for j in range(len(ListCryptoEntry[i])):
                word = ListCryptoEntry[i][j]
                if word[0] in _eng_chars:
                    newRUword = ''
                    newUAword = ''
                    for k in range(len(word)):
                        index = _eng_chars.find(word[k])
                        newRUword += _rus_chars[index]
                        newUAword += _ukr_chars[index]
                    if newRUword not in ListCryptoEntry[i]:
                        ListCryptoEntry[i].append(newRUword)
                    if newUAword not in ListCryptoEntry[i]:
                        ListCryptoEntry[i].append(newUAword)
                elif word[0] in _rus_chars:
                    newENword = ''
                    newUAword = ''
                    for k in range(len(word)):
                        index = _rus_chars.find(word[k])
                        newENword += _eng_chars[index]
                        newUAword += _ukr_chars[index]
                    if newENword not in ListCryptoEntry[i]:
                        ListCryptoEntry[i].append(newENword)
                    if newUAword not in ListCryptoEntry[i]:
                        ListCryptoEntry[i].append(newUAword)
                elif word[0] in _ukr_chars:
                    newENword = ''
                    newRUword = ''
                    for k in range(len(word)):
                        index = _ukr_chars.find(word[k])
                        newENword += _eng_chars[index]
                        newRUword += _rus_chars[index]
                    if newENword not in ListCryptoEntry[i]:
                        ListCryptoEntry[i].append(newENword)
                    if newRUword not in ListCryptoEntry[i]:    
                        ListCryptoEntry[i].append(newRUword)

    DicCryptoEqual = open("Dictionaries/CryptoEqual.txt", "r")
    ListCryptoEqual = DicCryptoEqual.readlines()
    DicCryptoEqual.close()
    for i in range(len(ListCryptoEqual)):
        if ListCryptoEqual[i].find(","):
            ListCryptoEqual[i] = ListCryptoEqual[i].split(",")
        elif ListCryptoEqual == "":
            ListCryptoEqual[i] = []
        else:
            ListCryptoEqual[i] = [ListCryptoEqual[i]]
        ListCryptoEqual[i][len(ListCryptoEqual[i]) - 1] = ListCryptoEqual[i][len(ListCryptoEqual[i]) - 1].replace("\n", "")
    for i in range(len(ListCryptoEqual)):
        if ListCryptoEqual[i] == ['']:
            pass
        else:
            for j in range(len(ListCryptoEqual[i])):
                word = ListCryptoEqual[i][j]
                if word[0] in _eng_chars:
                    newRUword = ''
                    newUAword = ''
                    for k in range(len(word)):
                        index = _eng_chars.find(word[k])
                        newRUword += _rus_chars[index]
                        newUAword += _ukr_chars[index]
                    if newRUword not in ListCryptoEqual[i]:
                        ListCryptoEqual[i].append(newRUword)
                    if newUAword not in ListCryptoEqual[i]:
                        ListCryptoEqual[i].append(newUAword)
                elif word[0] in _rus_chars:
                    newENword = ''
                    newUAword = ''
                    for k in range(len(word)):
                        index = _rus_chars.find(word[k])
                        newENword += _eng_chars[index]
                        newUAword += _ukr_chars[index]
                    if newENword not in ListCryptoEqual[i]:
                        ListCryptoEqual[i].append(newENword)
                    if newUAword not in ListCryptoEqual[i]:
                        ListCryptoEqual[i].append(newUAword)
                elif word[0] in _ukr_chars:
                    newENword = ''
                    newRUword = ''
                    for k in range(len(word)):
                        index = _ukr_chars.find(word[k])
                        newENword += _eng_chars[index]
                        newRUword += _rus_chars[index]
                    if newENword not in ListCryptoEqual[i]:
                        ListCryptoEqual[i].append(newENword)
                    if newRUword not in ListCryptoEqual[i]:    
                        ListCryptoEqual[i].append(newRUword)

def SearchValuesAndCurrencies(arr: list) -> list:
    Values = [] #values of national currencies
    CurNumber = [] #numbers of national currencies
    CryptoValues = [] #values of cryptocurrencies
    CryptoNumber = [] #numbers of cryptocurrencies
    i = 0
    j = 0
    while i < len(ListEntry):
        while j < len(ListEntry[i]):
            for u in range(len(arr)):
                # if it is a range of numbers
                if u <= len(arr) - 3 and arr[u][0].isdigit and arr[u + 2][0].isdigit and arr[u + 1] == "-":
                    # two words in the name of the currency
                    u += 2
                    if u <= len(arr) - 3 and (arr[u + 1] + " " + arr[u + 2]).find(ListEntry[i][j]) == 0 and ListEntry[i] != [''] and ListEntry[i][j].find(' ') != -1:
                        Values.append(arr[u])
                        CurNumber.append(i)
                        Values.append(arr[u - 2])
                        CurNumber.append(i)
                    u -= 2
                    if u >= 2 and (arr[u - 2] + " " + arr[u - 1]).find(ListEntry[i][j]) == 0 and ListEntry[i] != [''] and ListEntry[i][j].find(' ') != -1:
                        Values.append(arr[u])
                        CurNumber.append(i)
                        Values.append(arr[u + 2])
                        CurNumber.append(i)
                    # one word in the name of the currency
                    u += 2
                    if u <= len(arr) - 2 and arr[u + 1].find(ListEntry[i][j]) == 0 and ListEntry[i] != ['']:
                        Values.append(arr[u])
                        CurNumber.append(i)
                        Values.append(arr[u - 2])
                        CurNumber.append(i)
                    u -= 2
                    if u >= 1 and arr[u - 1].find(ListEntry[i][j]) == 0 and ListEntry[i] != ['']:
                        Values.append(arr[u])
                        CurNumber.append(i)
                        Values.append(arr[u + 2])
                        CurNumber.append(i)
                    u += 2
                elif arr[u][0].isdigit:
                    # two words in the name of the currency
                    if u <= len(arr) - 3 and (arr[u + 1] + " " + arr[u + 2]).find(ListEntry[i][j]) == 0 and ListEntry[i] != [''] and ListEntry[i][j].find(' ') != -1:
                        Values.append(arr[u])
                        CurNumber.append(i)
                    if u >= 2 and (arr[u - 2] + " " + arr[u - 1]).find(ListEntry[i][j]) == 0 and ListEntry[i] != [''] and ListEntry[i][j].find(' ') != -1:
                        Values.append(arr[u])
                        CurNumber.append(i)
                    # one word in the name of the currency
                    if u <= len(arr) - 2 and arr[u + 1].find(ListEntry[i][j]) == 0 and ListEntry[i] != ['']:
                        Values.append(arr[u])
                        CurNumber.append(i)
                    if u >= 1 and arr[u - 1].find(ListEntry[i][j]) == 0 and ListEntry[i] != ['']:
                        Values.append(arr[u])
                        CurNumber.append(i)
            j += 1
        i += 1
        j = 0
    i = 0
    j = 0
    while i < len(ListEqual):
        while j < len(ListEqual[i]):
            for u in range(len(arr)):
                # if it is a range of numbers
                if u <= len(arr) - 3 and arr[u][0].isdigit and arr[u + 2][0].isdigit and arr[u + 1] == "-":
                    u += 2
                    if u <= len(arr) - 2 and arr[u + 1] == ListEqual[i][j]:
                        Values.append(arr[u])
                        CurNumber.append(i)
                        Values.append(arr[u - 2])
                        CurNumber.append(i)
                    u -= 2
                    if u >= 1 and arr[u - 1] == ListEqual[i][j]:
                        Values.append(arr[u])
                        CurNumber.append(i)
                        Values.append(arr[u + 2])
                        CurNumber.append(i)
                    u += 2
                elif arr[u][0].isdigit:
                    # one word in the name of the currency
                    if u <= len(arr) - 2 and arr[u + 1] == ListEqual[i][j]:
                        Values.append(arr[u])
                        CurNumber.append(i)
                    if u >= 1 and arr[u - 1] == ListEqual[i][j]:
                        Values.append(arr[u])
                        CurNumber.append(i)
            j += 1
        i += 1
        j = 0
    i = 0
    j = 0
    while i < len(ListCryptoEntry):
        while j < len(ListCryptoEntry[i]):
            for u in range(len(arr)):
                if arr[u].find(ListCryptoEntry[i][j]) == 0 and ListCryptoEntry[i] != ['']:
                    if u != len(arr) - 1 and u != 0:
                        if arr[u + 1][0].isdigit():
                            CryptoValues.append(arr[u + 1])
                            CryptoNumber.append(i)
                        elif arr[u - 1][0].isdigit():
                            CryptoValues.append(arr[u - 1])
                            CryptoNumber.append(i)
                    elif u == len(arr) - 1 and arr[u - 1][0].isdigit():
                        CryptoValues.append(arr[u - 1])
                        CryptoNumber.append(i)
                    elif u == 0 and arr[u + 1][0].isdigit():
                        CryptoValues.append(arr[u + 1])
                        CryptoNumber.append(i)
            j += 1
        i += 1
        j = 0
    i = 0
    j = 0
    while i < len(ListCryptoEqual):
        while j < len(ListCryptoEqual[i]):
            for u in range(len(arr)):
                if arr[u] == ListCryptoEqual[i][j]:
                    if u != len(arr) - 1 and u != 0:
                        if arr[u + 1][0].isdigit():
                            #Indexes.append(u)
                            CryptoValues.append(arr[u + 1])
                            CryptoNumber.append(i)
                        elif arr[u - 1][0].isdigit():
                            #Indexes.append(u)
                            CryptoValues.append(arr[u - 1])
                            CryptoNumber.append(i)
                    elif u == len(arr) - 1 and arr[u - 1][0].isdigit():
                        #Indexes.append(u)
                        CryptoValues.append(arr[u - 1])
                        CryptoNumber.append(i)
                    elif u == 0 and arr[u + 1][0].isdigit():
                        #Indexes.append(u)
                        CryptoValues.append(arr[u + 1])
                        CryptoNumber.append(i)
            j += 1
        i += 1
        j = 0
    answ_ar = [Values, CurNumber, CryptoValues, CryptoNumber]
    #remove duplicates
    n = len(answ_ar[0])
    i = 0
    while i < n:
        for j in range(len(answ_ar[0])):
            if answ_ar[1][i] == answ_ar[1][j] and answ_ar[0][i] == answ_ar[0][j] and j != i:
                answ_ar[0].pop(j)
                answ_ar[1].pop(j)
                j -= 1
                n -= 1
                break
        i += 1
    n = len(answ_ar[2])
    i = 0
    while i < n:
        for j in range(len(answ_ar[2])):
            if answ_ar[3][i] == answ_ar[3][j] and answ_ar[2][i] == answ_ar[2][j] and j != i:
                answ_ar[2].pop(j)
                answ_ar[3].pop(j)
                j -= 1
                n -= 1
                break
        i += 1
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
    return answ_ar
    
def AnswerText(Arr: list, chatID: str, chatType: str) -> str:
    def TwoZeroesToOne(s: str):
        while s.rfind("00") == len(s) - 2:
            s = s[:-1]
        return s

    DictOfFlagsForChat = {}

    if GetSetting(chatID, "flags", chatType):
        DictOfFlagsForChat = ListsCache.GetDictOfFlags()
    else:
        DictOfFlagsForChat = ListsCache.GetEmptyDictOfFlags()

    isCryptoLink = False

    answer = ''
    for i in range(len(Arr[1])): #Проходимся по всем распознаным классическим валютам
        CurVault = float(Arr[0][i])
        CurCurrency = ListsCache.GetListOfCur()[Arr[1][i]]
        answer += "\n" + "======" + "\n"
        PartOfAnswer = DictOfFlagsForChat[CurCurrency] + str(f'{CurVault:,.2f}'.replace(","," ")) + " " + CurCurrency + "\n"

        ListOfChatCurrencies = GetAllCurrencies(chatID)
        ListOfChatCrypto = GetAllCrypto(chatID)
        for j in ListOfChatCurrencies: #Проходимся по всем классическим валютам
            if CurCurrency == j:
                pass
            elif j == 'EUR':
                Vault = round(CurVault / GetExchangeRates.exchangeRates[CurCurrency], 2)
                Vault = f'{Vault:,.2f}'.replace(","," ")
                PartOfAnswer += "\n" + DictOfFlagsForChat[j] + str(Vault) + " " + j
            elif j != 'EUR':
                Vault = round(CurVault * (GetExchangeRates.exchangeRates[j] / GetExchangeRates.exchangeRates[CurCurrency]), 2)
                Vault = f'{Vault:,.2f}'.replace(","," ")
                PartOfAnswer += "\n" + DictOfFlagsForChat[j] + str(Vault) + " " + j
        if CurCurrency == 'UAH' and CurVault == 40.0:
            PartOfAnswer += "\n👖1 штаны"
        elif CurCurrency == 'USD' and CurVault == 300.0:
            PartOfAnswer += "\n🤛1"

        if len(ListOfChatCurrencies) != 0:
            PartOfAnswer += "\n"
        
        for j in ListOfChatCrypto: #Проходимся по всем криптовалютам
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

    for i in range(len(Arr[3])): #Проходимся по всем распознаным криптовалютам
        isCryptoLink = True
        answer += "\n" + "======" + "\n"
        CurVault = float(Arr[2][i])
        CurCurrency = ListsCache.GetListOfCrypto()[Arr[3][i]]
        PartOfAnswer = TwoZeroesToOne(str(f'{CurVault:,.9f}'.replace(","," "))) + " " + CurCurrency + "\n"

        ListOfChatCurrencies = GetAllCurrencies(chatID)
        ListOfChatCrypto = GetAllCrypto(chatID)
        for j in ListOfChatCurrencies: #Проходимся по всем классическим валютам
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
        
        for j in ListOfChatCrypto: #Проходимся по всем криптовалютам
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