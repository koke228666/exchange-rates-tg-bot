import time
import DBH

BlackList = []

def IsUserInBlackList(userID: str, chatID: str) -> bool:
    global BlackList
    if userID in BlackList or chatID in BlackList:
        return True
    else:
        return False

def LoadBlackList():
    global BlackList
    while True:
        BlackList = DBH.GetBlacklist()
        time.sleep(60)

def AddToBlackList(userID: str, chatID: str, chatName: str):
    if userID not in BlackList:
        BlackList.append(userID)
    DBH.AddBlacklist(userID, chatID, chatName)

def RemoveFromBlackList(userID: str):
    BlackList.remove(userID)
    DBH.ClearBlacklist(userID)