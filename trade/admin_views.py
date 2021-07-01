from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from . serializers import UserSerializer
from .models import User, Post_Card, Orders
from rest_framework.response import Response
from django.http import JsonResponse
import logging
from datetime import datetime
import stripe
from .utils import Utils
stripe.api_key ='sk_test_51J3fPdGdPGnE47TFotkx7pqydBRgEOB4eDYKa3JvJna5z67WMghGdmF3viw7Pt4wvk3LU7TJUbm5It42bfyfgy3000W4atIDWx'


@api_view(['GET'])
def b_seller_view(request):
    logging.basicConfig(filename='success.log', level=logging.INFO)
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    a = True
    try:
        user = User.objects.filter(something=a)
    except Exception as e:
        message = str ( e )
        logging.error(f'{a} User Does not exist')
        return JsonResponse({"success": False,
                             'error': message}, status=400)

    if request.method == 'GET':
        data = user.values("name", "profile_pic", "DOB", "address", 'id')
        logging.info(f'Got Data')
        return Response(data, status=200)
    else:
        logging.error(f'Cannot GET data')
        return JsonResponse({"success": False}, status=400)




@api_view(['GET'])
def become_seller_recognition(request, pk):
    logging.basicConfig(filename='success.log', level=logging.INFO)
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    try:
        user = User.objects.filter(pk=pk)
    except Exception as e:
        message = str ( e )
        logging.error(f'{pk} User does not exist')
        return JsonResponse({'message':message}, status=400)

    if request.method == 'GET':

        data = user.values("name", "profile_pic", "DOB", "address", 'id', 'driving_license_front', 'driving_license_back', 'social_card','phone')
        logging.info(f'{user} Got Data')
        return Response(data, status=200)


@api_view(['POST'])
def become_seller_recognition_view(request, pk):
    logging.basicConfig(filename='success.log', level=logging.INFO)
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    try:
        user = User.objects.get(pk=pk)
    except Exception as e:
        message = str ( e )
        logging.error(f'{pk} User Does not exist')
        return JsonResponse({'message':message}, status=400)


    if request.method == 'POST':

        b = request.data.get('seller')
        if b == 'true':
            user.b_seller = True
            user.something=False
            user.save()
            logging.info(f'Data saved')
        if b == 'false':
            user.is_verified_seller = False
            user.something=False
            user.save()
            username = user.username
            print(username)
            email_body = "Hi " + username + "\n Your Request Has Been Rejected Due to Admin Did not Approve Contact admin on this no +923206467896"
            print(email_body)
            data = {'email_body': email_body, 'to_email': username, "email_subject": "Request Rejected"}
            print(data)
            Utils.send_email(data)
            logging.info(f'Email sent successfully')

        return JsonResponse({'success': True}, status=400)
    else:
        logging.error(f'Can not save data')
        return JsonResponse({"message": False}, status=400)





class UserViewSet(APIView):
    serializer_class = UserSerializer
    logging.basicConfig(filename='success.log', level=logging.INFO)

    def get(self, request):
        user_data = User.objects.all()
        serializer = UserSerializer(user_data, many=True)
        logging.info('Got data')
        return Response(serializer.data, status=200)





@api_view(['GET'])
def feature_seller_view(request):
    logging.basicConfig(filename='success.log', level=logging.INFO)
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    a = True
    try:
        user = User.objects.filter(under_verification_feature=a)
    except Exception as e:
        message = str ( e )
        logging.error(f'{a} User Does not exist')
        return JsonResponse({"Success": False,
                             'Error': message}, status=400)

    if request.method == 'GET':
        data = user.values("name", "profile_pic", "address", 'id', 'DOB')
        logging.info(f'Got Data')
        return Response(data, status=200)
    else:
        logging.error(f'Cannot GET data')
        return JsonResponse({"Success": False}, status=400)






@api_view(['POST'])
def verified_feature(request, pk):
    logging.basicConfig(filename='success.log', level=logging.INFO)
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    try:
        user = User.objects.get(pk=pk)
    except Exception as e:
        message = str ( e )
        logging.error(f'{pk} User Does not exist')
        return JsonResponse({'message':message}, status=400)


    if request.method == 'POST':

        b = request.data.get('verified_seller')
        if b == 'true':
            user.verified_feature = True
            user.under_verification_feature=False
            user.save()
            logging.info(f'Data saved')
            return JsonResponse({'success': True}, status=200)
        if b == 'false':
            user.under_verification_feature=False
            user.save()
            username = user.username
            print(username)
            email_body = "Hi " + username + "\n Your Request Has Been Rejected Due to Admin Did not Get Cash Contact admin on this no +923206467896"
            print(email_body)
            data = {'email_body': email_body, 'to_email': username, "email_subject": "Request Rejected"}
            print(data)
            Utils.send_email(data)
            logging.info(f'Email sent successfully')

            return JsonResponse({"success": True}, status=200)
    else:
        logging.error(f'Can not save data')
        return JsonResponse({"message": False}, status=400)






@api_view(['GET'])
def special_card_view(request):
    logging.basicConfig(filename='success.log', level=logging.INFO)
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    a = True
    try:
        user = Post_Card.objects.filter(special_card_verification=a)
    except Exception as e:
        message = str ( e )
        logging.error(f'{a} User Does not exist')
        return JsonResponse({"success": False,
                             'error': message}, status=400)

    if request.method == 'GET':
        data = user.values()
        logging.info(f'Got Data')
        return Response(data, status=200)
    else:
        logging.error(f'Cannot GET data')
        return JsonResponse({"success": False}, status=400)









@api_view(['POST'])
def special_card_verified(request, pk):
    logging.basicConfig(filename='success.log', level=logging.INFO)
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    try:
        user = Post_Card.objects.get(pk=pk)
    except Exception as e:
        message = str ( e )
        logging.error(f'{pk} User Does not exist')
        return JsonResponse({'message':message}, status=400)


    if request.method == 'POST':

        b = request.data['card_verified']
        if b == 'true':
            user.special_card_posted=datetime.now()
            print(user.special_card_posted)
            user.special_card = True
            user.save()
            logging.info(f'Data saved')
        if b == 'false':
            user.under_verification_feature=False
            user.save()
            usern = user.user
            username=str(usern)
            print(username)
            email_body = "Hi " + username + "\n Your Request Has Been Rejected Due to Admin Did not Get Cash Contact admin on this no +923206467896"
            print(email_body)
            data = {'email_body': email_body, 'to_email': username, "email_subject": "Request Rejected"}
            print(data)
            Utils.send_email(data)
            logging.info(f'Email sent successfully')

            return JsonResponse({"Success": True}, status=200)
        # user.save()
        return JsonResponse({'Success': True}, status=200)
    else:
        logging.error(f'Can not save data')
        return JsonResponse({"Message": False}, status=400)






@api_view(['GET'])
def post_card_view(request):
    logging.basicConfig(filename='success.log', level=logging.INFO)
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    a = True
    try:
        user = Post_Card.objects.filter(under_verification_card=a)
    except Exception as e:
        message = str ( e )
        logging.error(f'{a} User Does not exist')
        return JsonResponse({"success": False,
                             'error':message}, status=400)

    if request.method == 'GET':
        data = user.values()
        logging.info(f'Got Data')
        return Response(data, status=200)
    else:
        logging.error(f'Cannot GET data')
        return JsonResponse({"success": False}, status=400)


@api_view(['POST'])
def confirm_card_post(request, pk):
    logging.basicConfig(filename='success.log', level=logging.INFO)
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    try:
        user = Post_Card.objects.get(pk=pk)
        print(user.user)
    except Exception as e:
        message = str ( e )
        logging.error(f'{pk} User Does not exist')
        return JsonResponse({'message': message}, status=400)


    if request.method == 'POST':

        b = request.data['card_verified']
        if b == 'true':
            user.is_verified_card = True
            user.under_verification_card=False
            user.save()
            return Response ( {'success':True},status=status.HTTP_200_OK)
        if b == 'false':
            user.delete()
            usern = user.user
            username=str(usern)
            print(type(username))
            email_body = "Hi " + username + "\n Your card Has Been Rejected Due to Admin Rejected Contact admin on this no +923206467896"
            print(email_body)
            data = {'email_body': email_body, 'to_email': username, "email_subject": "CARD Request Rejected"}
            print(data)
            Utils.send_email(data)
            logging.info(f'Email sent successfully')

            return JsonResponse({"Success": True},status=200)
        return JsonResponse({'Success': True}, status=200)
    else:
        logging.error(f'Can not save data')
        return JsonResponse({"Message": False}, status=400)














# Order Cards


@api_view(['GET'])
def check_cards(request):
    logging.basicConfig(filename='success.log', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')


    if request.method=="GET":
        my_list = []
        data=list(Orders.objects.all().values())
        for i in data:
            car = i['card']
            card = list ( Post_Card.objects.filter ( id=car ).values ( 'card_no' , 'card_expiry' , 'user' ) )
            my_list.append ( card )
            # car = json.dumps(card, indent=4, sort_keys=True, default=str)

        return Response ( {"Cards": my_list} , content_type='application/json', status=200)


