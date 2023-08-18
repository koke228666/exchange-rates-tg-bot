from ListsCache import GetTokensForW2N, GetExceptionsForW2N
from NewPrint import Print

#df = pd.read_excel('tokens.xlsx')
df = ""

def CheckExceptions(word: str):
    exceptions = GetExceptionsForW2N()
    for exception in exceptions:
        if word.find(exception) != -1:
            return True
    return False

def levenstein(str_1, str_2):
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

def stringDeviation(str_1, str_2):
    if str_1[0] != str_2[0] or CheckExceptions(str_2):
        return 1
    return levenstein(str_1, str_2)/len(str_1)

def wordsMatching(word, tokens):
    if word in tokens:
        return (word, 0.0)

    min_deviation = stringDeviation(tokens[0], word)
    fitting_token = tokens[0]

    for token in tokens[1:]:
        if stringDeviation(token, word) < min_deviation:
            min_deviation = stringDeviation(token, word)
            fitting_token = token
    return (fitting_token, min_deviation)

def IsWordNumber(word):
    global df
    df = GetTokensForW2N()
    tokenWord, errorValue = wordsMatching(word, df['token'])
    Print("Word: " + str(word) + " | Token: " + str(tokenWord) + " | Error: " + str(errorValue) + " | Coef: " + str(errorValue / len(word)), "L")
    if (errorValue / len(word) < 0.12 and errorValue < 0.5 and len(word) > 3 or errorValue < 0.3 and len(word) <= 3) or word[0].isdigit():
        return tokenWord
    return -1

def ConvertWordsToNumber(words):
    arr = []
    newWords = []
    for word in words:
        if IsWordNumber(word) != -1:
            arr.append(1)
            newWords.append(word)
        elif word == "-":
            if len(arr) > 0 and arr[-1] == 1 and not newWords[-1][0].isdigit():
                pass
            else:
                arr.append(0)
                newWords.append(word)
        else:
            arr.append(0)
            newWords.append(word)

    words = newWords
    
    while 1 in arr:
        startIndex = 0
        endIndex = 0
        for i in range(1, len(arr)):
            if i == len(arr) - 1 and arr[i] == 1 and arr[i - 1] == 0 or arr[i - 1] == 0 and arr[i + 1] == 0 and arr[i] == 1:
                startIndex = i
                endIndex = i + 1
                break
            if arr[i] == 1 and arr[i - 1] == 0:
                startIndex = i
            if arr[i] == 0 and arr[i - 1] == 1 or i == len(arr) - 1 and arr[i] == 1:
                endIndex = i
                break
        num = wordsToNumber(words[startIndex:endIndex])
        # replace words with number
        words[startIndex:endIndex] = [str(num)]
        # replace 1 with 0
        arr[startIndex:endIndex] = [0]
    return words


def wordsToNumber(words):
    global df
    globalLevel = -1
    localLevel = -1
    globalValue = 0
    localValue = 0
    
    for word in words:
        if word[0].isdigit() and word[-1].isdigit():
            globalLevel = -1
            localLevel = -1
            globalValue = 0
            localValue = 0
            localValue += float(word)
            continue

        if not df.loc[df['token'] == word].to_dict('records'):
            token, min_diviation = wordsMatching(word, df['token'])
            token_dict = df.loc[df['token'] == token].to_dict('records')[0]      
        else:
            token_dict = df.loc[df['token'] == word].to_dict('records')[0]
        
        if token_dict['isMultiplier']:
            if globalLevel == -1 or token_dict['level'] < globalLevel:
                globalLevel = token_dict['level']
                if localValue == 0:
                    localValue += token_dict['value']
                else:
                    localValue *= token_dict['value']
                globalValue += localValue
                localValue = 0
                localLevel = -1
            else:
                pass
        else:
            if localLevel == -1 or token_dict['level'] < localLevel:
                localLevel = token_dict['level']
                localValue += token_dict['value']
            else:
                pass

    return globalValue + localValue