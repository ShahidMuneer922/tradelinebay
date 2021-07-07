from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Message
# Create your views here.

@api_view(['GET'])
def previous_msg(request, pk, id):
    try:
        my_list =[]
        your_list = []
        # print(list(Message.objects.filter(sender=me).values('text')))
        data = list(Message.objects.filter(sender=pk).values('thread'))
        dat = list(Message.objects.filter(sender=id).values('thread'))
        for i in data and dat:
            thread = str(i)
            da = thread.strip("{'thread':}")
            s = da
        user = list(Message.objects.filter(thread=s).values('text', "time", 'sender'))
        print(user)

        #     thread1 = i
        #     print(thread1)
        # print(thread1)
        # print("next")
        # for d in dat:
        #     thread2 = d
        #     print(thread2)
        #     if thread1 == thread2:
        #         user = Message.objects.filter(thread=thread2).values('text', "time", 'sender')
        #         for b in user:
        #             # print(i)
        #             my_list.append(b)

        # print(data, dat)

        return Response({'data': user})
    except Exception as e:
        message = str(e)
        return Response({"success":False,
                         "message":message})



