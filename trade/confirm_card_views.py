import logging
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Post_Card, F_password
from .models import User
from rest_framework.response import Response
from django.http import JsonResponse




@api_view(['GET'])
def card_dashboard_view(request):
    logging.basicConfig(filename='success.log', level=logging.INFO)
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    a = True
    try:
        user = Post_Card.objects.filter(is_verified_card=a)
    except Exception as e:
        message=str(e)
        logging.error(f'NO CARD EXIST')
        return JsonResponse({"Success": False,
                             'Error': message}, status=400)

    if request.method == 'GET':
        data = user.values()
        logging.info(f'Got Data')
        return Response(data, status=200)
    else:
        logging.error(f'Cannot GET data')
        return JsonResponse({"Success": False}, status=400)



@api_view(['GET'])
def pending_cards(request):
    logging.basicConfig(filename='success.log', level=logging.INFO)
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    a = request.headers['Authorization']
    try:
        user = User.objects.get(auth_token=a)
    except Exception as e:
        message = str(e)
        logging.error(f'User does not exist')
        return JsonResponse({"Success": False,
                             'Error':message}, status=400)

    if request.method == 'GET':
        id=user.id
        print(user.id)
        card=list(Post_Card.objects.filter(user=id).filter(under_verification_card=True).values())
        print(card)

        logging.info(f'Got Data')
        return Response(card, status=200)
    else:
        logging.error(f'Cannot GET data')
        return JsonResponse({"Success": False}, status=400)


