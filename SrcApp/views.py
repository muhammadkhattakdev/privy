from django.shortcuts import render
from django.http import JsonResponse
from django.http import JsonResponse
import redis
import json




def homepage(request):

    return render(request, 'home.html')






def chatRoom(request, roomId):
    context = {}
    context['roomId'] = roomId

    return render(request, 'chatRoom.html', context)




def chat_messages(request):
    roomId = request.GET.get('room_id')
    print('Room Id to views.py file', roomId)
    try :
        print("helo")
        r = redis.Redis(host='localhost', port=6379, db=0)
        messages = r.lrange(roomId, 0, 10)
        message_list = []
        for message_data in messages:
            print('hello world')
            message_json = json.loads(message_data)
            message_list.append({
                'message': message_json['message'],
                'time': message_json.get('time', 'Unknown Time')
            })
    except:
        print('My error')
    return JsonResponse(message_list, safe=False)



