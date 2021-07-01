from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .serializers import (UpdataeSerializer,
                          MessageSerializer
                          )
from django.contrib.auth.models import User
from .models import User, Message
from django.http import JsonResponse

@csrf_exempt
@api_view(['POST', 'GET'])
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        print(messages)
        serializer = MessageSerializer(messages, many=True, context={'request': request.data})
        # print(serializer)
        for message in messages:
            print(message)
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False, status=200)

    elif request.method == 'POST':
        m=[]
        print((request.data))
        data=request.data
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)











def chat_view(request):
    if request.method == "GET":
        return JsonResponse({'users': str(list(User.objects.exclude(username=request.user.username).values('username')))}, status=200)





def message_view(request, sender, receiver):
    if request.method == "GET":
        return JsonResponse(
                      {'users': str(list(User.objects.exclude(username=request.user.username))),
                       'receiver': str(User.objects.get(id=receiver)),
                       'messages': str(list(Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)))
                       }, status=200)
