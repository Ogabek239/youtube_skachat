import requests
import time

TOKEN = '7681275010:AAHDL8x6H7myw3fytPxRm1qRDvgV7pAdFF0'  # Bot tokeningizni shu yerga qo'ying
BASE_URL = f'https://api.telegram.org/bot{TOKEN}/'

def get_updates(offset=None):
    url = BASE_URL + 'getUpdates'
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

def send_message(chat_id, text):
    url = BASE_URL + 'sendMessage'
    params = {'chat_id': chat_id, 'text': text}
    requests.get(url, params=params)

def send_photo(chat_id, file_id):
    url = BASE_URL + 'sendPhoto'
    params = {'chat_id': chat_id, 'photo': file_id}
    requests.get(url, params=params)

def send_video(chat_id, file_id):
    url = BASE_URL + 'sendVideo'
    params = {'chat_id': chat_id, 'video': file_id}
    requests.get(url, params=params)

def send_audio(chat_id, file_id):
    url = BASE_URL + 'sendAudio'
    params = {'chat_id': chat_id, 'audio': file_id}
    requests.get(url, params=params)

def send_document(chat_id, file_id):
    url = BASE_URL + 'sendDocument'
    params = {'chat_id': chat_id, 'document': file_id}
    requests.get(url, params=params)

def send_voice(chat_id, file_id):
    url = BASE_URL + 'sendVoice'
    params = {'chat_id': chat_id, 'voice': file_id}
    requests.get(url, params=params)

def send_sticker(chat_id, file_id):
    url = BASE_URL + 'sendSticker'
    params = {'chat_id': chat_id, 'sticker': file_id}
    requests.get(url, params=params)

def send_location(chat_id, latitude, longitude):
    url = BASE_URL + 'sendLocation'
    params = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude}
    requests.get(url, params=params)

def send_contact(chat_id, phone_number, first_name, last_name=None):
    url = BASE_URL + 'sendContact'
    params = {
        'chat_id': chat_id,
        'phone_number': phone_number,
        'first_name': first_name,
    }
    if last_name:
        params['last_name'] = last_name
    requests.get(url, params=params)

def main():
    print('Universal Echo Bot ishga tushdi...')
    update_id = None

    while True:
        updates = get_updates(offset=update_id)
        if 'result' in updates and len(updates['result']) > 0:
            for item in updates['result']:
                update_id = item['update_id'] + 1
                message = item.get('message')
                if not message:
                    continue
                chat_id = message['chat']['id']

                # Endi turli xil xabar turlarini tekshiramiz:

                if 'text' in message:
                    send_message(chat_id, message['text'])

                elif 'photo' in message:
                    photo_list = message['photo']
                    file_id = photo_list[-1]['file_id']
                    send_photo(chat_id, file_id)

                elif 'video' in message:
                    file_id = message['video']['file_id']
                    send_video(chat_id, file_id)

                elif 'audio' in message:
                    file_id = message['audio']['file_id']
                    send_audio(chat_id, file_id)

                elif 'document' in message:
                    file_id = message['document']['file_id']
                    send_document(chat_id, file_id)

                elif 'voice' in message:
                    file_id = message['voice']['file_id']
                    send_voice(chat_id, file_id)

                elif 'sticker' in message:
                    file_id = message['sticker']['file_id']
                    send_sticker(chat_id, file_id)

                elif 'location' in message:
                    latitude = message['location']['latitude']
                    longitude = message['location']['longitude']
                    send_location(chat_id, latitude, longitude)

                elif 'contact' in message:
                    phone_number = message['contact']['phone_number']
                    first_name = message['contact']['first_name']
                    last_name = message['contact'].get('last_name')
                    send_contact(chat_id, phone_number, first_name, last_name)

                else:
                    send_message(chat_id, "Men bu xabar turini qaytara olmayman 😔")

        time.sleep(1)

if __name__ == '__main__':
    main()



