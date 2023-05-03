from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

import DBH
import ListsCache
import os
from NewPrint import Print

from Dictionaries.ButtonTexts import ButtonTexts
from Dictionaries.MessageTexts import MessageTexts

AllBigTexts = {}
ListOfNamesOfTextforBigTexts = []

def LoadTexts():
    global AllBigTexts
    global ListOfNamesOfTextforBigTexts
    UAtexts = {}
    RUtexts = {}
    ENtexts = {}
    try:
        listFiles = os.listdir("Texts")
        for i in listFiles:
            fileWithText = open("Texts/" + i)
            fileText = fileWithText.read()
            fileWithText.close()
            nameOfText = i[2:-4]
            if nameOfText not in ListOfNamesOfTextforBigTexts:
                ListOfNamesOfTextforBigTexts.append(nameOfText)
            if i.find("UA") == 0:
                UAtexts[nameOfText] = fileText
            elif i.find("EN") == 0:
                ENtexts[nameOfText] = fileText
            elif i.find("RU") == 0:
                RUtexts[nameOfText] = fileText
        AllBigTexts['ua'] = UAtexts
        AllBigTexts['ru'] = RUtexts
        AllBigTexts['en'] = ENtexts
    except:
        Print("Problem with Texts. Redownload, pls.", "E")

def DonateMarkup(chatID: str, chatType: str) -> InlineKeyboardMarkup:
    lang = DBH.GetSetting(chatID, "lang", chatType)
    isDeleteButton = DBH.GetSetting(chatID, "deleteButton", chatType)
    dictLang = ButtonTexts[lang]
    DonateMU = InlineKeyboardMarkup()
    DonateMU.add(InlineKeyboardButton(dictLang['donate'], url="https://secure.wayforpay.com/donate/d92c340414735", callback_data="donate"))
    if isDeleteButton:
        DonateMU.add(InlineKeyboardButton(dictLang['delete'], callback_data = "delete"))
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
    SettingsMU.add(InlineKeyboardButton(dictLang['currencies'], callback_data = "cur_menu"))
    SettingsMU.add(InlineKeyboardButton(dictLang['lang'], callback_data = "lang_menu"))
    SettingsMU.add(InlineKeyboardButton(dictLang['delete_button'], callback_data = "delbut_menu"))
    SettingsMU.add(InlineKeyboardButton(dictLang['flags'], callback_data = "flags_menu"))
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
    
    lang = DBH.GetSetting(chatID, "lang", chatType)
    AllSettings = DBH.GetAllSettings(chatID, chatType)
    dictLang = ButtonTexts[lang]
    LanguageMenuMU = InlineKeyboardMarkup()
    LanguageMenuMU.add(InlineKeyboardButton("🇬🇧EN" + RulesMark('en', AllSettings), callback_data = "lang_en"))
    LanguageMenuMU.add(InlineKeyboardButton("💩RU" + RulesMark('ru', AllSettings), callback_data = "lang_ru"))
    LanguageMenuMU.add(InlineKeyboardButton("🇺🇦UA" + RulesMark('ua', AllSettings), callback_data = "lang_ua"))
    LanguageMenuMU.add(InlineKeyboardButton(dictLang['back'], callback_data = "settings"))
    return LanguageMenuMU

def FlagsMarkup(chatID: str, chatType: str) -> InlineKeyboardMarkup:
    lang = DBH.GetSetting(chatID, "lang", chatType)
    AllSettings = DBH.GetAllSettings(chatID, chatType)
    dictLang = ButtonTexts[lang]
    FlagsMU = InlineKeyboardMarkup()
    if AllSettings['flags']:
        FlagsMU.add(InlineKeyboardButton(dictLang['flags_button'] + " ✅", callback_data = "flags_button"))
    else:
        FlagsMU.add(InlineKeyboardButton(dictLang['flags_button'] + " ❌", callback_data = "flags_button"))
    FlagsMU.add(InlineKeyboardButton(dictLang['back'], callback_data = "settings"))
    return FlagsMU

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

def GetText(chatID: str, nameOfText: str, chatType: str) -> str:
    lang = DBH.GetSetting(chatID, "lang", chatType)
    answerText = ''
    if nameOfText in ListOfNamesOfTextforBigTexts:
        dictLang = AllBigTexts[lang]
        answerText = dictLang[nameOfText]
    elif nameOfText in ButtonTexts[lang]:
        dictLang = ButtonTexts[lang]
        answerText = dictLang[nameOfText]
    elif nameOfText in MessageTexts[lang]:
        dictLang = MessageTexts[lang]
        answerText = dictLang[nameOfText]
    return answerText