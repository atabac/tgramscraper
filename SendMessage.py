from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import sys
import csv
import random
import time
import os.path
import pickle
from pathlib import Path

api_id = str()
api_hash = str()
phone = str()

config_file = Path("config.txt")
try:
    config_file.resolve(strict=True)
except FileNotFoundError:
    api_id = input('Enter the api_id: ')
    api_hash = input('Enter the api_hash: ')
    phone = input('Enter the phone: ')
else:
    accs = []
    fs = open('config.txt', 'rb')
    while True:
        try:
            accs.append(pickle.load(fs))
        except EOFError:
            fs.close()
            break
    print('Choose an account to scrape members\n')
    i = 0
    for acc in accs:
        print('(', i, ') ', acc[2])
        i += 1
    ind = int(input('Enter choice: '))
    api_id = accs[ind][0]
    api_hash = accs[ind][1]
    phone = accs[ind][2]

SLEEP_TIME = 30
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

input_file = sys.argv[1]
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

print("users count: ", len(users));
mode = int(input("Enter 1 to send by user ID or 2 to send by username: "))

messages= ["Hello {}, How are you?", "Hi {}, What's up?", "Hey {}, let me know your thoughts!"]

for user in users:
    if mode == 2:
        if user['username'] == "":
            continue
        receiver = client.get_input_entity(user['username'])
    elif mode == 1:
        receiver = InputPeerUser(user['id'],user['access_hash'])
    else:
        print("Invalid Mode. Exiting.")
        client.disconnect()
        sys.exit()
    message = messages[0]#random.choice(messages)
    try:
        print("Sending Message to:", user['name'])
        client.send_message(receiver, message.format(user['name']))
        print("Waiting {} seconds".format(SLEEP_TIME))
        time.sleep(SLEEP_TIME)
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        client.disconnect()
        sys.exit()
    except Exception as e:
        print("Error:", e)
        print("Trying to continue...")
        continue
client.disconnect()
print("Done. Message sent to all users.")
