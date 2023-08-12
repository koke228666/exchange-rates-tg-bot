import DBH

def writeChatsToFile():
    with open("chats.txt", "w") as file:
        for chat in DBH.GetChatIDs():
            file.write(str(chat) + "\n")
    print("Chats written to file")

if __name__ == "__main__":
    writeChatsToFile()