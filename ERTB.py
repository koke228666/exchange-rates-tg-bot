# Token
from Token import botToken, botUsername

# Public libraries
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from threading import Thread
import sys
import time
import os
import traceback
import logging
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import json

# Own libraries
import DBH
from NewPrint import Print, EnableLogging, DisableLogging, PrintMainInfo
from SkipUpdates import EnableUpdates, DisableUpdates, IsUpdate
from GetExchangeRates import SheduleUpdate, SheduleCryptoUpdate
from BlackList import IsUserInBlackList, LoadBlackList, RemoveFromBlackList, AddToBlackList
from Processing import AnswerText, LoadCurrencies, LoadCrypto, LoadDictionaries, LoadFlags, LoadSymbols, SearchValuesAndCurrencies, RemoveIgnored, SpecialSplit, MessagePreparation
import TextHelper as CustomMarkup
from TextHelper import LoadTexts, GetText
import ListsCache
import StopDDoS
from w2n import ConvertWordsToNumber

# Main variables
bot = Bot(token=botToken)
dp = Dispatcher(bot)
IsStartedCount = False

def GetDataFromMessage(message: types.Message):
    data = {}
    data['fromUserId'] = message.from_user.id
    data['chatID'] = message.chat.id
    data['chatType'] = message.chat.type
    data['chatName'] = "" if data['chatType'] == "private" else message.chat.title
    data['userName'] = message.from_user.username
    return data

def IsFromBot(message: types.Message):
    try:
        if message.forward_from.username == botUsername or message.from_user.id == 777000:
            return True
    except:
        return False

# Public commands
@dp.message_handler(commands=['about'])
async def AboutMes(message: types.Message):
    messageData = GetDataFromMessage(message)
    if IsUserInBlackList(messageData["fromUserId"], messageData["chatID"]):
        return
    IsChatExist(messageData["chatID"], messageData["chatType"], messageData["chatName"])
    await message.reply(GetText(messageData['chatID'], "about", messageData['chatType']), reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))


@dp.message_handler(commands=['help'])
async def HelpMes(message: types.Message):
    messageData = GetDataFromMessage(message)
    if IsUserInBlackList(messageData["fromUserId"], messageData["chatID"]):
        return
    IsChatExist(messageData["chatID"], messageData["chatType"], messageData["chatName"])
    await message.reply(GetText(messageData["chatID"], "help", messageData["chatType"]), reply_markup=CustomMarkup.DeleteMarkup(messageData["chatID"], messageData["chatType"]))


def CanUserEditSettings(chatID: str, chatType: str, memberStatus: str, userID: str, userName: str, AllMembersAreAdministrators: bool = False) -> bool:
    сanUserEditSettings = False
    AllChatSettings = DBH.GetAllSettings(chatID, chatType)
    if DBH.IsAdmin(userID):
        сanUserEditSettings = True
    elif chatType == "private":
        сanUserEditSettings = True
    else:
        whoCanEditSettings = AllChatSettings['editSettings']
        if whoCanEditSettings == "everybody":
            сanUserEditSettings = True
        elif chatType == "group":
            if AllMembersAreAdministrators == True and whoCanEditSettings == 'admins':
                сanUserEditSettings = True
            elif AllMembersAreAdministrators == True and whoCanEditSettings == 'creator':
                if memberStatus == 'creator' or userName == "GroupAnonymousBot":
                    сanUserEditSettings = True
            elif AllMembersAreAdministrators == False:
                if whoCanEditSettings == 'admins' and (memberStatus == "administrator" or memberStatus == "creator" or userName == "GroupAnonymousBot") or whoCanEditSettings == 'creator' and (memberStatus == "creator" or userName == "GroupAnonymousBot"):
                    сanUserEditSettings = True
        elif chatType == "supergroup":
            if whoCanEditSettings == 'admins' and (memberStatus == "administrator" or memberStatus == "creator" or userName == "GroupAnonymousBot") or whoCanEditSettings == 'creator' and (memberStatus == "creator" or userName == "GroupAnonymousBot"):
                сanUserEditSettings = True
    return сanUserEditSettings


@dp.message_handler(commands=['settings'])
async def SettingsMes(message: types.Message):
    messageData = GetDataFromMessage(message)
    if IsUserInBlackList(messageData["fromUserId"], messageData["chatID"]):
        return
    IsChatExist(messageData["chatID"], messageData["chatType"], messageData["chatName"])

    member = await message.chat.get_member(messageData["fromUserId"])
    if CanUserEditSettings(messageData["chatID"], messageData["chatType"], member.status, message.from_user.id, messageData["userName"], message.chat.all_members_are_administrators):
        await message.reply(GetText(messageData["chatID"], "main_settings_menu", messageData["chatType"]), parse_mode="HTML", reply_markup=CustomMarkup.SettingsMarkup(messageData['chatID'], messageData['chatType']))
    else:
        await message.reply(GetText(messageData["chatID"], "error_main_settings_menu", messageData["chatType"]), parse_mode="HTML", reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))


@dp.message_handler(commands=['donate'])
async def DonateMes(message: types.Message):
    messageData = GetDataFromMessage(message)
    if IsUserInBlackList(messageData["fromUserId"], messageData["chatID"]):
        return
    IsChatExist(messageData["chatID"], messageData["chatType"], messageData["chatName"])
    await message.reply(GetText(messageData["chatID"], "donate", messageData["chatType"]), reply_markup=CustomMarkup.DonateMarkup(messageData['chatID'], messageData['chatType']))


# Admin`s commands
@dp.message_handler(commands=['echo'])
async def EchoVoid(message: types.Message):
    messageData = GetDataFromMessage(message)
    if IsUserInBlackList(messageData["fromUserId"], messageData["chatID"]):
        return
    if DBH.IsAdmin(messageData["fromUserId"]):
        MessageToUsers = (message.text).replace("/echo ", "")
        adminList = DBH.GetAdmins()
        for i in adminList:
            await bot.send_message(i, "Started sending a message to all users. Message text:\n\n" + MessageToUsers, reply_markup=CustomMarkup.DeleteMarkup(i, "private"))
        listGC = DBH.GetGroupChatIDs()
        for i in listGC:
            try:
                await bot.send_message(i, MessageToUsers, parse_mode="HTML", disable_web_page_preview=True, reply_markup=CustomMarkup.DonateMarkup(i, "group"))
            except:
                Print("Chat " + str(i) + " is not available.", "W")
            time.sleep(0.035)
        listPC = DBH.GetPrivateChatIDs()
        for i in listPC:
            try:
                await bot.send_message(i, MessageToUsers, parse_mode="HTML", disable_web_page_preview=True, reply_markup=CustomMarkup.DonateMarkup(i, "private"))
            except:
                Print("Chat " + str(i) + " is not available.", "W")
            time.sleep(0.035)
        for i in adminList:
            await bot.send_message(i, "The 'echo' is over.", reply_markup=CustomMarkup.DeleteMarkup(i, "private"))


@dp.message_handler(commands=['write'])
async def EchoVoid(message: types.Message):
    messageData = GetDataFromMessage(message)

    if IsUserInBlackList(messageData["fromUserId"], messageData["chatID"]):
        return
    if DBH.IsAdmin(messageData["fromUserId"]):
        MessageToUsers = (message.text).replace("/write ", "")
        index = MessageToUsers.find(" ")
        toChatID = MessageToUsers[0:index]
        MessageToUsers = MessageToUsers.replace(str(toChatID) + " ", "")
        try:
            await bot.send_message(toChatID, MessageToUsers, parse_mode="HTML")
            await bot.send_message(messageData["fromUserId"], "Message sent.")
        except:
            await bot.send_message(messageData["fromUserId"], "Failed to send a message.")


@dp.message_handler(commands=['count'])
async def CountVoid(message: types.Message):
    messageData = GetDataFromMessage(message)

    global IsStartedCount
    if IsUserInBlackList(messageData["fromUserId"], messageData["chatID"]):
        return
    if DBH.IsAdmin(messageData["fromUserId"]):
        if not IsStartedCount:
            isShortVariant = False
            Variant = (message.text).replace("/count", "").replace(" ", "")
            if Variant == "short":
                isShortVariant = True
            adminList = DBH.GetAdmins()
            for i in adminList:
                if not isShortVariant:
                    await bot.send_message(i, "Started counting the number of members of all chats.", reply_markup=CustomMarkup.DeleteMarkup(i, "private"))
                else:
                    await bot.send_message(i, "Started counting the number of members of group chats.", reply_markup=CustomMarkup.DeleteMarkup(i, "private"))
            IsStartedCount = True
            CountUsers = 0
            listGC = DBH.GetGroupChatIDs()
            for i in listGC:
                try:
                    CountUsers += await bot.get_chat_members_count(i)
                except:
                    Print("Chat " + str(i) + " not found.", "W")
                time.sleep(0.035)
                IsStartedCount = False
            if not isShortVariant:
                IsStartedCount = True
                listPC = DBH.GetPrivateChatIDs()
                for i in listPC:
                    try:
                        CountUsers += await bot.get_chat_members_count(i) - 1
                    except:
                        Print("Chat " + str(i) + " not found.", "W")
                    time.sleep(0.035)
                IsStartedCount = False
            for i in adminList:
                if not isShortVariant:
                    await bot.send_message(i, "The number of members of all chats: " + str(CountUsers), reply_markup=CustomMarkup.DeleteMarkup(i, "private"))
                else:
                    await bot.send_message(i, "The number of members of group chats: " + str(CountUsers), reply_markup=CustomMarkup.DeleteMarkup(i, "private"))
        else:
            await message.reply("The counting has already begun.", reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))


@dp.message_handler(commands=['newadmin'])
async def AddAdminVoid(message: types.Message):
    messageData = GetDataFromMessage(message)

    if IsUserInBlackList(messageData["fromUserId"], messageData["chatID"]):
        return
    if DBH.IsAdmin(messageData["fromUserId"]):
        newAdminID = message.text
        newAdminID = newAdminID.replace("/newadmin ", "")
        if newAdminID.isdigit():
            if not DBH.IsAdmin(newAdminID):
                DBH.AddAdmin(int(newAdminID))
                ListOfAdmins = DBH.GetAdmins()
                if newAdminID in ListOfAdmins:
                    await message.reply("A new administrator has been successfully added.", reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))
                else:
                    await message.reply("Failed to add a new administrator.", reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))
            else:
                await message.reply("This ID is already on the list of administrators.", reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))
        else:
            await message.reply("The ID should only contain numbers and possibly a minus.", reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))


@dp.message_handler(commands=['amount'])
async def AmountVoid(message: types.Message):
    messageData = GetDataFromMessage(message)

    if IsUserInBlackList(messageData["fromUserId"], messageData["chatID"]):
        return
    if DBH.IsAdmin(messageData["fromUserId"]):
        chatStats = DBH.GetTimeStats()
        StatsByOneDay = DBH.GetStatsInPeriod(1)
        answerMes = "For all the time:\nPM: " + str(chatStats['private']) + "\nGroups: " + str(chatStats['groups']) + "\n\nIn 24 hours:\nPM: " + str(StatsByOneDay['activePrivate']) + "\nGroups: " + str(StatsByOneDay['activeGroups']) + "\n\nIn a week:\nPM: " + str(chatStats['activePrivateWeek']) + "\nGroups: " + str(chatStats['activeGroupsWeek']) + "\n\nIn 30 days:\nPM: " + str(chatStats['activePrivateMonth']) + "\nGroups: " + str(chatStats['activeGroupsMonth'])
        await message.reply(answerMes, reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))


@dp.message_handler(commands=['plotamount'])
async def PlotAmountVoid(message: types.Message):
    messageData = GetDataFromMessage(message)

    if IsUserInBlackList(messageData["fromUserId"], messageData["chatID"]):
        return
    if DBH.IsAdmin(messageData["fromUserId"]):
        chartData = DBH.GetStatsForChart()
        chartsNames = ["generalAmount", "activeWeek", "activeMonth"]
        BuildChartAmount(chartData['privateChatsAmount'], chartData['groupChatsAmount'], chartData['dates'], "privateChatsAmount", "groupChatsAmount", chartsNames[0])
        BuildChartAmount(chartData['activeWeekPrivateChats'], chartData['activeWeekGroupChats'], chartData['dates'], "activeWeekPrivateChats", "activeWeekGroupChats", chartsNames[1])
        BuildChartAmount(chartData['activeMonthPrivateChats'], chartData['activeMonthGroupChats'], chartData['dates'], "activeMonthPrivateChats", "activeMonthGroupChats", chartsNames[2])
        media = types.MediaGroup()
        media.attach_document(types.InputFile('generalAmount.png'))
        media.attach_document(types.InputFile('activeWeek.png'))
        media.attach_document(types.InputFile('activeMonth.png'))
        await message.reply_media_group(media=media)
        DeleteCharts(chartsNames)

@dp.message_handler(commands=['stats'])
async def StatsVoid(message: types.Message):
    messageData = GetDataFromMessage(message)

    if IsUserInBlackList(messageData["fromUserId"], messageData["chatID"]):
        return
    if DBH.IsAdmin(messageData["fromUserId"]):
        botUsageLastDayByMinute = DBH.GetBotUsageLastDayByMinute()
        botUsageLastWeekByHour = DBH.GetBotUsageLastWeekByHour()
        botUsageLastMonthByDay = DBH.GetBotUsageLastMonthByDay()

        botUniqueUsersAllTimeByDay = DBH.GetBotUniqueUsersAllTimeByDay()
        botUniqueUsersAllTimeByMonth = DBH.GetBotUniqueUsersAllTimeByMonth()

        usageToday = sum(list(botUsageLastDayByMinute.values()))
        usageLastWeek = sum(list(botUsageLastWeekByHour.values()))
        usageLastMonth = sum(list(botUsageLastMonthByDay.values()))
        try:
            uniqueUsersToday = botUniqueUsersAllTimeByDay[datetime.datetime.now().strftime("%Y-%m-%d")]
        except:
            uniqueUsersToday = 0
        uniqueUsersLastWeek = DBH.GetBotUniqueUsersLastWeek()
        uniqueUsersThisMonth = DBH.GetBotUniqueUsersLastMonth()
        answerMes = "Bot activity:\n\nToday: " + str(usageToday) + "\nIn the last week: " + str(usageLastWeek) + "\nIn the last month: " + str(usageLastMonth) + "\n\nUnique users:\n\nToday: " + str(uniqueUsersToday) + "\nIn the last week: " + str(uniqueUsersLastWeek) + "\nIn the last month: " + str(uniqueUsersThisMonth)
        await message.reply(answerMes, reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))
        

@dp.message_handler(commands=['plotstats'])
async def PlotStatsVoid(message: types.Message):
    startTime = time.time()
    messageData = GetDataFromMessage(message)

    if IsUserInBlackList(messageData["fromUserId"], messageData["chatID"]):
        return
    if DBH.IsAdmin(messageData["fromUserId"]):
        allRecordsCount = DBH.GetProcessedCurrenciesCountForStats()
        botUsageAllTimeByDay = {}
        botUniqueUsersAllTimeByDay = {}
        botUniqueUsersAllTimeByMonth = {}
        botUsageLastDayByMinute = {}
        botUsageLastWeekByHour = {}
        botUsageLastMonthByDay = {}
        uniqueIDs = {}
        langActivity = {}

        totalUsers = DBH.GetUniqueUsersCount()

        langDistribution = DBH.GetLangDistribution()
        langActivity = DBH.GetLangActivity()

        botUsageLastDayByMinute = DBH.GetBotUsageLastDayByMinute()
        botUsageLastWeekByHour = DBH.GetBotUsageLastWeekByHour()
        botUsageLastMonthByDay = DBH.GetBotUsageLastMonthByDay()

        botUsageAllTimeByDay = DBH.GetBotUsageAllTimeByDay()
        botUniqueUsersAllTimeByDay = DBH.GetBotUniqueUsersAllTimeByDay()
        botUniqueUsersAllTimeByMonth = DBH.GetBotUniqueUsersAllTimeByMonth()

        Print("Started plotting stats. Time: " + str(time.time() - startTime), "S")

        for i in botUsageLastWeekByHour:
            botUsageLastWeekByHour[i] = botUsageLastWeekByHour[i] / 60
        chartsNames = ["botUsageAllTimeByDay", "botUniqueUsersAllTimeByDay", "botUniqueUsersAllTimeByMonth", "botUsageLastDayByMinute", "botUsageLastWeekByHour", "botUsageLastMonthByDay", "langDistributionUsers", "langDistributionPercentage", "langActivityCalls", "langActivityPercentage"]
        BuildChart(list(botUsageAllTimeByDay.values()), list(botUsageAllTimeByDay.keys()), "Bot usage for all time by day", "Calls per day", chartsNames[0])
        # for day, users in botUniqueUsersAllTimeByDay.items():
        #     botUniqueUsersAllTimeByDay[day] = len(users)
        BuildChart(list(botUniqueUsersAllTimeByDay.values()), list(botUniqueUsersAllTimeByDay.keys()), "Bot unique users for all time by day", "Users per day", chartsNames[1])
        # for month, users in botUniqueUsersAllTimeByMonth.items():
        #     botUniqueUsersAllTimeByMonth[month] = len(users)
        BuildChart(list(botUniqueUsersAllTimeByMonth.values()), list(botUniqueUsersAllTimeByMonth.keys()), "Bot unique users for all time by month", "Users per month", chartsNames[2])
        BuildChart(list(botUsageLastDayByMinute.values()), list(botUsageLastDayByMinute.keys()), "Bot usage today by minute", "Calls per minute", chartsNames[3])
        BuildChart(list(botUsageLastWeekByHour.values()), list(botUsageLastWeekByHour.keys()), "Bot usage last week by hour", "Calls per minute", chartsNames[4])
        BuildChart(list(botUsageLastMonthByDay.values()), list(botUsageLastMonthByDay.keys()), "Bot usage last month by day", "Calls per day", chartsNames[5])
        BuildBarChart(list(langDistribution.keys()), list(langDistribution.values()), "Language distribution", "Users", chartsNames[6])
        for lang, count in langDistribution.items():
            langDistribution[lang] = count / totalUsers * 100
        BuildBarChart(list(langDistribution.keys()), list(langDistribution.values()), "Language distribution", "Percentage", chartsNames[7])
        BuildBarChart(list(langActivity.keys()), list(langActivity.values()), "Language activity", "Calls", chartsNames[8])
        for lang, count in langActivity.items():
            langActivity[lang] = count / allRecordsCount * 100
        BuildBarChart(list(langActivity.keys()), list(langActivity.values()), "Language activity", "Percentage", chartsNames[9])
        media = types.MediaGroup()
        for i in chartsNames:
            media.attach_document(types.InputFile(i + ".png"))
        await message.reply_media_group(media=media)
        DeleteCharts(chartsNames)
        Print("Plotting stats took " + str(time.time() - startTime) + " seconds.", "S")

@dp.message_handler(commands=['backup'])
async def BackupVoid(message: types.Message):
    messageData = GetDataFromMessage(message)

    if IsUserInBlackList(messageData["fromUserId"], messageData["chatID"]):
        return
    if DBH.IsAdmin(messageData["fromUserId"]):
        nameOfBackup = DBH.CreateAllBackups()
        fileSize = os.path.getsize(nameOfBackup)
        if fileSize <= 52428800:
            try:
                backupFile = open(nameOfBackup, 'rb')
                await bot.send_document(messageData["chatID"], backupFile)
            except:
                await message.reply("The file sending failed.", reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))
        else:
            await message.reply("The file is too big. Its weight is " + str(fileSize) + " bytes.", reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))


@dp.message_handler(commands=['unban'])
async def UnbanVoid(message: types.Message):
    messageData = GetDataFromMessage(message)

    if IsUserInBlackList(messageData["fromUserId"], messageData["chatID"]):
        return
    if DBH.IsAdmin(messageData["fromUserId"]):
        unbanID = message.text
        unbanID = unbanID.replace("/unban ", "")
        if unbanID.isdigit():
            if DBH.IsBlacklisted(int(unbanID)):
                RemoveFromBlackList(int(unbanID))
                if not DBH.IsBlacklisted(int(unbanID)):
                    await message.reply("User/group has been successfully unblocked.", reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))
                else:
                    await message.reply("Failed to unblock user/group.", reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))
            else:
                await message.reply("This user/group is not in a black list.", reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))
        else:
            await message.reply("The ID should only contain numbers and minus.", reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))


@dp.message_handler(commands=['ban'])
async def UnbanVoid(message: types.Message):
    messageData = GetDataFromMessage(message)

    if IsUserInBlackList(messageData["fromUserId"], messageData["chatID"]):
        return
    if DBH.IsAdmin(messageData["fromUserId"]):
        banID = message.text
        banID = banID.replace("/ban ", "")
        if banID.isdigit() or (banID[1:].isdigit() and banID[0] == '-'):
            if not DBH.IsBlacklisted(int(banID)):
                AddToBlackList(int(banID), messageData["fromUserId"], messageData["chatName"])
                if DBH.IsBlacklisted(int(banID)):
                    await message.reply("User/group successfully blocked.", reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))
                else:
                    await message.reply("Failed to block a user/chat.", reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))
            else:
                await message.reply("This user/group is already in the black list.", reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))
        else:
            await message.reply("The ID should only contain numbers and minus.", reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))


@dp.message_handler(commands=['chats'])
async def ChatsVoid(message: types.Message):
    messageData = GetDataFromMessage(message)

    if IsUserInBlackList(messageData["fromUserId"], messageData["chatID"]):
        return
    if DBH.IsAdmin(messageData["fromUserId"]):
        with open("chats.txt", "w") as file:
            for chat in DBH.GetChatIDs():
                file.write(str(chat) + "\n")
        await bot.send_document(messageData["chatID"], types.InputFile("chats.txt"))
        os.remove("chats.txt")         


# Technical commands
@dp.message_handler(commands=['start'])
async def StartVoid(message: types.Message):
    messageData = GetDataFromMessage(message)

    if IsUserInBlackList(messageData["fromUserId"], messageData["chatID"]):
        return

    if not IsChatExist(messageData["chatID"], messageData["chatType"], messageData["chatName"]):
        if messageData["chatType"] == "private":
            userLang = message.from_user.language_code
            lang = "en"
            langs = []
            with open("Dictionaries/langs.json", "r", encoding="utf-8") as file:
                langs = json.load(file)
            langs = langs['langs']
            for i in langs:
                if i['code'] == userLang:
                    lang = i['botCode']
                    break
            
            DBH.SetSetting(messageData["chatID"], "lang", lang, messageData["chatType"])
            await message.reply(GetText(messageData["chatID"], "main_settings_menu", messageData["chatType"]), reply_markup=CustomMarkup.SettingsMarkup(messageData['chatID'], messageData['chatType']))


# Main void
@dp.message_handler(content_types=ContentType.ANY)
async def MainVoid(message: types.Message):
    starttime = time.time()
    messageData = GetDataFromMessage(message)

    # Checking if the message is from the bot
    if IsFromBot(message):
        return

    # Checking if a user is on the blacklist
    if IsUserInBlackList(messageData["fromUserId"], messageData["chatID"]):
        Print("User (" + str(messageData["fromUserId"]) + ") is in the blacklist. Message: " + str(message.text), "L")
        return

    # Get message text
    MessageText = message.text
    if message.photo or message.video is not None or message.document is not None:
        MessageText = message.caption
    if MessageText is None or MessageText == "":
        return

    # Logging basic information to terminal
    PrintMainInfo(message, MessageText)

    # Checking the chat in the database
    IsChatExist(messageData["chatID"], messageData["chatType"], messageData["chatName"])

    # preparing a message
    OriginalMessageText = MessageText
    try:
        MessageText = MessagePreparation(MessageText)
    except:
        Print("Error SpecialSplit(). Message: " + OriginalMessageText, "E")
        return
    
    Print("After MessagePreparation(): " + MessageText, "L")

    # Preparing a message for searching currencies
    try:
        TextArray = SpecialSplit(MessageText)
    except:
        Print("Error SpecialSplit(). Message: " + OriginalMessageText, "E")
        return
    Print("After SpecialSplit(): " + str(TextArray), "L")

    # Word to number
    try:
        TextArray = ConvertWordsToNumber(TextArray)
    except:
        Print("Error ConvertWordsToNumber(). Message: " + OriginalMessageText, "E")
        return
    Print("After ConvertWordsToNumber(): " + str(TextArray), "L")

    # Searching Currencies
    try:
        NumArray = SearchValuesAndCurrencies(TextArray)
        NumArray = RemoveIgnored(NumArray, messageData["chatID"])
    except:
        Print("Error SearchValuesAndCurrencies(). Message: " + OriginalMessageText, "E")
        return
    Print("After SearchValuesAndCurrencies(): " + str(NumArray), "L")

    # If there are no currencies, then work is interrupted
    if NumArray == [[], [], [], []]:
        return

    if StopDDoS.updateData(messageData["fromUserId"], messageData["chatID"], len(NumArray[1]) + len(NumArray[3]), message.chat.title):
        await message.reply(GetText(messageData["chatID"], 'added_to_bl', messageData["chatType"]))
        ListAdmins = DBH.GetAdmins()
        for i in ListAdmins:
            await bot.send_message(i, "User @" + str(message.from_user.username) + " id: " + str(messageData["fromUserId"]) + " is blocked.", reply_markup=CustomMarkup.DeleteMarkup(i, "private"))
        return

    result = AnswerText(NumArray, messageData["chatID"], messageData["chatType"])
    endtime = time.time()
    Print("Time: " + str(endtime - starttime), "L")
    try:
        reply_message = await message.reply(result, parse_mode="HTML", disable_web_page_preview=True, reply_markup=CustomMarkup.DeleteMarkup(messageData['chatID'], messageData['chatType']))
        DBH.UpdateChatUsage(messageData["chatID"])
        DBH.NewProcessedCurrency(messageData["chatID"], messageData["fromUserId"], message.from_user.language_code, ','.join(NumArray[1]+NumArray[3]), ','.join(DBH.GetAllCurrencies(messageData["chatID"]) + DBH.GetAllCrypto(messageData["chatID"])), reply_message.message_id)
    except:
        Print("Cannot send message. Chat ID: " + str(message.chat.id) +
              " | Chat name: " + str(message.chat.title) +
              " | Chat username: " + 
              str(message.chat.username) + 
              " | Chat type: "+str(message.chat.type), "E")
    
    
# Callbacks
@dp.callback_query_handler(lambda call: True)
async def CallbackAnswer(call: types.CallbackQuery):
    fromUserId = call.from_user.id
    chatID = call.message.chat.id
    chatType = call.message.chat.type
    callData = call.data
    allAdmins = call.message.chat.all_members_are_administrators
    userName = call.from_user.username
    Print("Callback data: " + str(call), "L")

    if IsUserInBlackList(call.message.from_user.id, chatID):
        return
    if callData == "delete":
        CanUserDeleteMes = False
        if chatType == "private":
            CanUserDeleteMes = True
        else:
            whoCanDeleteMes = DBH.GetSetting(chatID, "deleteRules", chatType)
            if whoCanDeleteMes == "everybody":
                CanUserDeleteMes = True
            elif chatType == "group":
                member = await call.message.chat.get_member(fromUserId)
                if allAdmins == True and (whoCanDeleteMes == 'admins' or whoCanDeleteMes == 'everybody'):
                    CanUserDeleteMes = True
                elif allAdmins == True and whoCanDeleteMes == 'creator':
                    if member.status == 'creator':
                        CanUserDeleteMes = True
                elif allAdmins == False:
                    if whoCanDeleteMes == 'admins' and (member.status == "administrator" or member.status == "creator") or whoCanDeleteMes == 'creator' and member.status == "creator" or whoCanDeleteMes == 'everybody':
                        CanUserDeleteMes = True
            elif chatType == "supergroup":
                try:
                    member = await call.message.chat.get_member(fromUserId)
                    if whoCanDeleteMes == 'admins' and (member.status == "administrator" or member.status == "creator") or whoCanDeleteMes == 'creator' and member.status == "creator" or whoCanDeleteMes == 'everybody':
                        CanUserDeleteMes = True
                except:
                    pass
        if CanUserDeleteMes:
            try: 
                await bot.edit_message_text(call.message.text + "\n\n@" + str(call.from_user.username) + " (id: " + str(fromUserId) + ")" + " delete it.", chatID, call.message.message_id)
                await call.message.delete()
                DBH.DeleteProcessedCurrency(chatID, call.message.message_id)

            except:
                Print("Cannot delete message.", "E")
    elif str(callData).find("delbut_") == 0:
        member = await call.message.chat.get_member(fromUserId)
        if not CanUserEditSettings(chatID, chatType, member.status, call.from_user.id, userName, allAdmins):
            return
        Index = str(callData).find("_") + 1
        Value = str(callData)[Index:len(str(callData))]
        if Value == "menu":
            pass
        elif Value == "button":
            IsFlag = DBH.GetSetting(chatID, 'deleteButton', chatType)
            DBH.SetSetting(chatID, 'deleteButton', int(not IsFlag), chatType)
        else:
            DBH.SetSetting(chatID, 'deleteRules', Value, chatType)
        await bot.edit_message_text(GetText(chatID, 'delete_button_menu', chatType), chatID, call.message.message_id, parse_mode="HTML", reply_markup=CustomMarkup.DeleteButtonMenuMarkup(chatID, chatType))

    elif str(callData).find("lang_") == 0:
        member = await call.message.chat.get_member(fromUserId)
        if not CanUserEditSettings(chatID, chatType, member.status, call.from_user.id, userName, allAdmins):
            return
        Index = str(callData).find("_") + 1
        Value = str(callData)[Index:len(str(callData))]
        if Value == "menu":
            pass
        else:
            DBH.SetSetting(chatID, 'lang', Value, chatType)
        await bot.edit_message_text(GetText(chatID, 'lang_menu', chatType), chatID, call.message.message_id, parse_mode="HTML", reply_markup=CustomMarkup.LanguageMenuMarkup(chatID, chatType))

    elif str(callData).find("ui_") == 0:
        member = await call.message.chat.get_member(fromUserId)
        if not CanUserEditSettings(chatID, chatType, member.status, call.from_user.id, userName, allAdmins):
            return
        Index = str(callData).find("_") + 1
        Value = str(callData)[Index:len(str(callData))]
        if Value == "menu":
            pass
        elif Value == "flags":
            IsFlag = DBH.GetSetting(chatID, 'flags', chatType)
            DBH.SetSetting(chatID, 'flags', int(not IsFlag), chatType)
        elif Value == "symbols":
            IsSymbol = DBH.GetSetting(chatID, 'currencySymbol', chatType)
            DBH.SetSetting(chatID, 'currencySymbol', int(not IsSymbol), chatType)
        Print(GetText(chatID, 'mes_view_menu', chatType), "L")
        await bot.edit_message_text(GetText(chatID, 'mes_view_menu', chatType), chatID, call.message.message_id, parse_mode="HTML", reply_markup=CustomMarkup.MessageViewMarkup(chatID, chatType))

    elif str(callData).find("edit_") == 0:
        member = await call.message.chat.get_member(fromUserId)
        memberStatus = member.status
        if not CanUserEditSettings(chatID, chatType, memberStatus, call.from_user.id, userName, allAdmins):
            return
        Index = str(callData).find("_") + 1
        Value = str(callData)[Index:len(str(callData))]
        if Value == "menu":
            pass
        else:
            if memberStatus == "member":
                pass
            elif memberStatus == "administrator" and (Value == "admins" or Value == "everybody"):
                DBH.SetSetting(chatID, 'editSettings', Value, chatType)
            elif memberStatus == "creator":
                DBH.SetSetting(chatID, 'editSettings', Value, chatType)
        await bot.edit_message_text(GetText(chatID, 'edit_menu', chatType), chatID, call.message.message_id, parse_mode="HTML", reply_markup=CustomMarkup.EditMenuMarkup(chatID, chatType))

    elif str(callData).find("cur_ignore_") == 0:
        member = await call.message.chat.get_member(fromUserId)
        memberStatus = member.status
        if not CanUserEditSettings(chatID, chatType, memberStatus, call.from_user.id, userName, allAdmins):
            return
        callData = str(callData).replace("cur_ignore_", "")
        Value = str(callData)[0:len(str(callData))]

        if Value == "menu":
            await bot.edit_message_text(GetText(chatID, "ignore_currencies_mainmenu", chatType), chatID, call.message.message_id, parse_mode="HTML", reply_markup=CustomMarkup.IgnoreCurrenciesMainMenuMarkup(chatID, chatType))
        elif Value == "cryptomenu":
            await bot.edit_message_text(GetText(chatID, "ignore_crypto_mainmenu", chatType), chatID, call.message.message_id, parse_mode="HTML", reply_markup=CustomMarkup.IgnoreCryptoMenuMarkup(chatID, chatType))
        elif Value == "curmenu":
            await bot.edit_message_text(GetText(chatID, "ignore_currencies_menu", chatType), chatID, call.message.message_id, parse_mode="HTML", reply_markup=CustomMarkup.IgnoreCurrenciesMenuMarkup(chatID, chatType))
        elif len(Value) == 1 or len(Value) == 2:
            await bot.edit_message_text(GetText(chatID, "ignore_letter_menu", chatType), chatID, call.message.message_id, parse_mode="HTML", reply_markup=CustomMarkup.IgnoreCurrenciesSetupMarkup(chatID, chatType, Value))
        elif len(Value) == 3 or len(Value) == 4:
            DBH.SetIgnoredCurrency(chatID, Value, not DBH.GetIgnoredCurrency(chatID, Value))
            DBH.ReverseCurrencySetting(chatID, Value)
            if Value in ListsCache.GetListOfCrypto():
                await bot.edit_message_text(GetText(chatID, "ignore_crypto_mainmenu", chatType), chatID, call.message.message_id, parse_mode="HTML", reply_markup=CustomMarkup.IgnoreCryptoMenuMarkup(chatID, chatType))
            else:
                dictForMU = {'A': 'a', 'B': 'b', 'C': 'c', 'D': 'df', 'E': 'df', 'F': 'df', 'G': 'gh', 'H': 'gh', 'I': 'ij', 'J': 'ij', 'K': 'kl', 'L': 'kl', 'M': 'm',
                             'N': 'nq', 'O': 'nq', 'P': 'nq', 'Q': 'nq', 'R': 'rs', 'S': 'rs', 'T': 'tu', 'U': 'tu', 'V': 'vz', 'W': 'vz', 'X': 'vz', 'Y': 'vz', 'Z': 'vz'}
                await bot.edit_message_text(GetText(chatID, "ignore_letter_menu", chatType), chatID, call.message.message_id, parse_mode="HTML", reply_markup=CustomMarkup.IgnoreCurrenciesSetupMarkup(chatID, chatType, dictForMU[Value[0]]))

    elif str(callData).find("cur_") == 0:
        member = await call.message.chat.get_member(fromUserId)
        memberStatus = member.status
        if not CanUserEditSettings(chatID, chatType, memberStatus, call.from_user.id, userName, allAdmins):
            return
        Index = str(callData).find("_") + 1
        Value = str(callData)[Index:len(str(callData))]

        if Value == "menu":
            await bot.edit_message_text(GetText(chatID, "currencies_mainmenu", chatType), chatID, call.message.message_id, parse_mode="HTML", reply_markup=CustomMarkup.CurrenciesMainMenuMarkup(chatID, chatType))
        elif Value == "cryptomenu":
            await bot.edit_message_text(GetText(chatID, "crypto_mainmenu", chatType), chatID, call.message.message_id, parse_mode="HTML", reply_markup=CustomMarkup.CryptoMenuMarkup(chatID, chatType))
        elif Value == "curmenu":
            await bot.edit_message_text(GetText(chatID, "currencies_menu", chatType), chatID, call.message.message_id, parse_mode="HTML", reply_markup=CustomMarkup.CurrenciesMenuMarkup(chatID, chatType))
        elif len(Value) == 1 or len(Value) == 2:
            await bot.edit_message_text(GetText(chatID, "letter_menu", chatType), chatID, call.message.message_id, parse_mode="HTML", reply_markup=CustomMarkup.CurrenciesSetupMarkup(chatID, chatType, Value))
        elif len(Value) == 3 or len(Value) == 4:
            DBH.ReverseCurrencySetting(chatID, Value)
            if Value in ListsCache.GetListOfCrypto():
                await bot.edit_message_text(GetText(chatID, "crypto_mainmenu", chatType), chatID, call.message.message_id, parse_mode="HTML", reply_markup=CustomMarkup.CryptoMenuMarkup(chatID, chatType))
            else:
                dictForMU = {'A': 'a', 'B': 'b', 'C': 'c', 'D': 'df', 'E': 'df', 'F': 'df', 'G': 'gh', 'H': 'gh', 'I': 'ij', 'J': 'ij', 'K': 'kl', 'L': 'kl', 'M': 'm',
                             'N': 'nq', 'O': 'nq', 'P': 'nq', 'Q': 'nq', 'R': 'rs', 'S': 'rs', 'T': 'tu', 'U': 'tu', 'V': 'vz', 'W': 'vz', 'X': 'vz', 'Y': 'vz', 'Z': 'vz'}
                await bot.edit_message_text(GetText(chatID, "letter_menu", chatType), chatID, call.message.message_id, parse_mode="HTML", reply_markup=CustomMarkup.CurrenciesSetupMarkup(chatID, chatType, dictForMU[Value[0]]))

    elif callData == "settings":
        await bot.edit_message_text(GetText(chatID, "main_settings_menu", chatType), chatID, call.message.message_id, parse_mode="HTML", reply_markup=CustomMarkup.SettingsMarkup(chatID, chatType))


def CheckArgument(key: str, value: str) -> bool:
    isAllOkArg = True
    if key == "--logs" or key == "-l":
        if value == "1":
            EnableLogging()
        elif value == "0":
            DisableLogging()
        else:
            isAllOkArg = False
    elif key == "--admin" or key == "-a":
        if value.isdigit():
            if not DBH.IsAdmin(value):
                DBH.AddAdmin(value)
        else:
            isAllOkArg = False
    elif key == "--updates" or key == "-u":
        if value == "1":
            EnableUpdates()
        elif value == "0":
            DisableUpdates()
        else:
            isAllOkArg = False
    else:
        print("Error. Unknow argument '{}'".format(key))
    return isAllOkArg

def BuildChartAmount(firstArr: list[int], secondArr: list[int], dates: list[str], firstLabel: str, secondLabel: str, chartName: str):
    date_interval = int((datetime.datetime.strptime(dates[-1], '%Y-%m-%d') - datetime.datetime.strptime(dates[0], '%Y-%m-%d')).days / 10)
    if date_interval < 1:
        date_interval = 1
    dates = [datetime.datetime.strptime(date_str, "%Y-%m-%d") for date_str in dates]
    plt.figure(figsize=(16,9))
    plt.plot(dates, firstArr, label=firstLabel)
    plt.plot(dates, secondArr, label=secondLabel)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=date_interval))
    plt.grid()
    plt.legend()        
    plt.savefig(chartName + '.png')
    plt.clf()

def BuildChart(arr: list[int], dates: list[str], label: str, labely: str, chartName: str):
    plt.figure(figsize=(16,9))
    if label.find("by day") != -1:
        try:
            date_interval = int((datetime.datetime.strptime(dates[-1], '%Y-%m-%d') - datetime.datetime.strptime(dates[0], '%Y-%m-%d')).days / 10)
            if date_interval < 1:
                date_interval = 1
        except:
            date_interval = 1
        dates = [datetime.datetime.strptime(date_str, "%Y-%m-%d") for date_str in dates]
        plt.plot(dates, arr, label=label)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=date_interval))
    elif label.find("by minute") != -1:
        dates = [datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M") for date_str in dates]
        plt.plot(dates, arr, label=label)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        date_interval = 60
        plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=date_interval))
    elif label.find("by hour") != -1:
        dates = [datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M") for date_str in dates]
        plt.plot(dates, arr, label=label)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
        date_interval = 24
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=date_interval))
    elif label.find("by month") != -1:
        dates = [datetime.datetime.strptime(date_str, "%Y-%m") for date_str in dates]
        plt.plot(dates, arr, label=label)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        date_interval = 1
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=date_interval))
    plt.ylabel(labely)
    plt.grid()
    plt.legend()        
    plt.savefig(chartName + '.png')
    plt.clf()

def BuildBarChart(columns: list[str], values: list, label: str, labely: str, chartName: str):
    #round values to 2 digits
    for i in range(len(values)):
        values[i] = round(values[i], 2)
    plt.figure(figsize=(16,9))
    plt.bar(columns, values, label=label)
    ax = plt.gca()
    ax.bar_label(ax.containers[0])
    plt.ylabel(labely)
    plt.grid()
    plt.legend()
    plt.savefig(chartName + '.png')
    plt.clf()

def DeleteCharts(names: list[str]):
    for name in names:
        os.remove(name + '.png')

def IsChatExist(chatID: str, chatType: str, chatName: str):
    if DBH.ChatExists(chatID):
        return True
    else:
        DBH.AddID(chatID, chatType)
        DBH.AddIDStats(chatID, chatType, chatName)
        DBH.AddIgnoredCurrency(chatID)
        return False

def LoadDataForBot():
    DBH.DBIntegrityCheck()
    LoadCurrencies()
    LoadCrypto()
    LoadFlags()
    LoadSymbols()
    LoadDictionaries()
    LoadTexts()
    ListsCache.SetTokensForW2N()
    ListsCache.SetExceptionsForW2N()


def RegularBackup():
    while True:
        nameOfArch = DBH.CreateAllBackups()
        time.sleep(86400)


def RegularStats():
    while True:
        Stats = DBH.GetSetTimeStats()
        time.sleep(86400)

def save_error_to_file(exception_type, exception_value, exception_traceback):
    with open('error_log.txt', 'a') as file:
        file.write(f"Exception Type: {exception_type}\n")
        file.write(f"Exception Value: {exception_value}\n")
        file.write("Traceback:\n")
        traceback.print_tb(exception_traceback, file=file)

def exception_handler(exception_type, exception_value, exception_traceback):    
    logging.error("An error occurred", exc_info=(exception_type, exception_value, exception_traceback))    
    save_error_to_file(exception_type, exception_value, exception_traceback)


if __name__ == '__main__':
    sys.excepthook = exception_handler

    logging.basicConfig(
        level=logging.ERROR,  
        filename='error_log.txt',  
        filemode='w',  
        format='\n=================================\n%(asctime)s - %(levelname)s - %(message)s'  
    )

    LoadDataForBot()    
    
    if len(sys.argv) == 3:
        if not CheckArgument(sys.argv[1], sys.argv[2]):
            Print("Error arg.", "E")
            sys.exit()
    elif len(sys.argv) == 5 and sys.argv[1] != sys.argv[3]:
        if not CheckArgument(sys.argv[1], sys.argv[2]):
            Print("Error arg.", "E")
            sys.exit()
        elif not CheckArgument(sys.argv[3], sys.argv[4]):
            Print("Error arg.", "E")
            sys.exit()
    elif len(sys.argv) == 7 and sys.argv[1] != sys.argv[3] and sys.argv[1] != sys.argv[2] and sys.argv[2] != sys.argv[3]:
        if not CheckArgument(sys.argv[1], sys.argv[2]):
            Print("Error arg.", "E")
            sys.exit()
        elif not CheckArgument(sys.argv[3], sys.argv[4]):
            Print("Error arg.", "E")
            sys.exit()
        elif not CheckArgument(sys.argv[5], sys.argv[6]):
            Print("Error arg.", "E")
            sys.exit()
    elif len(sys.argv) == 5 and not sys.argv[1] != sys.argv[3] or len(sys.argv) == 7 and not (sys.argv[1] != sys.argv[3] and sys.argv[1] != sys.argv[2] and sys.argv[2] != sys.argv[3]):
        Print("Error. Duplicate argument.", "E")
        sys.exit()

    ThreadUpdateExchangeRates = Thread(target=SheduleUpdate)
    ThreadUpdateExchangeRates.start()
    ThreadUpdateCryptoRates = Thread(target=SheduleCryptoUpdate)
    ThreadUpdateCryptoRates.start()
    ThreadRegularBackup = Thread(target=RegularBackup)
    ThreadRegularBackup.start()
    ThreadRegularStats = Thread(target=RegularStats)
    ThreadRegularStats.start()
    ThreadBlackList = Thread(target=LoadBlackList)
    ThreadBlackList.start()
    executor.start_polling(dp, skip_updates=IsUpdate())
