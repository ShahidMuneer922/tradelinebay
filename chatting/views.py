from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging
from datetime import datetime, timedelta
from .models import Message
from django.http import JsonResponse


# Create your views here.


def intersection(data, dat):
    lst3 = [value for value in data if value in dat]
    return lst3


@api_view(['GET'])
def previous_msg(request, pk, id):
    try:
        data = list(Message.objects.filter(sender=pk).values('thread'))
        dat = list(Message.objects.filter(sender=id).values('thread'))
        print(data)
        print(dat)
        if data == []:
            if dat == []:
                return Response({'success': True,
                                 'message': 'No Messages To show'})
        print(intersection(data, dat))
        if intersection(data, dat) == []:
            for i in dat:
                thread = str(i)
                da = thread.strip("{'thread':}")
                print(da)
        if intersection(data, dat) == []:
            for i in data:
                thread = str(i)
                da = thread.strip("{'thread':}")
                print(da)
        if intersection(data, dat) != []:
            for i in intersection(data, dat):
                thread = str(i)
                da = thread.strip("{'thread':}")
                print(da)
        user = list(Message.objects.filter(thread=da).values('text', "thread", "time", 'sender', 'id'))
        print(user)

        return Response({'data': user})
    except Exception as e:
        message = str(e)
        return Response({"success": False,
                         "message": message})


# Documentation Done
@api_view(['DELETE'])
def delete_message(request, pk):
    logging.basicConfig(filename='success.log', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    try:
        user = Message.objects.get(id=pk)
    except Exception as e:
        message = str(e)
        logging.info(f'{message}')
        return JsonResponse({'message': message}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        user.delete()
        logging.info(f'deleted successfully')
        return JsonResponse({'success': True}, status=200)
    else:
        return JsonResponse({'message': False
                             }, status=400)


def disappear_messages(request):
    user = Message.objects.filter(disappear_message=True)
    # print(user)
    for use in user:
        print(use.disappear_message)
        if use.disappear_message == True:
            a = list(Message.objects.filter(disappear_message_start_time__lte=datetime.now() - timedelta(seconds=10)))
            for b in a:
                print(b)
                b.delete()
    return JsonResponse({"success": True}, status=200)


@api_view(['POST'])
def disappear_message_start(request, pk):
    logging.basicConfig(filename='success.log', level=logging.INFO)
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    try:
        use = Message.objects.filter(thread=pk)
    except Exception as e:
        message = str(e)
        logging.error(f' User Does not exist')
        return JsonResponse({'message': message}, status=400)

    if request.method == 'POST':

        b = request.data.get('disappear')
        if b == 'true':
            for user in use:
                user.disappear_message_start_time = datetime.now()
                print(user.disappear_message_start_time)
                user.disappear_message = True
                user.save()
                return JsonResponse({"Success": True}, status=200)
        c = request.data.get('dont_disappear')
        if c == 'true':
            for user in use:
                user.disappear_message = False
                user.disappear_message_start_time = None
                user.save()
                logging.info(f'Data saved')
                return JsonResponse({'Success': True}, status=200)
    else:
        logging.error(f'Can not save data')
        return JsonResponse({"Message": False}, status=400)
