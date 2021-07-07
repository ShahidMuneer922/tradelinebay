import logging
from rest_framework.decorators import api_view
from .models import Post_Card
from rest_framework.response import Response
from django.http import JsonResponse


@api_view(['POST'])
def verification_card(request, pk):
    logging.basicConfig(filename='success.log', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    try:
        user = Post_Card.objects.get(pk=pk)
        print(Post_Card.objects.all())
        use = Post_Card.objects.all()

    except Exception as e:
        message = str(e)
        logging.info(f' Does not Exist')
        return JsonResponse({'message': message}, status=400)

    if request.method == 'POST':
        verified = request.data['card_verification']
        if verified == 'true':
            user.special_card_verification = True
            user.save()
            logging.info(f' verification card')
            return JsonResponse({"Success": True}, status=200)
        else:
            logging.info(f'{user.username} Can not verify seller')
            return JsonResponse({"Message": False}, status=400)


@api_view(['GET'])
def special_card_confirm_view(request):
    logging.basicConfig(filename='success.log', level=logging.INFO)
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    a = True
    try:
        user = Post_Card.objects.filter(special_card=a)
    except Exception as e:
        message = str(e)
        logging.error(f'{a} User Does not exist')
        return JsonResponse({"Success": False,
                             'Error': message}, status=400)

    if request.method == 'GET':
        data = user.values()
        logging.info(f'Got Data')
        return Response(data, status=200)
    else:
        logging.error(f'Cannot GET data')
        return JsonResponse({"Success": False}, status=400)
