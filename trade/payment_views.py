import logging
import stripe
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import (AdminAmountData_Serializer
                          )
from django.contrib.auth.models import User
from .models import User, Payment, AmountTracking, CardPayment, AdminAmountData
from rest_framework.response import Response
from rest_framework import status








stripe.api_key ='sk_test_51J3fPdGdPGnE47TFotkx7pqydBRgEOB4eDYKa3JvJna5z67WMghGdmF3viw7Pt4wvk3LU7TJUbm5It42bfyfgy3000W4atIDWx'


@api_view(['POST', 'GET'])
def test_payment(request):
    try:
        header=request.headers['Authorization']
        user = User.objects.get ( auth_token=header )
    except Exception as e:
        a= str(e)
        return Response({'success':False,
                         'error':a})
    try:
        if request.method=="POST":

            print(user.id)
            a=request.data.get('amount')
            test_payment_intent = stripe.PaymentIntent.create(
            amount=a, currency='eur',
            payment_method_types=['card'],
            receipt_email='shahidmuneerawan@gmail.com')
            print(test_payment_intent['amount'])
            amount=test_payment_intent['amount']
            print(test_payment_intent['id'])
            id=test_payment_intent['id']
            print(test_payment_intent['client_secret'])
            s_id=test_payment_intent['client_secret']
            print(test_payment_intent['created'])
            c_no=test_payment_intent['created']
            amoun=AmountTracking.objects.filter(user=user).last()
            if amoun == None:
                my_amount=int(amount) * 0.2
                amount = int(amount) - my_amount
                amount = 0 + int(amount)
                AmountTracking.objects.create ( user=user , amount=amount , amount_id=id , client_secret=s_id ,
                                                created=c_no )
                return Response ( status=status.HTTP_200_OK , data=test_payment_intent )
            else:
                my_amount=int(amount) * 0.2
                amount = int(amount) - my_amount
                amount=int(amoun.amount) + int(amount)
                AmountTracking.objects.create(user=user, amount=amount, amount_id=id, client_secret=s_id, created=c_no)
                return Response ( status=status.HTTP_200_OK , data=test_payment_intent )

        if request.method =="GET":
            amount=AmountTracking.objects.filter(user=user).last()
            amount=amount.amount
            return Response( {'amount':amount})

    except Exception as e:
        if str(e)=="'NoneType' object has no attribute 'amount'":
            return Response({'success': True,
                             'amount': 0}, status=status.HTTP_200_OK)
        print(e)
        return Response(str(e), status=400)


@api_view(['POST'])
def card_pay(request):
    try:
        if request.method=="POST":

            a=request.data.get('amount')
            email=request.data.get('email')
            my_amount = int(a)
            my_amount = int (my_amount) * 0.2
            test_payment = stripe.PaymentIntent.create(
            amount=int(my_amount), currency='eur',
            payment_method_types=['card'],
            receipt_email='shahidmuneerawan@gmail.com')
            print ( test_payment['amount'] )
            amount = test_payment['amount']
            print ( test_payment['id'] )
            id = test_payment['id']
            print ( test_payment['client_secret'] )
            s_id = test_payment['client_secret']
            print ( test_payment['created'] )
            c_no = test_payment['created']
            z=AdminAmountData.objects.create(amount_id=id, client_secret=s_id, amount=amount, created=c_no)
            amount=int(a)-my_amount
            test_payment_intent = stripe.PaymentIntent.create(
            amount=int(amount), currency='eur',
            payment_method_types=['card'],
            receipt_email=email)
            print(test_payment_intent['amount'])
            amount=test_payment_intent['amount']
            print(test_payment_intent['id'])
            id=test_payment_intent['id']
            print(test_payment_intent['client_secret'])
            s_id=test_payment_intent['client_secret']
            print(test_payment_intent['created'])
            c_no=test_payment_intent['created']
            CardPayment.objects.create(amount_id=id, client_secret=s_id, amount=amount, created=c_no)
            return Response(data=test_payment_intent, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class AdminAccountViewSet(APIView):
    serializer_class = AdminAmountData
    logging.basicConfig(filename='success.log', level=logging.INFO)

    def get(self, request):
        user_data = AdminAmountData.objects.all()
        serializer = AdminAmountData_Serializer(user_data, many=True)
        logging.info('Got data')
        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST', 'GET'])
def wal_payment(request):
    try:
        header=request.headers['Authorization']
        user = User.objects.get ( auth_token=header )
    except Exception as e:
        a= str(e)
        return Response({'success':False,
                         'error':a})
    try:
        if request.method=='POST':
            a= AmountTracking.objects.filter(user=user).last()
            print(a.user)
            email=request.data.get('email')
            price=request.data.get('amount')
            amount=int(a.amount) - int(price)
            a.amount=amount
            if a.amount < 0:
                return Response({'success':False,
                                 'error':"Low Balance"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print(a.amount)
                test_payment_intent = stripe.PaymentIntent.create (
                    amount=int ( price ) , currency='eur' ,
                    payment_method_types=['card'] ,
                    receipt_email=email)
                a.save()
            return Response({'success':True,
                             "balance":a.amount,
                             'data':test_payment_intent}, status=status.HTTP_200_OK)
    except Exception as e:
        error=str(e)
        return Response({'success':False, 'error':error}, status=status.HTTP_400_BAD_REQUEST)
