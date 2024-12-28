from django.shortcuts import render
from django.http import JsonResponse
from django.http import JsonResponse
import redis
import json
import uuid 
import qrcode
from io import BytesIO
import base64
from cryptography.fernet import Fernet



def home(request):
    context = {}
    return render(request, 'home.html', context)

def create_room(request):
    room_link = ''
    context = {}

    room_id = str(uuid.uuid4())
    base_url = request.build_absolute_uri('/')
    
    if base_url.endswith('/'):
        base_url = base_url[:-1]
    
    room_link = f'{base_url}/room/{room_id}'

    qr_code = qrcode.make(room_link)
    qr_image = BytesIO()
    qr_code.save(qr_image, format="PNG")
    qr_image.seek(0)

    
    qr_code_data = base64.b64encode(qr_image.read()).decode('utf-8')

    context['room_link'] = room_link
    context['qr_code_data'] = qr_code_data

    return render(request, 'createRoom.html', context)


def chatRoom(request, roomId):
    context = {}
    context['roomId'] = roomId

    base_url = request.build_absolute_uri('/')
    
    if base_url.endswith('/'):
        base_url = base_url[:-1]
    
    room_link = f'{base_url}/room/{roomId}'

    context['room_link'] = room_link

    return render(request, 'chatRoom.html', context)


def decrypt_message(key, encrypted_message):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message.encode()).decode()



def chat_messages(request):
    room_id = request.GET.get('room_id')
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        messages = r.lrange(room_id, 0, -1)

        key = r.get(f"{room_id}_key")
        if not key:
            print("Error: Encryption key not found for room.")
            return JsonResponse({"error": "Key not found"}, status=500)

        message_list = []
        for message_data in messages:
            message_json = json.loads(message_data)
            decrypted_message = decrypt_message(key, message_json['message'])
            message_list.append({
                'message': decrypted_message,
                'time': message_json.get('time', 'Unknown Time')
            })
        message_list.reverse()
        print('My message list is', message_list)

    except Exception as e:
        print("Error", str(e))
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse(message_list, safe=False)

