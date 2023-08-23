import sqlite3 as sql
import sys
import os
from typing import Set
import json
import zipfile
import datetime
import json

from NewPrint import Print

listOfTables = ["SettingsGroups", "SettingsPrivateChats", "ExchangeRates", "SettingsExchangeRates", "CryptoRates", "SettingsCryptoRates", "IgnoredCurrencies"]
listOfServiceTables = ["AdminsList", "BlackList"]
listOfStatsTables = ["ChatsTimeStats", "ChatsUsage", "ProcessedCurrencies", "NewProcessedCurrencies"]

with open('Dictionaries/crypto.json') as json_file:
    cryptoData = json.load(json_file)
    
with open('Dictionaries/currencies.json') as json_file:
    currenciesData = json.load(json_file)

def CreateFileBackup(filePath: str):
    if os.path.exists("Backups"):
        pass
    else:
        Print("Folder 'Backups' not found.", "E")
        os.mkdir("Backups")
        Print("Folder 'Backups' is created", "S")
    today = datetime.datetime.today()
    dt = today.strftime("%Y-%m-%d-%H.%M.%S")
    nameOfDB = filePath.find("/")
    nameOfDB = filePath[filePath + 1:-7]
    nameOfArch = 'Backups/' + nameOfDB + '-' + dt + '.zip'
    zipArch = zipfile.ZipFile(nameOfArch, 'w')
    try:
        zipArch.write(filePath)
        zipArch.close()
        Print(filePath + " added to " + nameOfArch, "S")
    except:
        Print("Cannot add " + filePath + " to archive.", "E")

def CreateAllBackups() -> str:
    if os.path.exists("Backups"):
        pass
    else:
        Print("Folder 'Backups' not found.", "E")
        os.mkdir("Backups")
        Print("Folder 'Backups' is created", "S")
    today = datetime.datetime.today()
    dt = today.strftime("%Y-%m-%d-%H.%M.%S")
    nameOfArch = 'Backups/backup-' + dt + '.zip'
    zipArch = zipfile.ZipFile(nameOfArch, 'w')
    try:
        zipArch.write("DataBases/DataForBot.sqlite")
        zipArch.write("DataBases/ServiceData.sqlite")
        zipArch.write("DataBases/StatsData.sqlite")
        zipArch.close()
        Print("Backup " + nameOfArch + " created.", "S")
    except:
        Print("Cannot create archive.", "E")
    return nameOfArch

def DBIntegrityCheck():
    if os.path.exists("DataBases/DataForBot.sqlite"):
        # Connect to DB
        con = sql.connect('DataBases/DataForBot.sqlite')
        cursor = con.cursor()
        Print("Connected to main DB successfully.", 'S')

        # Check SettingsCryptoRates integrity
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='SettingsCryptoRates';")
        table_exists = cursor.fetchone()

        if table_exists:
            # Fetch existing columns
            cursor.execute('PRAGMA table_info(SettingsCryptoRates);')
            existing_columns = [column[1] for column in cursor.fetchall()]

            # Iterate over the data in the JSON file
            for crypto in cryptoData['crypto']:
                column_name = crypto['code']

                # If the column does not exist in the table, add it
                if column_name not in existing_columns:
                    Print(f"Column {column_name} does not exist in SettingsCryptoRates table. Adding it now.", "S")
                    cursor.execute(f'ALTER TABLE SettingsCryptoRates ADD COLUMN {column_name} INTEGER DEFAULT 0;')
            
            # Iterate over the existing columns
            for column in existing_columns:
                # If the column is not present in the JSON file, delete it
                if column == "chatID":
                    continue
                if column not in [crypto['code'] for crypto in cryptoData['crypto']]:
                    Print(f"Column {column} does not exist in JSON file. Deleting it now from SettingsCryptoRates.", "S")
                    cursor.execute(f'ALTER TABLE SettingsCryptoRates DROP COLUMN {column};')
        else:
            # Table does not exist, create it with all required columns
            columns = ', '.join([f"{crypto['code']} INTEGER DEFAULT 0" for crypto in cryptoData['crypto']])
            cursor.execute(f"""
                CREATE TABLE SettingsCryptoRates (
                    chatID INTEGER NOT NULL PRIMARY KEY,
                    {columns}
                );
            """)
        
        # check currencies
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='SettingsExchangeRates';")
        table_exists = cursor.fetchone()

        if table_exists:
            # Fetch existing columns
            cursor.execute('PRAGMA table_info(SettingsExchangeRates);')
            existing_columns = [column[1] for column in cursor.fetchall()]

            # Iterate over the data in the JSON file
            for currency in currenciesData['currencies']:
                column_name = '_'+currency['code']

                # If the column does not exist in the table, add it
                if column_name not in existing_columns:
                    Print(f"Column {column_name} does not exist in SettingsExchangeRates table. Adding it now.", "S")
                    cursor.execute(f'ALTER TABLE SettingsExchangeRates ADD COLUMN {column_name} INTEGER DEFAULT 0;')
            # Iterate over the existing columns
            for column in existing_columns:
                # Skip the "chatID" column
                if column == "chatID":
                    continue

                # If the column is not present in the JSON file, delete it
                if column not in ['_' + currency['code'] for currency in currenciesData['currencies']]:
                    Print(f"Column {column} does not exist in JSON file. Deleting it now from SettingsExchangeRates.", "S")
                    cursor.execute(f'ALTER TABLE SettingsExchangeRates DROP COLUMN {column};')
        else:
            # Table does not exist, create it with all required columns
            columns = ', '.join([f"{'_'+currency['code']} INTEGER DEFAULT 0" for currency in currenciesData['currencies']])
            cursor.execute(f"""
                CREATE TABLE SettingsExchangeRates (
                    chatID INTEGER NOT NULL PRIMARY KEY,
                    {columns}
                );
            """)
        
        # check IgnoredCurrencies integrity
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='IgnoredCurrencies';")
        table_exists = cursor.fetchone()

        if table_exists:
            # Fetch existing columns
            cursor.execute('PRAGMA table_info(IgnoredCurrencies);')
            existing_columns = [column[1] for column in cursor.fetchall()]

            # Iterate over the data in the JSON file
            for currency in currenciesData['currencies']:
                column_name = '_'+currency['code']

                # If the column does not exist in the table, add it
                if column_name not in existing_columns:
                    Print(f"Column {column_name} does not exist in IgnoredCurrencies table. Adding it now.", "S")
                    cursor.execute(f'ALTER TABLE IgnoredCurrencies ADD COLUMN {column_name} INTEGER DEFAULT 0;')

            for currency in cryptoData['crypto']:
                column_name = '_'+currency['code']

                # If the column does not exist in the table, add it
                if column_name not in existing_columns:
                    Print(f"Column {column_name} does not exist in IgnoredCurrencies table. Adding it now.", "S")
                    cursor.execute(f'ALTER TABLE IgnoredCurrencies ADD COLUMN {column_name} INTEGER DEFAULT 0;')
             # Get the columns to remove
            columns_to_remove = [column for column in existing_columns if column not in ['_' + currency['code'] for currency in currenciesData['currencies']] and column not in ['_' + crypto['code'] for crypto in cryptoData['crypto']] and column != 'chatID']

            # Iterate over the columns to remove
            for column in columns_to_remove:
                Print(f"Column {column} does not exist in JSON file. Deleting it now from IgnoredCurrencies.", "S")
                cursor.execute(f'ALTER TABLE IgnoredCurrencies DROP COLUMN {column};')

        else:
            # Table does not exist, create it with all required columns
            Print("Table IgnoredCurrencies does not exist. Creating it now.", "S")
            columns = ', '.join([f"{'_'+currency['code']} INTEGER DEFAULT 0" for currency in currenciesData['currencies']])
            columns += ', ' + ', '.join([f"{'_'+crypto['code']} INTEGER DEFAULT 0" for crypto in cryptoData['crypto']])
            cursor.execute(f"""
                CREATE TABLE IgnoredCurrencies (
                    chatID INTEGER NOT NULL PRIMARY KEY,
                    {columns}
                );
            """)
        
        # insert or ignore every row from SettingsExchangeRates with default values
        cursor.execute("SELECT * FROM SettingsExchangeRates;")
        rows = cursor.fetchall()
        for row in rows:
            chatID = row[0]
            cursor.execute(f"INSERT OR IGNORE INTO IgnoredCurrencies (chatID) VALUES ({chatID});")

        # check SettingsGroups integrity
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='SettingsGroups';")
        table_exists = cursor.fetchone()
        expected_columns = {
            "chatID": {"type": "INTEGER", "default": "NULL PRIMARY KEY"},
            "deleteRules": {"type": "TEXT", "default": "'admins'"},
            "deleteButton": {"type": "INTEGER", "default": "1"},
            "editSettings": {"type": "TEXT", "default": "'admins'"},
            "flags": {"type": "INTEGER", "default": "1"},
            "currencySymbol": {"type": "INTEGER", "default": "1"},
            "lang": {"type": "TEXT", "default": "'en'"}
        }
        if table_exists:
            # Fetch existing columns
            cursor.execute('PRAGMA table_info(SettingsGroups);')
            existing_columns = [column[1] for column in cursor.fetchall()]

            # iterate over expected columns
            for column_name, column_properties in expected_columns.items():
                # If the column does not exist in the table, add it
                if column_name not in existing_columns:
                    Print(f"Column {column_name} does not exist in SettingsGroups table. Adding it now.", "S")
                    cursor.execute(f'''ALTER TABLE SettingsGroups ADD COLUMN {column_name} {column_properties["type"]} DEFAULT {column_properties["default"]};''')
        else:
            # Table does not exist, create it with all required columns
            columns = ', '.join([f"{column_name} {column_properties['type']} DEFAULT {column_properties['default']}" for column_name, column_properties in expected_columns.items()])
            cursor.execute(f"""
                CREATE TABLE SettingsGroups (
                    {columns}
                );
            """)
        
        # Check SettingsPrivateChats integrity
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='SettingsPrivateChats';")
        table_exists = cursor.fetchone()
        expected_columns = {
            "chatID": {"type": "INTEGER", "default": "NULL PRIMARY KEY"},
            "deleteButton": {"type": "INTEGER", "default": "1"},
            "flags": {"type": "INTEGER", "default": "1"},
            "currencySymbol": {"type": "INTEGER", "default": "1"},
            "lang": {"type": "TEXT", "default": "'en'"}
        }
        if table_exists:
            # Fetch existing columns
            cursor.execute('PRAGMA table_info(SettingsPrivateChats);')
            existing_columns = [column[1] for column in cursor.fetchall()]

            # iterate over expected columns
            for column_name, column_properties in expected_columns.items():
                # If the column does not exist in the table, add it
                if column_name not in existing_columns:
                    print(f"Column {column_name} does not exist in SettingsPrivateChats table. Adding it now.", "S")
                    cursor.execute(f'''ALTER TABLE SettingsPrivateChats ADD COLUMN {column_name} {column_properties["type"]} DEFAULT {column_properties["default"]};''')
        else:
            # Table does not exist, create it with all required columns
            columns = ', '.join([f"{column_name} {column_properties['type']} DEFAULT {column_properties['default']}" for column_name, column_properties in expected_columns.items()])
            cursor.execute(f"""
                CREATE TABLE SettingsPrivateChats (
                    {columns}
                );
            """)
            
        # Getting all names of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        listNames = cursor.fetchall()
        for i in range(len(listNames)):
            listNames[i] = listNames[i][0]

        for i in listOfTables:
            if not i in listNames:
                CreateFileBackup("DataBases/DataForBot.sqlite")
                os.remove('DataBases/DataForBot.sqlite')
                Print("Error. Main database is corrupted. 'DataForBot.sqlite' was backuped and deleted. New database will be create automatically.", "E")

                CreateDataBaseTemplate()
                break
        
        # Get a list of all tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            if table_name not in listOfTables:
                cursor.execute("DROP TABLE IF EXISTS " + table_name + ";")
                Print("Table " + table_name + " removed.", "W")


        # Commit the changes and close the connection
        con.commit()
        con.close() 

        
        
        Print("Main DB is OK.", "S")
    else:
        Print("Connected to main DB unsuccessfully.", "E")
        CreateDataBaseTemplate()

    if os.path.exists("DataBases/ServiceData.sqlite"):
        # Connect to DB
        con = sql.connect('DataBases/ServiceData.sqlite')
        cursor = con.cursor()
        Print("Connected to service DB successfully.", "S")

        # Getting all names of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        listNames = cursor.fetchall()
        for i in range(len(listNames)):
            listNames[i] = listNames[i][0]

        for i in listOfServiceTables:
            if not i in listNames:
                CreateFileBackup("DataBases/ServiceData.sqlite")
                os.remove('DataBases/ServiceData.sqlite')
                Print("Error. Service database is corrupted. 'ServiceData.sqlite' was backuped and deleted. New database will be create automatically.", "E")

                CreateServiceDataBase()
                break
        # Get a list of all tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            if table_name not in listOfServiceTables:
                cursor.execute("DROP TABLE IF EXISTS " + table_name + ";")
                Print("Table " + table_name + " removed.", "W")
        
        # Commit the changes and close the connection
        con.commit()
        con.close() 

        
        Print("Service DB is OK.", "S")
    else:
        Print("Connected to service DB unsuccessfully.", "E")
        CreateServiceDataBase()

    if os.path.exists("DataBases/StatsData.sqlite"):
        con = sql.connect("DataBases/StatsData.sqlite")
        cursor = con.cursor()
        Print("Connected to stats DB successfully.", "S")

        
        # check ProcessedCurrencies columns
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ProcessedCurrencies';")
        table_exists = cursor.fetchone()

        if table_exists:
            # Fetch existing columns
            cursor.execute('PRAGMA table_info(ProcessedCurrencies);')
            existing_columns = [column[1] for column in cursor.fetchall()]

            # Iterate over the data in the JSON file
            for crypto in cryptoData['crypto']:
                column_name = "_"+crypto['code']

                # If the column does not exist in the table, add it
                if column_name not in existing_columns:
                    Print(f"Adding column {column_name} to ProcessedCurrencies table", "S")
                    cursor.execute(f'ALTER TABLE ProcessedCurrencies ADD COLUMN {column_name} INTEGER DEFAULT 0;')
            
            for currency in currenciesData['currencies']:
                column_name = "_"+currency['code']

                # If the column does not exist in the table, add it
                if column_name not in existing_columns:
                    Print(f"Adding column {column_name} to ProcessedCurrencies table", "S")
                    cursor.execute(f'ALTER TABLE ProcessedCurrencies ADD COLUMN {column_name} INTEGER DEFAULT 0;')

        # check ChatsUsage columns
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ChatsUsage';")
        table_exists = cursor.fetchone()

        if table_exists:
            # Fetch existing columns
            cursor.execute('PRAGMA table_info(ChatsUsage);')
            existing_columns = [column[1] for column in cursor.fetchall()]
            expected_columns = ["chatID", "chatType", "chatName", "timeAdded", "lastTimeUse"]

            for column in expected_columns:
                if column not in existing_columns:
                    Print(f"Adding column {column} to ChatsUsage table", "S")
                    cursor.execute(f'ALTER TABLE ChatsUsage ADD COLUMN {column} TEXT;')
        else:
            Print("Creating ChatsUsage table", "S")
            cursor.execute("""
                CREATE TABLE ChatsUsage (
                    chatID INTEGER NOT NULL PRIMARY KEY,
                    chatType TEXT,
                    chatName TEXT,
                    timeAdded TEXT,
                    lastTimeUse TEXT
                           );""")
            
        # check NewProcessedCurrencies columns
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='NewProcessedCurrencies';")
        table_exists = cursor.fetchone()

        if table_exists:
            # Fetch existing columns
            cursor.execute('PRAGMA table_info(NewProcessedCurrencies);')
            existing_columns = [column[1] for column in cursor.fetchall()]
            expected_columns = ["date", "chatID", "userID", "lang", "convertedFrom", "convertedTo", "deleted", "deletedDate", "messageID"]

            for column in expected_columns:
                if column not in existing_columns:
                    Print(f"Adding column {column} to NewProcessedCurrencies table", "S")
                    cursor.execute(f'ALTER TABLE NewProcessedCurrencies ADD COLUMN {column} TEXT;')
        else:
            Print("Creating NewProcessedCurrencies table", "S")
            cursor.execute("""
                CREATE TABLE NewProcessedCurrencies (
                    date TEXT,
                    chatID INTEGER NOT NULL,
                    userID INTEGER DEFAULT 0,
                    lang TEXT,
                    convertedFrom TEXT,
                    convertedTo TEXT,
                    deleted INTEGER DEFAULT 0,
                    deletedDate TEXT,
                    messageID INTEGER NOT NULL
                           );""")
            
            
        # Get a list of all tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            if table_name not in listOfStatsTables:
                cursor.execute("DROP TABLE IF EXISTS " + table_name + ";")
                Print("Table " + table_name + " removed.", "W")
        
        # Commit the changes and close the connection
        con.commit()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        listNames = cursor.fetchall()
        for i in range(len(listNames)):
            listNames[i] = listNames[i][0]

        for i in listOfStatsTables:
            if not i in listNames:
                CreateFileBackup("DataBases/StatsData.sqlite")
                os.remove("DataBases/StatsData.sqlite")
                Print("Error. Stats database is corrupted. 'StatsData.sqlite' was backuped and deleted. New database will be create automatically.", "E")
                CreateStatsDataBase()
                break

        con.close() 
        Print("Stats DB is OK.", "S")
    else:
        Print("Connected to stats DB unsuccessfully.", "E")
        CreateStatsDataBase()


def CreateStatsDataBase():
    Print("Creating stats DB is starting...", "S")
    # Connect to DB
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    with con:
        con.execute("""
            CREATE TABLE ChatsUsage (
                chatID INTEGER NOT NULL PRIMARY KEY,
                chatType TEXT,
                chatName TEXT,
                timeAdded TEXT,
                lastTimeUse TEXT
            );
        """)

    with con:
        con.execute("""
            CREATE TABLE ChatsTimeStats (
                date TEXT,
                privateChatsAmount INTEGER DEFAULT 0,
                groupChatsAmount INTEGER DEFAULT 0,
                activeWeekPrivateChats INTEGER DEFAULT 0,
                activeWeekGroupChats INTEGER DEFAULT 0,
                activeMonthPrivateChats INTEGER DEFAULT 0,
                activeMonthGroupChats INTEGER DEFAULT 0
            );
        """)

    with con:
        con.execute("""
            CREATE TABLE NewProcessedCurrencies (
                date TEXT,
                chatID INTEGER NOT NULL,
                userID INTEGER DEFAULT 0,
                lang TEXT,
                convertedFrom TEXT,
                convertedTo TEXT,
                deleted INTEGER DEFAULT 0,
                deletedDate TEXT,
                messageID INTEGER NOT NULL
            );
        """)


    currencyCodes = [currency['code'] for currency in currenciesData['currencies']]
    currencyCodes = ', '.join([f"_{currency} INTEGER DEFAULT 0" for currency in currencyCodes])


    cryptoCodes = [crypto['code'] for crypto in cryptoData['crypto']]
    cryptoCodes = ', '.join([f"_{crypto} INTEGER DEFAULT 0" for crypto in cryptoCodes])
    with con:
        con.execute(f"""
            CREATE TABLE ProcessedCurrencies (
                date TEXT,
                chatID INTEGER,
                userID INTEGER,
                proccesedCurrency TEXT,
                message TEXT,
                {currencyCodes},
                {cryptoCodes}
            );
        """)

    con.close()
    Print("Stats DB is created.", "S")


def CreateServiceDataBase():
    if os.path.exists("DataBases"):
        pass
    else:
        Print("Folder 'DataBases' not found", "E")
        sys.exit(1)
    Print("Creating service DB is starting...", "S")
    # Connect to DB
    con = sql.connect('DataBases/ServiceData.sqlite')
    cursor = con.cursor()

    with con:
        con.execute("""
            CREATE TABLE AdminsList (
                adminID INTEGER NOT NULL PRIMARY KEY 
            );
        """)

    with con:
        con.execute("""
            CREATE TABLE BlackList (
                userID INTEGER NOT NULL PRIMARY KEY ,
                banDate TEXT DEFAULT 0,
                chatID INTEGER DEFAULT 0,
                chatName TEXT DEFAULT 0
            );
        """)

    # with con:
    #     con.execute("""
    #         CREATE TABLE Reports (
    #             date TEXT,
    #             chatID INTEGER DEFAULT 0,
    #             userID INTEGER DEFAULT 0,
    #             message TEXT,
    #             reply TEXT
    #         );
    #     """)

    con.close()
    Print("Service DB is created.", "S")


def CreateDataBaseTemplate():
    if os.path.exists("DataBases"):
        pass
    else:
        Print("Folder 'DataBases' not found", "E")
        os.mkdir("DataBases")
        Print("Folder 'DataBases' is created", "S")
    Print("Creating main DB is starting...", "S")
    # Connect to DB
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()

    with con:
        con.execute("""
            CREATE TABLE SettingsGroups (
                chatID INTEGER NOT NULL PRIMARY KEY ,
                deleteRules TEXT DEFAULT admins,
                deleteButton INTEGER DEFAULT 1,
                editSettings TEXT DEFAULT admins,
                flags INTEGER DEFAULT 1,
                currencySymbol INTEGER DEFAULT 1,
                lang TEXT DEFAULT en
            );
        """)
    with con:
        con.execute("""
            CREATE TABLE SettingsPrivateChats (
                chatID INTEGER NOT NULL PRIMARY KEY ,
                deleteButton INTEGER DEFAULT 1,
                flags INTEGER DEFAULT 1,
                currencySymbol INTEGER DEFAULT 1,
                lang TEXT DEFAULT en
            );
        """)
    with con:
        con.execute("""
            CREATE TABLE ExchangeRates (
                currency TEXT NOT NULL PRIMARY KEY,
                flag TEXT,
                exchangeRates FLOAT
            );
        """)
    with con:
        con.execute("""
            CREATE TABLE CryptoRates (
                currency TEXT NOT NULL PRIMARY KEY,
                flag TEXT,
                exchangeRates FLOAT
            );
        """)

    # use codes from json. ETH and BTC are default
    cryptoCodes = [crypto['code'] for crypto in cryptoData['crypto']]
    with con:
        con.execute(f"""
            CREATE TABLE SettingsCryptoRates (
                chatID INTEGER NOT NULL PRIMARY KEY,
                {', '.join([f"{code} INTEGER DEFAULT {int(code == 'ETH' or code == 'BTC')}" for code in cryptoCodes])}
            );
        """)

    # use codes from json
    currencyCodes = [currency['code'] for currency in currenciesData['currencies']]

    with con:
        con.execute(f"""
            CREATE TABLE SettingsExchangeRates (
                chatID INTEGER NOT NULL PRIMARY KEY ,
                {', '.join([f"{'_'+code} INTEGER DEFAULT {int(code in ['USD','EUR','UAH','GBP','PLN'])}" for code in currencyCodes])}
            );
        """)

    # create ignored currencies table
    with con:
        con.execute(f"""
            CREATE TABLE IgnoredCurrencies (
                chatID INTEGER NOT NULL PRIMARY KEY ,
                {', '.join([f"{'_'+code} INTEGER DEFAULT 0" for code in currencyCodes])} ,
                {', '.join([f"{'_'+code} INTEGER DEFAULT 0" for code in cryptoCodes])}
            );
        """)
    con.close()
    Print("Main DB is created.", "S")


def AddID(chatID: str, chatType: str):
    chatID = int(chatID)
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO SettingsExchangeRates (chatID) values (?)", tuple([chatID]))
    cursor.execute(
        "INSERT OR IGNORE INTO SettingsCryptoRates (chatID) values (?)", tuple([chatID]))
    if chatType == "group" or chatType == "supergroup":
        cursor.execute(
            "INSERT OR IGNORE INTO SettingsGroups (chatID) values (?)", tuple([chatID]))
    else:
        cursor.execute(
            "INSERT OR IGNORE INTO SettingsPrivateChats (chatID) values (?)", tuple([chatID]))
    con.commit()


def SetSetting(chatID: str, key: str, val: str, chatType: str):
    chatID = int(chatID)
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    try:
        if chatType == "group" or chatType == "supergroup":
            cursor.execute("UPDATE OR ABORT SettingsGroups SET "+str(key)+" = ? WHERE chatID = ?", (val, chatID))
        else:
            cursor.execute("UPDATE OR ABORT SettingsPrivateChats SET "+str(key)+" = ? WHERE chatID = ?", (val, chatID))
        con.commit()
    except:
        Print("No such column. Cannot find '" + str(key) + "'. Error in 'SetSetting'.", "E")


def SetCurrencySetting(chatID: str, currency: str, val: str):
    chatID = int(chatID)
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    try:
        cursor.execute("UPDATE OR ABORT SettingsExchangeRates SET " + "_"+str(currency)+"= "+str(val)+" WHERE chatID = "+str(chatID))
        con.commit()
    except:
        Print("No such column. Cannot find '" + str(currency) + "'. Error in 'SetCurrencySetting'.", "E")

def ReverseCurrencySetting(chatID: str, currency: str):
    chatID = int(chatID)
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    try:
        cursor.execute("SELECT "+ "_"+str(currency) + " from SettingsExchangeRates WHERE chatID = "+str(chatID))
        res = cursor.fetchone()
        cursor.execute("UPDATE OR ABORT SettingsExchangeRates SET " + "_"+str(currency)+"= "+str(int(not res[0]))+" WHERE chatID = "+str(chatID))
        con.commit()
    except:
        try:
            cursor.execute("SELECT "+str(currency) + " from SettingsCryptoRates WHERE chatID = "+str(chatID))
            res = cursor.fetchone()
            cursor.execute("UPDATE OR ABORT SettingsCryptoRates SET " + str(currency)+"= "+str(int(not res[0]))+" WHERE chatID = "+str(chatID))
            con.commit()
        except:
            Print("No such column. Cannot find '" + str(currency) + "'. Error in 'ReverseCurrencySetting'.", "E")

def SetCryptoSetting(chatID: str, crypto: str, val: str):
    chatID = int(chatID)
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    try:
        cursor.execute("UPDATE OR ABORT SettingsCryptoRates SET " +str(crypto)+"= "+str(val)+" WHERE chatID = "+str(chatID))
        con.commit()
    except:
        Print("No such column. Cannot find '" + str(crypto) + "'. Error in 'SetCryptoSetting'.", "E")

def AddIgnoredCurrency(chatID: str):
    chatID = int(chatID)
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO IgnoredCurrencies (chatID) values (?)", tuple([chatID]))
    con.commit()

def SetIgnoredCurrency(chatID: str, currency: str, val: int):
    chatID = int(chatID)
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    try:
        cursor.execute("UPDATE OR ABORT IgnoredCurrencies SET " + "_"+str(currency)+"= "+str(val)+" WHERE chatID = "+str(chatID))
        con.commit()
    except:
        Print("No such column. Cannot find '" + str(currency) + "'. Error in 'SetIgnoredCurrency'.", "E")

def GetIgnoredCurrency(chatID: str, currency: str) -> bool:
    chatID = int(chatID)
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    try:
        cursor.execute("SELECT "+ "_"+str(currency) + " from IgnoredCurrencies WHERE chatID = "+str(chatID))
        res = cursor.fetchone()
        return bool(res[0])
    except:
        Print("No such column. Cannot find '" + str(currency) + "'. Error in 'GetIgnoredCurrency'.", "E")
        return False

def GetIgnoredCurrencies(chatID: str) -> list:
    chatID = int(chatID)
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    try:
        cursor.execute("SELECT * from IgnoredCurrencies WHERE chatID = ?", (chatID,))
        res = cursor.fetchone()
        if res is not None:
            column_names = [column[0].replace('_', '') for column, value in zip(cursor.description, res) if value == 1]
            return column_names
        else:
            Print("No such column. Cannot find '" + str(chatID) + "'. Error in 'GetIgnoredCurrencies'.","E")
            return []
    except Exception as e:
        Print("Error:"+e, "E")
        return []
    
def ReverseIgnoredCurrency(chatID: str, currency: str):
    chatID = int(chatID)
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    try:
        cursor.execute("SELECT "+ "_"+str(currency) + " from IgnoredCurrencies WHERE chatID = "+str(chatID))
        res = cursor.fetchone()
        cursor.execute("UPDATE OR ABORT IgnoredCurrencies SET " + "_"+str(currency)+"= "+str(int(not res[0]))+" WHERE chatID = "+str(chatID))
        con.commit()
    except:
        Print("No such column. Cannot find '" + str(currency) + "'. Error in 'ReverseIgnoredCurrency'.", "E")

def GetAllSettings(chatID: str, chatType: str) -> dict:
    chatID = int(chatID)
    con = sql.connect('DataBases/DataForBot.sqlite')
    con.row_factory = sql.Row
    cursor = con.cursor()
    try:
        if chatType == "group" or chatType == "supergroup":
            cursor.execute(
                "SELECT * from SettingsGroups WHERE chatID = "+str(chatID))
            res = cursor.fetchone()
        else:
            cursor.execute(
                "SELECT * from SettingsPrivateChats WHERE chatID = "+str(chatID))
            res = cursor.fetchone()
        return dict(res)
    except:
        Print("No such column. Cannot find '" + str(chatID) + "'. Error in 'GetAllSettings'.", "E")
        return None


def GetSetting(chatID: str, key: str, chatType: str) -> str:
    chatID = int(chatID)
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    try:
        if chatType == "group" or chatType == "supergroup":
            cursor.execute("SELECT "+str(key) +
                            " from SettingsGroups WHERE chatID = "+str(chatID))
            res = cursor.fetchone()
        else:
            cursor.execute(
                "SELECT "+str(key)+" from SettingsPrivateChats WHERE chatID = "+str(chatID))
            res = cursor.fetchone()
        return res[0]
    except:
        Print("No such column. Cannot find '" + str(key) + "'. Error in 'GetSetting'.", "E")
        return None


def GetAllCurrencies(chatID: str) -> list:
    chatID = int(chatID)
    con = sql.connect('DataBases/DataForBot.sqlite')
    con.row_factory = sql.Row
    cursor = con.cursor()
    try:
        cursor.execute(
            "SELECT * FROM SettingsExchangeRates WHERE chatID = "+str(chatID))
        res = dict(cursor.fetchone())
        return sorted([k[1:] for k, v in res.items() if v == 1])
    except:
        Print("No such column. Cannot find '" + str(chatID) + "'. Error in 'GetAllCurrencies'.", "E")
        return None


def GetAllCrypto(chatID: str) -> list:
    chatID = int(chatID)
    con = sql.connect('DataBases/DataForBot.sqlite')
    con.row_factory = sql.Row
    cursor = con.cursor()
    try:
        cursor.execute(
            "SELECT * FROM SettingsCryptoRates WHERE chatID = "+str(chatID))
        res = dict(cursor.fetchone())
        return sorted([k[0:] for k, v in res.items() if v == 1])
    except:
        Print("No such column. Cannot find '" + str(chatID) + "'. Error in 'GetAllCrypto'.", "E")
        return None


def ChatExists(chatID: str) -> int:
    chatID = int(chatID)
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    cursor.execute(
        "SELECT EXISTS(SELECT 1 FROM SettingsExchangeRates WHERE chatID = "+str(chatID)+")")
    res = cursor.fetchone()
    return res[0]


def IsBlacklisted(userID: str) -> int:
    userID = int(userID)
    con = sql.connect('DataBases/ServiceData.sqlite')
    cursor = con.cursor()
    cursor.execute(
        "SELECT EXISTS(SELECT 1 FROM BlackList WHERE userID = "+str(userID)+")")
    res = cursor.fetchone()
    return res[0]


def ClearBlacklist(userID: str):
    userID = int(userID)
    con = sql.connect('DataBases/ServiceData.sqlite')
    cursor = con.cursor()
    if userID == 0:
        cursor.execute("DELETE FROM BlackList")
        con.commit()
        cursor.execute("VACUUM")
        con.commit()
        return 1
    else:
        try:
            cursor.execute("DELETE FROM BlackList WHERE userID = "+str(userID))
            con.commit()
            return 1
        except:
            Print("No such column. Cannot find '" + str(userID) + "'. Error in 'ClearBlacklist'.", "E")
            return None


def AddBlacklist(userID: str, chatID: str = 0, chatName: str = ""):
    chatID = int(chatID)
    con = sql.connect('DataBases/ServiceData.sqlite')
    cursor = con.cursor()
    cursor.execute("INSERT OR IGNORE INTO BlackList (userID,chatID,chatName,banDate) values (?,?,?,DATETIME())", tuple(
        [userID, chatID, chatName]))
    con.commit()


def GetBlacklist() -> list:
    con = sql.connect('DataBases/ServiceData.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT * from BlackList")
    res = cursor.fetchall()
    return [k[0] for k in res]


def GetAdmins() -> list:
    con = sql.connect('DataBases/ServiceData.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT * from AdminsList")
    res = cursor.fetchall()
    return [k[0] for k in res]


def IsAdmin(adminID: str) -> int:
    adminID = int(adminID)
    con = sql.connect('DataBases/ServiceData.sqlite')
    cursor = con.cursor()
    cursor.execute(
        "SELECT EXISTS(SELECT 1 FROM AdminsList WHERE adminID = "+str(adminID)+")")
    res = cursor.fetchone()
    return res[0]


def AddAdmin(adminID: str):
    adminID = int(adminID)
    con = sql.connect('DataBases/ServiceData.sqlite')
    cursor = con.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO AdminsList (adminID) values ("+str(adminID)+")")
    con.commit()


def ClearAdmins(adminID: str):
    adminID = int(adminID)
    con = sql.connect('DataBases/ServiceData.sqlite')
    cursor = con.cursor()
    if adminID == 0:
        cursor.execute("DELETE FROM AdminsList")
        con.commit()
        return 1
    else:
        try:
            cursor.execute(
                "DELETE FROM AdminsList WHERE adminID = "+str(adminID))
            con.commit()
            return 1
        except:
            Print("No such adminID. Cannot find '" + str(adminID) + "'. Error in 'ClearAdmins'.", "E")
            return None


def GetListOfCurrencies() -> list:
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.execute("SELECT * FROM SettingsExchangeRates")
    names = [description[0] for description in cursor.description]
    names.pop(0)
    return sorted([i[1:] for i in names])


def GetListOfCrypto() -> list:
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.execute("SELECT * FROM SettingsCryptoRates")
    names = [description[0] for description in cursor.description]
    names.pop(0)
    return [i[0:] for i in names]


def UpdateExchangeRatesDB(exchangeRates: dict):
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    f = open("Dictionaries/currencies.json", encoding="utf-8")
    data = json.load(f)
    for cur, rate in exchangeRates.items():
        flag = next(
            (item for item in data['currencies'] if item['code'] == cur), None)
        try:
            cursor.execute("INSERT OR REPLACE INTO ExchangeRates (currency,flag,exchangeRates) values ('" +
                           cur+"','"+flag["emoji"]+"',?)", tuple([rate]))
        except:
            continue
    con.commit()


def UpdateCryptoRatesDB(cryptoRates: dict):
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    for cur, rate in cryptoRates.items():
        cursor.execute("INSERT OR REPLACE INTO CryptoRates (currency,flag,exchangeRates) values ('" +cur+"','"+""+"',?)", tuple([rate]))
    con.commit()


def AddIDStats(chatID: str, chatType: str, chatName: str):
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    cursor.execute("INSERT OR IGNORE INTO ChatsUsage (chatID, chatType, timeAdded, lastTimeUse, chatName) values ("+str(chatID)+",'"+chatType+"',DATETIME(),DATETIME(),'"+chatName+"')")
    con.commit()


def UpdateChatUsage(chatID: str):
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    cursor.execute(
        "UPDATE ChatsUsage SET lastTimeUse = DATETIME() WHERE chatID = "+str(chatID))
    con.commit()

def GetChatsAmount() -> dict:
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM ChatsUsage WHERE chatType = 'private'")
    res = {}
    res['private'] = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM ChatsUsage WHERE chatType = 'group' OR chatType = 'supergroup'")
    res['groups'] = cursor.fetchone()[0]
    return res

def GetGroupChatIDs() -> list:
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT * from SettingsGroups")
    res = cursor.fetchall()
    return [k[0] for k in res]

def GetPrivateChatIDs() -> list:
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT * from SettingsPrivateChats")
    res = cursor.fetchall()
    return [k[0] for k in res]

def GetSetTimeStats() -> dict:
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM ChatsUsage WHERE chatType = 'private'")
    res = {}
    res['private'] = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM ChatsUsage WHERE chatType = 'group' OR chatType = 'supergroup'")
    res['groups'] = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM ChatsUsage WHERE chatType = 'private' AND lastTimeUse > datetime('now', '-7 days')")
    res['activePrivateWeek'] = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM ChatsUsage WHERE (chatType = 'group' OR chatType ='supergroup' ) AND lastTimeUse > datetime('now', '-7 days')")
    res['activeGroupsWeek'] = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM ChatsUsage WHERE chatType = 'private' AND lastTimeUse > datetime('now', '-1 month')")
    res['activePrivateMonth'] = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM ChatsUsage WHERE (chatType = 'group' OR chatType ='supergroup' ) AND lastTimeUse > datetime('now', '-1 month')")
    res['activeGroupsMonth'] = cursor.fetchone()[0]
    cursor.execute("INSERT INTO ChatsTimeStats (date,privateChatsAmount,groupChatsAmount,activeWeekPrivateChats,activeWeekGroupChats,activeMonthPrivateChats,activeMonthGroupChats) values (DATETIME(),?,?,?,?,?,?)", tuple(res.values()))
    con.commit()
    return res

def GetTimeStats() -> dict:
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM ChatsUsage WHERE chatType = 'private'")
    res = {}
    res['private'] = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM ChatsUsage WHERE chatType = 'group' OR chatType = 'supergroup'")
    res['groups'] = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM ChatsUsage WHERE chatType = 'private' AND lastTimeUse > datetime('now', '-7 days')")
    res['activePrivateWeek'] = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM ChatsUsage WHERE (chatType = 'group' OR chatType ='supergroup' ) AND lastTimeUse > datetime('now', '-7 days')")
    res['activeGroupsWeek'] = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM ChatsUsage WHERE chatType = 'private' AND lastTimeUse > datetime('now', '-1 month')")
    res['activePrivateMonth'] = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM ChatsUsage WHERE (chatType = 'group' OR chatType ='supergroup' ) AND lastTimeUse > datetime('now', '-1 month')")
    res['activeGroupsMonth'] = cursor.fetchone()[0]
    return res

def ProcessedCurrency(chatID: str, userID: str, processedCurrency: str, message: str):
    values_q = [chatID, userID, processedCurrency, message]
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    query = "INSERT INTO ProcessedCurrencies (date, chatID, userID, proccesedCurrency ,message"
    turnedOnCurrencies = GetAllCurrencies(chatID) + GetAllCrypto(chatID)
    try:
        turnedOnCurrencies.remove(processedCurrency)
    except:
        pass
    for cur in turnedOnCurrencies:
        query = query + ", _" + cur
        values_q.append(1)
    query = query+") values (DATETIME(), ?,?,?,?"
    for cur in turnedOnCurrencies:
        query = query + ",?"
    query = query+")"
    cursor.execute(query, tuple(values_q))
    con.commit()

def NewProcessedCurrency(chatID: str, userID: str, lang: str, convertedFrom: str, convertedTo: str, messageID: str):
    values_q = [chatID, userID, lang, convertedFrom, convertedTo, messageID]
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    query = "INSERT INTO NewProcessedCurrencies (date, chatID, userID, lang, convertedFrom, convertedTo, messageID) values (DATETIME(), ?,?,?,?,?,?)"
    cursor.execute(query, tuple(values_q))
    con.commit()

def DeleteProcessedCurrency(chatID: str, messageID: str):
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    # change deleted to true and add deleted date
    cursor.execute("UPDATE NewProcessedCurrencies SET deleted = 1, deletedDate = DATETIME() WHERE chatID = ? AND messageID = ?", (chatID, messageID))
    con.commit()

def GetProcessedCurrencies():
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()

    cursor.execute("SELECT * FROM NewProcessedCurrencies")
    rows = cursor.fetchall()

    records_list = []

    for row in rows:
        record_dict = {
            'date': row[0],
            'chatID': row[1],
            'userID': row[2],
            'lang': row[3],
            'convertedFrom': row[4],
            'convertedTo': row[5],
            'deleted': row[6],
            'deletedDate': row[7],
            'messageID': row[8]
        }
        records_list.append(record_dict)

    return records_list

def GetProcessedCurrenciesForStats():
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()

    cursor.execute("SELECT * FROM NewProcessedCurrencies WHERE (NOT deleted OR (deleted AND (strftime('%s', deletedDate) - strftime('%s', date)) >= 3))")
    rows = cursor.fetchall()

    records_list = []

    for row in rows:
        record_dict = {
            'date': row[0],
            'chatID': row[1],
            'userID': row[2],
            'lang': row[3],
            'convertedFrom': row[4],
            'convertedTo': row[5],
            'deleted': row[6],
            'deletedDate': row[7],
            'messageID': row[8]
        }
        records_list.append(record_dict)

    return records_list

def GetProcessedCurrenciesCountForStats() -> int:
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM NewProcessedCurrencies WHERE (NOT deleted OR (deleted AND (strftime('%s', deletedDate) - strftime('%s', date)) >= 3))")
    res = cursor.fetchone()
    return res[0]

def GetUniqueUsersCount() -> int:
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(DISTINCT userID) FROM NewProcessedCurrencies WHERE (NOT deleted OR (deleted AND (strftime('%s', deletedDate) - strftime('%s', date)) >= 3))")
    res = cursor.fetchone()
    return res[0]

def GetLangActivity() -> dict:
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT lang, COUNT(*) FROM NewProcessedCurrencies WHERE (NOT deleted OR (deleted AND (strftime('%s', deletedDate) - strftime('%s', date)) >= 3)) GROUP BY lang")
    rows = cursor.fetchall()
    res = {row[0]: row[1] for row in rows}
    res["unknown"] = res.pop(None)
    res = dict(sorted(res.items(), key=lambda item: item[1], reverse=True))
    return res

def GetLangDistribution() -> dict:
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT lang, COUNT(DISTINCT userID) FROM NewProcessedCurrencies WHERE (NOT deleted OR (deleted AND (strftime('%s', deletedDate) - strftime('%s', date)) >= 3)) GROUP BY lang")
    rows = cursor.fetchall()
    res = {row[0]: row[1] for row in rows}
    res["unknown"] = res.pop(None)
    res = dict(sorted(res.items(), key=lambda item: item[1], reverse=True))
    return res

def GetBotUsageLastDayByMinute() -> dict:
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT strftime('%Y-%m-%d %H:%M', date), COUNT(*) FROM NewProcessedCurrencies WHERE (NOT deleted OR (deleted AND (strftime('%s', deletedDate) - strftime('%s', date)) >= 3)) AND date(date) = date('now') GROUP BY strftime('%H:%M', date)")
    rows = cursor.fetchall()
    res = {row[0]: row[1] for row in rows}
    res = dict(sorted(res.items(), key=lambda item: item[0]))
    return res

def GetBotUsageAllTimeByDay() -> dict:
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT strftime('%Y-%m-%d', date), COUNT(*) FROM NewProcessedCurrencies WHERE (NOT deleted OR (deleted AND (strftime('%s', deletedDate) - strftime('%s', date)) >= 3)) GROUP BY strftime('%Y-%m-%d', date)")
    rows = cursor.fetchall()
    res = {row[0]: row[1] for row in rows}
    res = dict(sorted(res.items(), key=lambda item: item[0]))
    return res

def GetBotUniqueUsersAllTimeByDay() -> dict:
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT strftime('%Y-%m-%d', date), COUNT(DISTINCT userID) FROM NewProcessedCurrencies WHERE (NOT deleted OR (deleted AND (strftime('%s', deletedDate) - strftime('%s', date)) >= 3)) GROUP BY strftime('%Y-%m-%d', date)")
    rows = cursor.fetchall()
    res = {row[0]: row[1] for row in rows}
    res = dict(sorted(res.items(), key=lambda item: item[0]))
    return res

def GetBotUniqueUsersAllTimeByMonth() -> dict:
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT strftime('%Y-%m', date), COUNT(DISTINCT userID) FROM NewProcessedCurrencies WHERE (NOT deleted OR (deleted AND (strftime('%s', deletedDate) - strftime('%s', date)) >= 3)) GROUP BY strftime('%Y-%m', date)")
    rows = cursor.fetchall()
    res = {row[0]: row[1] for row in rows}
    res = dict(sorted(res.items(), key=lambda item: item[0]))
    return res

def GetBotUsageLastWeekByHour() -> dict:
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT strftime('%Y-%m-%d %H:00', date), COUNT(*) FROM NewProcessedCurrencies WHERE (NOT deleted OR (deleted AND (strftime('%s', deletedDate) - strftime('%s', date)) >= 3)) AND date(date) > datetime('now', '-7 days') GROUP BY strftime('%Y-%m-%d %H', date)")
    rows = cursor.fetchall()
    res = {row[0]: row[1] for row in rows}
    res = dict(sorted(res.items(), key=lambda item: item[0]))
    return res

def GetBotUsageLastMonthByDay() -> dict:
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT strftime('%Y-%m-%d', date), COUNT(*) FROM NewProcessedCurrencies WHERE (NOT deleted OR (deleted AND (strftime('%s', deletedDate) - strftime('%s', date)) >= 3)) AND date(date) > datetime('now', '-1 month') GROUP BY strftime('%Y-%m-%d', date)")
    rows = cursor.fetchall()
    res = {row[0]: row[1] for row in rows}
    res = dict(sorted(res.items(), key=lambda item: item[0]))
    return res

def GetBotUniqueUsersLastWeek() -> int:
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(DISTINCT userID) FROM NewProcessedCurrencies WHERE (NOT deleted OR (deleted AND (strftime('%s', deletedDate) - strftime('%s', date)) >= 3)) AND date(date) > datetime('now', '-7 days')")
    res = cursor.fetchone()
    return res[0]

def GetBotUniqueUsersLastMonth() -> int:
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(DISTINCT userID) FROM NewProcessedCurrencies WHERE (NOT deleted OR (deleted AND (strftime('%s', deletedDate) - strftime('%s', date)) >= 3)) AND date(date) > datetime('now', '-1 month')")
    res = cursor.fetchone()
    return res[0]

def GetDictOfFlags() -> dict:
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM ExchangeRates")
    res = cursor.fetchall()
    res_dict = {}
    for i in res:
        res_dict[i[0]] = i[1]
    return res_dict


def GetExchangeRates() -> dict:
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM ExchangeRates")
    res = cursor.fetchall()
    res_dict = {}
    for i in res:
        res_dict[i[0]] = i[2]
    return res_dict


def GetCryptoRates() -> dict:
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM CryptoRates")
    res = cursor.fetchall()
    res_dict = {}
    for i in res:
        res_dict[i[0]] = i[2]
    return res_dict


def GetStatsInPeriod(days: int) -> dict:
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    res = {}
    cursor.execute(
        "SELECT COUNT(*) FROM ChatsUsage WHERE chatType = 'private' AND lastTimeUse > datetime('now', '-"+str(days)+" days')")
    res['activePrivate'] = cursor.fetchone()[0]
    cursor.execute(
        "SELECT COUNT(*) FROM ChatsUsage WHERE (chatType = 'group' OR chatType ='supergroup' ) AND lastTimeUse > datetime('now', '-"+str(days)+" days')")
    res['activeGroups'] = cursor.fetchone()[0]
    return res

def GetStatsForChart() -> dict:
    con = sql.connect('DataBases/StatsData.sqlite')
    cursor = con.cursor()
    res = {}

    cursor.execute("DELETE FROM ChatsTimeStats WHERE (DATE(date), TIME(date)) NOT IN (SELECT DATE(date), MAX(TIME(date)) FROM ChatsTimeStats GROUP BY DATE(date))")
    con.commit()
    
    cursor.execute("SELECT DATE(date), privateChatsAmount, groupChatsAmount, activeWeekPrivateChats, activeWeekGroupChats, activeMonthPrivateChats, activeMonthGroupChats FROM ChatsTimeStats")
    data = cursor.fetchall()
    res['dates'] = [k[0] for k in data]
    res['privateChatsAmount'] = [k[1] for k in data]
    res['groupChatsAmount'] = [k[2] for k in data]
    res['activeWeekPrivateChats'] = [k[3] for k in data]
    res['activeWeekGroupChats'] = [k[4] for k in data]
    res['activeMonthPrivateChats'] = [k[5] for k in data]
    res['activeMonthGroupChats'] = [k[6] for k in data]
    return res

def AddReport(chatID: str, userID: str, message: str, reply: str = ""):
    con = sql.connect('DataBases/ServiceData.sqlite')
    cursor = con.cursor()
    cursor.execute("INSERT INTO Reports (date,chatID,userID,message,reply) values (DATETIME(),?,?,?,?)", tuple(
        [chatID, userID, message, reply]))
    con.commit()


def ClearReports():
    con = sql.connect('DataBases/ServiceData.sqlite')
    cursor = con.cursor()
    cursor.execute("DELETE FROM Reports")
    con.commit()
    cursor.execute("VACUUM")
    con.commit()

def GetChatIDs():
    con = sql.connect('DataBases/DataForBot.sqlite')
    cursor = con.cursor()
    cursor.execute("SELECT chatID FROM SettingsGroups")
    res = [k[0] for k in cursor.fetchall()]
    cursor.execute("SELECT chatID FROM SettingsPrivateChats")
    res += [k[0] for k in cursor.fetchall()]
    return res
