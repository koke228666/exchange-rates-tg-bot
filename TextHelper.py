from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

import DBH
import ListsCache
import os
import json
from NewPrint import Print

AllBigTexts = {}
ButtonTexts = {}
MessageTexts = {}
ListOfNamesOfTextForBigTexts = []

def LoadTexts():
    global AllBigTexts
    global ListOfNamesOfTextForBigTexts
    try:
        listFiles = os.listdir("Texts")
        langs = []
        for i in listFiles:
            if i[0:2] not in langs:
                langs.append(i[0:2].lower())
                AllBigTexts[i[0:2].lower()] = {}
        for i in listFiles:
            fileWithText = open("Texts/" + i)
            fileText = fileWithText.read()
            fileWithText.close()
            nameOfText = i[2:-4]
            if nameOfText not in ListOfNamesOfTextForBigTexts:
                ListOfNamesOfTextForBigTexts.append(nameOfText)
            if i[0:2].lower() in AllBigTexts:
                AllBigTexts[i[0:2].lower()][nameOfText] = fileText
    except:
        Print("Problem with Texts. Redownload, pls.", "E")

    global MessageTexts
    fileWithTextsForButtons = open("Dictionaries/messages_texts.csv")
    lines = fileWithTextsForButtons.readlines()
    for i in range(0, len(lines)):
        lines[i] = lines[i].replace("\n", "")
    langs = lines[0].split(";")
    langs.pop(0)
    for i in langs:
        MessageTexts[i] = {}
    for i in lines[1:]:
        line = i.split(";")
        for j in range(0, len(langs)):
            MessageTexts[langs[j]][line[0]] = line[j+1]
    fileWithTextsForButtons.close()

    global ButtonTexts
    fileWithTextsForButtons = open("Dictionaries/buttons.csv")
    lines = fileWithTextsForButtons.readlines()
    for i in range(0, len(lines)):
        lines[i] = lines[i].replace("\n", "")
    langs = lines[0].split(";")
    langs.pop(0)
    for i in langs:
        ButtonTexts[i] = {}
    for i in lines[1:]:
        line = i.split(";")
        for j in range(0, len(langs)):
            ButtonTexts[langs[j]][line[0]] = line[j+1]
    fileWithTextsForButtons.close()

def DonateMarkup(chatID: str, chatType: str) -> InlineKeyboardMarkup:
    lang = DBH.GetSetting(chatID, "lang", chatType)
    isDeleteButton = DBH.GetSetting(chatID, "deleteButton", chatType)
    dictLang = ButtonTexts[lang]
    DonateMU = InlineKeyboardMarkup()
    DonateMU.add(InlineKeyboardButton(dictLang['donate'], url="https://secure.wayforpay.com/donate/d92c340414735", callback_data="donate"))
    # if isDeleteButton:
    #     DonateMU.add(InlineKeyboardButton(dictLang['delete'], callback_data = "delete"))
    return DonateMU

def DeleteMarkup(chatID: str, chatType: str) -> InlineKeyboardMarkup:
    isDeleteButton = DBH.GetSetting(chatID, "deleteButton", chatType)
    DeleteMU = InlineKeyboardMarkup()
    if isDeleteButton:
        lang = DBH.GetSetting(chatID, "lang", chatType)
        dictLang = ButtonTexts[lang]
        DeleteMU.add(InlineKeyboardButton(dictLang['delete'], callback_data = "delete"))
    return DeleteMU

def SettingsMarkup(chatID: str, chatType: str) -> InlineKeyboardMarkup:
    lang = DBH.GetSetting(chatID, "lang", chatType)
    isDeleteButton = DBH.GetSetting(chatID, "deleteButton", chatType)
    dictLang = ButtonTexts[lang]
    SettingsMU = InlineKeyboardMarkup()
    SettingsMU.add(InlineKeyboardButton(dictLang['lang'], callback_data = "lang_menu"))
    SettingsMU.add(InlineKeyboardButton(dictLang['currencies'], callback_data = "cur_menu"))
    SettingsMU.add(InlineKeyboardButton(dictLang['ignore'], callback_data = "cur_ignore_menu"))
    SettingsMU.add(InlineKeyboardButton(dictLang['delete_button'], callback_data = "delbut_menu"))
    SettingsMU.add(InlineKeyboardButton(dictLang['mes_view'], callback_data = "ui_menu"))
    if chatType != "private":
        SettingsMU.add(InlineKeyboardButton(dictLang['permisssions'], callback_data = "edit_menu"))
    if isDeleteButton:
        SettingsMU.add(InlineKeyboardButton(dictLang['delete'], callback_data = "delete"))
    return SettingsMU

def DeleteButtonMenuMarkup(chatID: str, chatType: str) -> InlineKeyboardMarkup:
    def RulesMark(role: str, answDict) -> str:
        if answDict['deleteRules'] == role:
            return " ✅"
        else:
            return " ❌"
    
    lang = DBH.GetSetting(chatID, "lang", chatType)
    AllSettings = DBH.GetAllSettings(chatID, chatType)
    dictLang = ButtonTexts[lang]
    DeleteButtonMenuMU = InlineKeyboardMarkup()
    if AllSettings['deleteButton']:
        DeleteButtonMenuMU.add(InlineKeyboardButton(dictLang['delbutton'] + " ✅", callback_data = "delbut_button"))
        if chatType != "private":
            DeleteButtonMenuMU.add(InlineKeyboardButton(dictLang['creator'] + RulesMark('creator', AllSettings), callback_data = "delbut_creator"))
            DeleteButtonMenuMU.add(InlineKeyboardButton(dictLang['admins'] + RulesMark('admins', AllSettings), callback_data = "delbut_admins"))
            DeleteButtonMenuMU.add(InlineKeyboardButton(dictLang['everybody'] + RulesMark('everybody', AllSettings), callback_data = "delbut_everybody"))
    else:
        DeleteButtonMenuMU.add(InlineKeyboardButton(dictLang['delbutton'] + " ❌", callback_data = "delbut_button"))
    DeleteButtonMenuMU.add(InlineKeyboardButton(dictLang['back'], callback_data = "settings"))
    return DeleteButtonMenuMU

def LanguageMenuMarkup(chatID: str, chatType: str):
    def RulesMark(lang: str, answDict) -> str:
        if answDict['lang'] == lang:
            return " ✅"
        else:
            return " ❌"
    
    #open json
    langs = []
    with open("Dictionaries/langs.json", "r", encoding="utf-8") as file:
        langs = json.load(file)
    langs = langs['langs']

    lang = DBH.GetSetting(chatID, "lang", chatType)
    AllSettings = DBH.GetAllSettings(chatID, chatType)
    dictLang = ButtonTexts[lang]
    LanguageMenuMU = InlineKeyboardMarkup()
    for i in langs:
        if i["active"]:
            LanguageMenuMU.add(InlineKeyboardButton(i['interface'] + RulesMark(i['botCode'], AllSettings), callback_data = "lang_" + i['botCode']))
    LanguageMenuMU.add(InlineKeyboardButton(dictLang['back'], callback_data = "settings"))
    return LanguageMenuMU

def MessageViewMarkup(chatID: str, chatType: str) -> InlineKeyboardMarkup:
    lang = DBH.GetSetting(chatID, "lang", chatType)
    AllSettings = DBH.GetAllSettings(chatID, chatType)
    dictLang = ButtonTexts[lang]
    MessageViewMU = InlineKeyboardMarkup()
    if AllSettings['flags']:
        MessageViewMU.add(InlineKeyboardButton(dictLang['flags_button'] + " ✅", callback_data = "ui_flags"))
    else:
        MessageViewMU.add(InlineKeyboardButton(dictLang['flags_button'] + " ❌", callback_data = "ui_flags"))
    if AllSettings['currencySymbol']:
        MessageViewMU.add(InlineKeyboardButton(dictLang['symbols_button'] + " ✅", callback_data = "ui_symbols"))
    else:
        MessageViewMU.add(InlineKeyboardButton(dictLang['symbols_button'] + " ❌", callback_data = "ui_symbols"))
    MessageViewMU.add(InlineKeyboardButton(dictLang['back'], callback_data = "settings"))
    return MessageViewMU

def EditMenuMarkup(chatID: str, chatType: str) -> InlineKeyboardMarkup:
    def RulesMark(role: str, answDict) -> str:
        if answDict['editSettings'] == role:
            return " ✅"
        else:
            return " ❌"
    
    lang = DBH.GetSetting(chatID, "lang", chatType)
    AllSettings = DBH.GetAllSettings(chatID, chatType)
    dictLang = ButtonTexts[lang]
    EditMenuMU = InlineKeyboardMarkup()
    EditMenuMU.add(InlineKeyboardButton(dictLang['creator'] + RulesMark('creator', AllSettings), callback_data = "edit_creator"))
    EditMenuMU.add(InlineKeyboardButton(dictLang['admins'] + RulesMark('admins', AllSettings), callback_data = "edit_admins"))
    EditMenuMU.add(InlineKeyboardButton(dictLang['everybody'] + RulesMark('everybody', AllSettings), callback_data = "edit_everybody"))
    EditMenuMU.add(InlineKeyboardButton(dictLang['back'], callback_data = "settings"))
    return EditMenuMU

def CurrenciesMainMenuMarkup(chatID: str, chatType: str) -> InlineKeyboardMarkup:
    lang = DBH.GetSetting(chatID, "lang", chatType)
    dictLang = ButtonTexts[lang]
    CurrenciesMainMenuMU = InlineKeyboardMarkup()
    CurrenciesMainMenuMU.add(InlineKeyboardButton(dictLang['cur_menu'], callback_data = "cur_curmenu"))
    CurrenciesMainMenuMU.add(InlineKeyboardButton(dictLang['crypto_menu'], callback_data = "cur_cryptomenu"))
    CurrenciesMainMenuMU.add(InlineKeyboardButton(dictLang['back'], callback_data = "settings"))
    return CurrenciesMainMenuMU

def CryptoMenuMarkup(chatID: str, chatType: str) -> InlineKeyboardMarkup:
    lang = DBH.GetSetting(chatID, "lang", chatType)
    dictLang = ButtonTexts[lang]
    CryptoMenuMU = InlineKeyboardMarkup()
    AllCrypto = ListsCache.GetListOfCrypto()
    TurnedOnCrypto = DBH.GetAllCrypto(chatID)
    for i in AllCrypto:
        if i in TurnedOnCrypto:
            CryptoMenuMU.add(InlineKeyboardButton(i + " ✅", callback_data = "cur_" + i))
        else:
            CryptoMenuMU.add(InlineKeyboardButton(i + " ❌", callback_data = "cur_" + i))
    CryptoMenuMU.add(InlineKeyboardButton(dictLang['back'], callback_data = "cur_menu"))
    return CryptoMenuMU

def CurrenciesMenuMarkup(chatID: str, chatType: str) -> InlineKeyboardMarkup:
    lang = DBH.GetSetting(chatID, "lang", chatType)
    dictLang = ButtonTexts[lang]
    CurrenciesMenuMU = InlineKeyboardMarkup()
    CurrenciesMenuMU.add(InlineKeyboardButton("A", callback_data = "cur_a"))
    CurrenciesMenuMU.add(InlineKeyboardButton("B", callback_data = "cur_b"))
    CurrenciesMenuMU.add(InlineKeyboardButton("C", callback_data = "cur_c"))
    CurrenciesMenuMU.add(InlineKeyboardButton("D-F", callback_data = "cur_df"))
    CurrenciesMenuMU.add(InlineKeyboardButton("G-H", callback_data = "cur_gh"))
    CurrenciesMenuMU.add(InlineKeyboardButton("I-J", callback_data = "cur_ij"))
    CurrenciesMenuMU.add(InlineKeyboardButton("K-L", callback_data = "cur_kl"))
    CurrenciesMenuMU.add(InlineKeyboardButton("M", callback_data = "cur_m"))
    CurrenciesMenuMU.add(InlineKeyboardButton("N-Q", callback_data = "cur_nq"))
    CurrenciesMenuMU.add(InlineKeyboardButton("R-S", callback_data = "cur_rs"))
    CurrenciesMenuMU.add(InlineKeyboardButton("T-U", callback_data = "cur_tu"))
    CurrenciesMenuMU.add(InlineKeyboardButton("V-Z", callback_data = "cur_vz"))
    CurrenciesMenuMU.add(InlineKeyboardButton(dictLang['back'], callback_data = "cur_menu"))
    return CurrenciesMenuMU

def CurrenciesSetupMarkup(chatID: str, chatType: str, letter: str) -> InlineKeyboardMarkup:
    lang = DBH.GetSetting(chatID, "lang", chatType)
    dictLang = ButtonTexts[lang]
    AllCurrencies = ListsCache.GetListOfCur()
    TurnedOnCurrencies = DBH.GetAllCurrencies(chatID)
    AllFlags = ListsCache.GetDictOfFlags()
    CurrenciesSetupMU = InlineKeyboardMarkup()
    if len(letter) == 1:
        letter = letter.upper()
        for i in AllCurrencies:
            if i[0] == letter:
                if i in TurnedOnCurrencies:
                    CurrenciesSetupMU.add(InlineKeyboardButton(AllFlags[i] + i + " ✅", callback_data = "cur_" + i))
                else:
                    CurrenciesSetupMU.add(InlineKeyboardButton(AllFlags[i] + i + " ❌", callback_data = "cur_" + i))
    else:
        firstLetter = ord(letter[0].upper())
        lastLetter = ord(letter[1].upper())
        listOfLetters = []
        while firstLetter <= lastLetter:
            listOfLetters.append(chr(firstLetter))
            firstLetter += 1
        for i in AllCurrencies:
            if i[0] in listOfLetters:
                if i in TurnedOnCurrencies:
                    CurrenciesSetupMU.add(InlineKeyboardButton(AllFlags[i] + i + " ✅", callback_data = "cur_" + i))
                else:
                    CurrenciesSetupMU.add(InlineKeyboardButton(AllFlags[i] + i + " ❌", callback_data = "cur_" + i))
    CurrenciesSetupMU.add(InlineKeyboardButton(dictLang['back'], callback_data = "cur_curmenu"))
    return CurrenciesSetupMU

def IgnoreCurrenciesMainMenuMarkup(chatID: str, chatType: str) -> InlineKeyboardMarkup:
    lang = DBH.GetSetting(chatID, "lang", chatType)
    dictLang = ButtonTexts[lang]
    IgnoreCurrenciesMainMenuMU = InlineKeyboardMarkup()
    IgnoreCurrenciesMainMenuMU.add(InlineKeyboardButton(dictLang['cur_menu'], callback_data = "cur_ignore_curmenu"))
    IgnoreCurrenciesMainMenuMU.add(InlineKeyboardButton(dictLang['crypto_menu'], callback_data = "cur_ignore_cryptomenu"))
    IgnoreCurrenciesMainMenuMU.add(InlineKeyboardButton(dictLang['back'], callback_data = "settings"))
    return IgnoreCurrenciesMainMenuMU

def IgnoreCryptoMenuMarkup(chatID: str, chatType: str) -> InlineKeyboardMarkup:
    lang = DBH.GetSetting(chatID, "lang", chatType)
    dictLang = ButtonTexts[lang]
    IgnoreCryptoMenuMU = InlineKeyboardMarkup()
    AllCrypto = ListsCache.GetListOfCrypto()
    IgnoredCrypto = DBH.GetIgnoredCurrencies(chatID)
    for i in AllCrypto:
        if i in IgnoredCrypto:
            IgnoreCryptoMenuMU.add(InlineKeyboardButton(i + " ✅", callback_data = "cur_ignore_" + i))
        else:
            IgnoreCryptoMenuMU.add(InlineKeyboardButton(i + " ❌", callback_data = "cur_ignore_" + i))
    IgnoreCryptoMenuMU.add(InlineKeyboardButton(dictLang['back'], callback_data = "cur_ignore_menu"))
    return IgnoreCryptoMenuMU

def IgnoreCurrenciesMenuMarkup(chatID: str, chatType: str) -> InlineKeyboardMarkup:
    lang = DBH.GetSetting(chatID, "lang", chatType)
    dictLang = ButtonTexts[lang]
    IgnoreCurrenciesMenuMU = InlineKeyboardMarkup()
    IgnoreCurrenciesMenuMU.add(InlineKeyboardButton("A", callback_data = "cur_ignore_a"))
    IgnoreCurrenciesMenuMU.add(InlineKeyboardButton("B", callback_data = "cur_ignore_b"))
    IgnoreCurrenciesMenuMU.add(InlineKeyboardButton("C", callback_data = "cur_ignore_c"))
    IgnoreCurrenciesMenuMU.add(InlineKeyboardButton("D-F", callback_data = "cur_ignore_df"))
    IgnoreCurrenciesMenuMU.add(InlineKeyboardButton("G-H", callback_data = "cur_ignore_gh"))
    IgnoreCurrenciesMenuMU.add(InlineKeyboardButton("I-J", callback_data = "cur_ignore_ij"))
    IgnoreCurrenciesMenuMU.add(InlineKeyboardButton("K-L", callback_data = "cur_ignore_kl"))
    IgnoreCurrenciesMenuMU.add(InlineKeyboardButton("M", callback_data = "cur_ignore_m"))
    IgnoreCurrenciesMenuMU.add(InlineKeyboardButton("N-Q", callback_data = "cur_ignore_nq"))
    IgnoreCurrenciesMenuMU.add(InlineKeyboardButton("R-S", callback_data = "cur_ignore_rs"))
    IgnoreCurrenciesMenuMU.add(InlineKeyboardButton("T-U", callback_data = "cur_ignore_tu"))
    IgnoreCurrenciesMenuMU.add(InlineKeyboardButton("V-Z", callback_data = "cur_ignore_vz"))
    IgnoreCurrenciesMenuMU.add(InlineKeyboardButton(dictLang['back'], callback_data = "cur_ignore_menu"))
    return IgnoreCurrenciesMenuMU

def IgnoreCurrenciesSetupMarkup(chatID: str, chatType: str, letter: str) -> InlineKeyboardMarkup:
    lang = DBH.GetSetting(chatID, "lang", chatType)
    dictLang = ButtonTexts[lang]
    AllCurrencies = ListsCache.GetListOfCur()
    IgnoredCurrencies = DBH.GetIgnoredCurrencies(chatID)
    AllFlags = ListsCache.GetDictOfFlags()
    IgnoreCurrenciesSetupMU = InlineKeyboardMarkup()
    if len(letter) == 1:
        letter = letter.upper()
        for i in AllCurrencies:
            if i[0] == letter:
                if i in IgnoredCurrencies:
                    IgnoreCurrenciesSetupMU.add(InlineKeyboardButton(AllFlags[i] + i + " ✅", callback_data = "cur_ignore_" + i))
                else:
                    IgnoreCurrenciesSetupMU.add(InlineKeyboardButton(AllFlags[i] + i + " ❌", callback_data = "cur_ignore_" + i))
    else:
        firstLetter = ord(letter[0].upper())
        lastLetter = ord(letter[1].upper())
        listOfLetters = []
        while firstLetter <= lastLetter:
            listOfLetters.append(chr(firstLetter))
            firstLetter += 1
        for i in AllCurrencies:
            if i[0] in listOfLetters:
                if i in IgnoredCurrencies:
                    IgnoreCurrenciesSetupMU.add(InlineKeyboardButton(AllFlags[i] + i + " ✅", callback_data = "cur_ignore_" + i))
                else:
                    IgnoreCurrenciesSetupMU.add(InlineKeyboardButton(AllFlags[i] + i + " ❌", callback_data = "cur_ignore_" + i))
    IgnoreCurrenciesSetupMU.add(InlineKeyboardButton(dictLang['back'], callback_data = "cur_curmenu"))
    return IgnoreCurrenciesSetupMU

def GetText(chatID: str, nameOfText: str, chatType: str) -> str:
    lang = DBH.GetSetting(chatID, "lang", chatType)
    answerText = ''
    if nameOfText in ListOfNamesOfTextForBigTexts:
        dictLang = AllBigTexts[lang]
        answerText = dictLang[nameOfText]
    elif nameOfText in ButtonTexts[lang]:
        dictLang = ButtonTexts[lang]
        answerText = dictLang[nameOfText]
    elif nameOfText in MessageTexts[lang]:
        dictLang = MessageTexts[lang]
        answerText = dictLang[nameOfText]
    return answerText