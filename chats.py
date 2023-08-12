import DBH

def writeChatsToFile():
    with open("chats.txt", "w") as file:
        for chat in DBH.GetChatIDs():
            file.write(str(chat) + "\n")