import random
import logging
from django.core.validators import validate_email
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import (UpdataeSerializer,
                          VerifiedSerializer,
                          f_serializer,
                          UserDetailSerializer
                          )
from django.contrib.auth.models import User
from .models import Post_Card, F_password
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import User
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from .utils import Utils

# Create your views here.

class LoginAPI(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, **kwargs):
        logging.basicConfig(filename='success.log', level=logging.INFO,  datefmt='%m/%d/%Y %I:%M:%S %p')
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            print(user.is_verified)
            if user.is_superuser == True:
                login(request, user)
                logging.info(f'{user.username} is admin (login)')
                return JsonResponse({'token': Token.objects.get(user=user).key,
                                     'success': True,
                                     "super_user_status": 1}, status=200)
            elif user.is_verified == True:
                login(request, user)
                logging.info(f'{user.username} is logged in')
                return JsonResponse({'token': Token.objects.get(user=user).key,
                                     'success': True,
                                     "super_user_status": 0}, status=200)
            else:
                logging.info(f'{user.username} user is not verified')
                return JsonResponse({"success": False,
                                     "error": "User is not Verified",
                                     "token":Token.objects.get(user=user).key,
                                     "status": 2}, status=status.HTTP_200_OK)
        else:
            logging.info(f'Invalid Credentials')
            return JsonResponse({"success": False,
                                 "error": "Wrong Username Or Password",
                                 "status":3}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request):
    a = request.headers['Authorization']
    print(a)
    logging.basicConfig(filename='success.log', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    try:
        user = User.objects.get(auth_token=a)
    except Exception as e:
        message=str(e)
        logging.info(f'User Does Not Exist')
        return JsonResponse({'message': message}, status=400)

    if request.method == 'GET':
        user_serializer = UserDetailSerializer(user)
        print(user.username)
        logging.info(f'{user.username} got data')
        return JsonResponse(user_serializer.data, status=200)


    elif request.method == 'DELETE':
        user.delete()
        logging.info(f'{user.username} deleted successfully')
        return JsonResponse({'success': True}, status=200)
    else:
        return JsonResponse({'message': False
                             }, status=400)


class Verifyviewset(viewsets.ModelViewSet):
    serializer_class = VerifiedSerializer

    def get_queryset(self):
        data = Post_Card.objects.all()
        return data

@api_view(['POST'])
def Verify_Email(request):
    logging.basicConfig(filename='success.log', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    # print(request.)
    a = request.headers.get('Authorization')
    try:
        user = User.objects.get(auth_token=a)
    except Exception as e:
        logging.info(f'{a}User Does Not Exist')
        logging.info(f'{e}')
        return JsonResponse({"success": False,
                             # 'error': 'Something Went Wrong',
                             "message": str(e)}, status=400)

    if request.method == 'POST':
        otp = user.otp
        verified_otp = request.data['otp']
        print(verified_otp)
        if int(verified_otp) == otp:
            user.is_verified = True
            user.save()
            logging.info(f'{user.username} Verified through OTP')
            return JsonResponse({"success": True,
                                 "message": "OTP verified"}, status=200)
        else:
            logging.info(f'{user.username} entered wrong otp')
            print("wrong otp")
            return JsonResponse({"success": False,
                                 "error": "Incorrect OTP"}, status=400)

@api_view(['POST'])
def Verification_seller(request):
    logging.basicConfig(filename='success.log', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    a = request.headers['Authorization']
    try:
        user = User.objects.get(auth_token=a)
    except Exception as e:
        message= str(e)
        logging.info(f'{a} Does not Exist')
        return JsonResponse({'message': message}, status=400)

    if request.method == 'POST':
        verified_otp = request.data['is_verified_seller']
        if verified_otp == 'true':
            if user.b_seller ==True:
                return JsonResponse({'success':True,
                         'message':user.b_seller}, status=200)
            user.is_verified_seller = True
            user.something=True
            user.save()
            logging.info(f'{user.username} verified user')
            return JsonResponse({"success": True,
                                "message":user.b_seller}, status=200)
        else:
            logging.info(f'{user.username} Can not verify seller')
            return JsonResponse({"message": False}, status=400)


@api_view(['POST'])
def registration_view(request):
    logging.basicConfig(filename='success.log', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    if request.method == 'POST':
        user = request.data
        r = random.randint(111111, 999999)
        usernam = user.get('username')
        username=usernam.lower()
        password = user.get('password')
        try:
            validate_email(username)
        except Exception as e:
            message=str(e)
            logging.info(f'{username} is not a valid email please enter a valid email')
            return JsonResponse({"success": False,
                                 "error": message}, status=400)

        try:
            user = User.objects.create_user(username=username, password=password, otp=r)
            user.save()
            logging.info(f'User saved successfully')
            dat = {}
            token = r
            print(token)
            absurl = "OTP :" + str(token)
            print(absurl)
            email_body = "Hi " + username + " use the OTP to verify \n" + absurl
            print(email_body)
            data = {'email_body': email_body, 'to_email': username, "email_subject": "Verify your email"}
            print(data)
            Utils.send_email(data)
            dat['success'] =  "User Registered Successfully"
            token = Token.objects.get(user=user).key
            dat['token'] = token
            logging.info(f'OTP sent successfully')
            return JsonResponse({"success": True,
                                 "token": token})
        except Exception as e:
            print(e)
            a=str(e)
            print(a)
            User.objects.get(username=username)
            logging.info(f'{username} already exist')
            return JsonResponse({"success": False,
                                 "error": a}, status=400)


    else:
        logging.info(f'Can not process data please try again')
        return JsonResponse({"Success": False,
                             "Error": "Please Post The Request"}, status=400)


@api_view(['GET'])
def seller(request):
    if request.method == 'GET':
        user = User.objects.all().values("id", "auth_token", "username", 'name', 'address')
        return Response( {'data':user})


@api_view(['POST'])
def further_registration(request):
    logging.basicConfig(filename='success.log', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    a = request.headers['Authorization']
    try:
        user = User.objects.get(auth_token=a)
    except Exception as e:
        message=str(e)
        logging.info(f'{a} User Does not exist')
        return JsonResponse({"Success": False,
                             'Error': message}, status=400)

    if request.method == 'POST':

        print(request.data)
        user.name = request.data.get('name')
        user.address = request.data.get('address')
        user.DOB = request.data.get('DOB')
        user.profile_pic = request.data.get('profile_pic')
        user.driving_license_front = request.data.get('driving_license_front')
        user.driving_license_back = request.data.get('driving_license_back')
        user.social_card = request.data.get('social_card')
        user.phone = request.data.get('phone')
        user.save()
        logging.info(f'{user.username} Data Saved')
        return JsonResponse({'Success': True,
                             "Message": "Data saved"}, status=200)

    else:
        logging.info(f"Can't save data")
        return JsonResponse({"Success": False,
                             "Error": "Can't Save Data"}, status=400)




@api_view(['POST', 'GET'])
def card(request):
    b=True
    logging.basicConfig(filename='success.log', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    a = request.headers['Authorization']
    try:
        user = User.objects.get(auth_token=a)
        user_id = user.id
        print(user_id)
    except Exception as e:
        message=str(e)
        logging.info(f'{a} User Does not exist')
        return JsonResponse({'message': message}, status=400)

    if request.method == 'GET':
        if User.objects.filter(b_seller=b):
            data = Post_Card.objects.filter(user=user_id)
            print(data.values())
            i =data.values()
            logging.info(f'Got data')
            return Response(i, status=200)

    if request.method == 'POST':
        if User.objects.filter(b_seller=b):
            user_id=user_id
            card_image = request.data["card_image"]
            card_no = request.data["card_no"]
            card_limit = request.data["card_limit"]
            card_expiry = request.data["card_expiry"]
            realative_name = request.data["realative_name"]
            card_balance = request.data["card_balance"]
            card_sell_price = request.data["card_sell_price"]
            card_bid_price = request.data["card_bid_price"]
            Post_Card.objects.create(user_id=user_id,card_image=card_image,card_no=card_no, card_limit=card_limit,card_expiry=card_expiry,
                                     realative_name=realative_name,card_balance=card_balance,card_sell_price=card_sell_price,
                                     card_bid_price=card_bid_price, under_verification_card=True)
            logging.info(f'Data saved Successfully')
            return JsonResponse({"success":True,
                                 "message":"Data saved"}, status=200)
        else:
            print("You are nat a seller")
            return JsonResponse({"success":False,
                                 "message":"You are nat a seller"}, status=400)
    else:
        logging.info(f'Cannot save data')
        return JsonResponse({"Message": False}, status=400)




@api_view(['PUT'])
def update_password(request):
    logging.basicConfig(filename='success.log', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    a = request.headers['Authorization']
    try:
        user = User.objects.get(auth_token=a)
    except Exception as e:
        message=str(e)
        logging.info(f'{a} User Does not exist')
        return JsonResponse({'message': message}, status=400)

    if request.method == 'PUT':
        print(request.data)
        serializer= UpdataeSerializer(user, data=request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            data['success']=True
            return Response(data=data, status=200)
        else:
            return Response(serializer.errors, status=400)





@api_view(['POST'])
def forgot_password(request):
    logging.basicConfig(filename='success.log', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    username = request.data['username']
    try:
        user = User.objects.get(username=username)
        user_id=user.id
        r=random.randint(111111,999999)
        token = r
        absurl = "OTP :" + str(token)
        email_body = "Hi " + username + " use the OTP to verify \n" + absurl
        data = {'email_body': email_body, 'to_email': username, "email_subject": "Password Reset"}
        Utils.send_email(data)
        F_password.objects.create(user_id=user_id, password_reset_code=r)
        token = Token.objects.get(user=user).key
        logging.info(f'OTP sent successfully')
        return JsonResponse({"success": True,
                             "token": token,
                             'id':user_id}, status=200)
    except Exception as e:
        message= str(e)
        logging.info(f' User Does not exist')
        return JsonResponse({'error': message}, status=400)


@api_view(['POST'])
def Verify_Code(request, pk):
    logging.basicConfig(filename='success.log', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    try:
        user = F_password.objects.filter(user_id=pk)
        print(user)
    except Exception as e:
        message=str(e)
        logging.info(f'User Does Not Exist')
        return JsonResponse({"success": False,
                             'error': message}, status=400)

    if request.method == 'POST':
        for obj in user:
            otp = obj.password_reset_code
            print(obj.password_reset_code)
        verified_otp = request.data['password_reset_code']
        try:
            if int(verified_otp) == otp:
                user.delete()
                logging.info(f'Verified through Code')
                return JsonResponse({"success": True,
                                     "message": "OTP verified"}, status=200)
            else:
                logging.info(f' entered wrong Code')
                print("wrong otp")
                return JsonResponse({"success": False,
                                     "error": "Incorrect Code"}, status=300)
        except Exception as e:
            message= str(e)
            return JsonResponse({"error": message}, status=400)

class f_pass(APIView):
    serializer_class = f_serializer
    logging.basicConfig(filename='success.log', level=logging.INFO)

    def get(self, request):
        user_data = F_password.objects.all()
        serializer = f_serializer(user_data, many=True)
        logging.info('Got data')
        return Response(serializer.data, status=200)




@api_view(['PUT'])
def update_user(request):
    logging.basicConfig(filename='success.log', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    a = request.headers['Authorization']
    try:
        user = User.objects.get(auth_token=a)
    except Exception as e:
        message=str(e)
        logging.info(f'{a} User Does not exist')
        return JsonResponse({'message': message})

    if request.method == 'PUT':
        data=request.data
        print(data)
        if request.data.get('name') != None:
            user.name= request.data.get('name')
            user.save()
        if request.data.get('address') != None:
            user.address = request.data.get('address')
            user.save()
        if request.data.get('DOB') != None:
            user.DOB =request.data.get('DOB')
            user.save()
        if request.data.get('phone') != None:
            user.phone = request.data.get('phone')
            user.save()
        if request.data.get('profile_pic') != None:
            user.profile_pic = request.data.get('profile_pic')
            user.save()

        return JsonResponse({'success': True,
                             'message': 'User Saved'}, status=200)

    else:
            return JsonResponse({'success':False,
                                 'message':'User Did notSaved'}, status=400)




def in_card_view(request, pk):
    try:
        card_id = Post_Card.objects.get(pk=pk)
        print(card_id)
    except Exception as e:
        print(str(e))
        message=str(e)
        return JsonResponse({'message':message}, status=400)
    if request.method=='GET':
        a=card_id.user_id
        print(card_id.card_no)
        card_no = card_id.card_no
        id=card_id.id
        card_expiry = card_id.card_expiry
        sell_price=card_id.card_sell_price
        print(a)
        user=User.objects.filter(id=a)
        for data in user:
            print(data.name)
            name=data.name
            email=data.username
            address=data.address
            phone=data.phone
            DOB=data.DOB

        return JsonResponse({'name':name, 'address':address, 'phone':phone, 'DOB':DOB,
                             'card_no':card_no, 'card_expiry':card_expiry,'card_price':sell_price ,'email':email,'card_id':id}, status=200)




def in_seller_view(request, pk):
    try:
        user = User.objects.get(pk=pk)
        name=user.name
        address=user.address
        profile_pic=user.profile_pic
        id=user.id
        print(id)
    except Exception as e:
        message=str(e)
        print(str(e))
        return JsonResponse({'message': message}, status=400)
    if request.method=='GET':
        user=list(Post_Card.objects.filter(user_id=id).values('card_no', 'card_expiry', 'user', 'id'))
        print(user)
        return JsonResponse({'name': name, 'address':address,'profile_pic':str(profile_pic), 'card_no': user}, status=200)







def in_seller_dash(request):
    a = request.headers['Authorization']

    try:
        user = User.objects.get(auth_token=a)
        name=user.name
        id=user.id
        print(id)
    except Exception as e:
        message=str(e)
        print(str(e))
        return JsonResponse({'message':message}, status=400)
    if request.method=='GET':
        user=list(Post_Card.objects.filter(user_id=id).filter(is_verified_card=True).values('card_no', 'card_expiry', 'user'))
        print(user)
        return JsonResponse({'name': name, 'card_no': user}, status=200)




def all_sellers(request):
    a = True
    try:
        user = list(User.objects.filter(b_seller=a).values('name', 'profile_pic', 'address', 'id'))
        print(user)
    except Exception as e:
        message=str(e)
        print(str(e))
        return JsonResponse({'message':message}, status=400)
    if request.method=='GET':
        return JsonResponse({'name': user}, status=200)


@api_view(['GET'])
def Verify(request):
    try:
        user=Post_Card.objects.filter(is_verified_card=True)
    except Exception as e:
        message=str(e)
        return JsonResponse({'message':message}, status=400)
    if request.method=='GET':
        data=user.values()
        print(data)
        return Response(data, status=200)

