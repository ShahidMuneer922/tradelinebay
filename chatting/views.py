from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Message
# Create your views here.


def intersection(data, dat):
    lst3 = [value for value in data if value in dat]
    return lst3

@api_view(['GET'])
def previous_msg(request, pk, id):
    try:

        data = list(Message.objects.filter(sender=pk).values('thread'))
        dat = list(Message.objects.filter(sender=id).values('thread'))
        for i in intersection(data, dat):
            thread = str(i)
            da = thread.strip("{'thread':}")
            print(da)

        user = list(Message.objects.filter(thread=da).values('text', "time", 'sender'))
        print(user)

        return Response({'data': user})
    except Exception as e:
        message = str(e)
        return Response({"success":False,
                         "message":message})



