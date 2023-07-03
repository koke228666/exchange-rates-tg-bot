from aiogram.types.message import ContentType

consoleLog = False
import datetime

counterS = 0
counterL = 0
counterE = 0

def Print(printingText: str, status: str = "L"):
    printingText = str(printingText)
    global counterS, counterL, counterE
    status = status.lower()
    if consoleLog or status == "e" or status == "s":
        if status == 's':
            print("\033[36m{} ".format("Service") + "\033[37m{}".format(str(counterS)) + ": "+ printingText)
            counterS += 1
        elif status == 'e':
            print("\033[31m{} ".format("Error") + "\033[37m{}".format(str(counterE)) + ": "+ printingText)
            counterE += 1
        elif status == 'l':
            print("\033[32m{} ".format("Log") + "\033[37m{}".format(str(counterL)) + ": "+ printingText)
            counterL += 1
        elif status == 'w':
            print("\033[33m{} ".format("Warning") + "\033[37m{}".format(str(counterL)) + ": "+ printingText)
            counterL += 1
        elif status == '':
            print(printingText)

def EnableLogging():
    global consoleLog
    consoleLog = True

def DisableLogging():
    global consoleLog
    consoleLog = False

def PrintMainInfo(mes, mestxt: str):
    now = datetime.datetime.now()
    Print("","")
    Print("******************************","")
    Print(now.strftime("%d-%m-%Y %H:%M:%S"),"L")
    Print("Username: " + str(mes.from_user.username) + " | User ID: " + str(mes.from_user.id) + " | First name: " + str(mes.from_user.first_name) + " | Last name: " + str(mes.from_user.last_name), "L")
    Print("Chat ID: " + str(mes.chat.id) + " | Chat name: " + str(mes.chat.title) + " | Chat username: "+str(mes.chat.username) + " | Chat type: "+str(mes.chat.type), "L")
    Print("","")
    Print("Message: " + str(mestxt),    "L")

def IsEnabledLogging():
    global consoleLog
    return consoleLog