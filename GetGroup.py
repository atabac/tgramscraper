from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv
import os.path
import pickle
from pathlib import Path

def SaveToFile(target_group, client):

    print('Fetching Members...')
    all_participants = []
    all_participants = client.get_participants(target_group, aggressive=True)

    print('Saving In file...')
    with open("groupmembers_" +  target_group.title + ".csv","w",encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
        for user in all_participants:
            print('username: ' + str(user.username))
            print('first name: ' + str(user.first_name))
            print('last name: ' + str(user.last_name))
            print('\n')
            if user.username:
                username= user.username
            else:
                username= ""
            if user.first_name:
                first_name= user.first_name
            else:
                first_name= ""
            if user.last_name:
                last_name= user.last_name
            else:
                last_name= ""
            name= (first_name + ' ' + last_name).strip()
            writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
    print('Members scraped successfully.')
    
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
    
    
print('Connecting...')
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))


chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        """if chat.megagroup== True:"""
        groups.append(chat)
    except:
        continue

print('Choose a group to scrape members from:')
i=1
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1
print('0 - SelectAll')

g_index = input("Enter a Number: ")

if(int(g_index) == 0):
    for g in groups:
        SaveToFile(g, client)
else:
    SaveToFile(groups[int(g_index) - 1], client)
        

