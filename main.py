from telethon import TelegramClient, events, utils
import configparser



# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")


# Считывание чатов для парсинга
with open('chats.txt', 'r') as f:
    chats = f.readlines()


keywords = []

# Считывание ключевых слов
with open('keywords.txt', 'r') as f:
    lines = f.readlines()
for key in lines:
    keywords.append(key.strip())

print(keywords)



api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
forward_chat = config['Telegram']['forward_chat']
session_name = 'session'


client = TelegramClient(session_name, api_id, api_hash)
client.start()


@client.on(events.NewMessage(chats=chats)) #можно парсить неограниченное кол-во каналов
async def normal_handler(event):
    try:
        for i in keywords:
            if i in event.message.to_dict()['message']:
                await client.forward_messages(int(forward_chat), event.message)
                chat = await client.get_entity(event.message.to_dict()['peer_id']['channel_id'])
                link = 'https://t.me/{}/{}'.format(chat.username, event.message.to_dict()['id'])
                await client.send_message(int(forward_chat), link)

                # print(chat.username)
    except:
        pass


client.run_until_disconnected()
