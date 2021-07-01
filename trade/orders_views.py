import logging

from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Post_Card, F_password
from .models import User, Orders, AdminAmountData, AmountTracking, CardPayment
from rest_framework.response import Response
from django.http import JsonResponse
import stripe
stripe.api_key ='sk_test_51J3fPdGdPGnE47TFotkx7pqydBRgEOB4eDYKa3JvJna5z67WMghGdmF3viw7Pt4wvk3LU7TJUbm5It42bfyfgy3000W4atIDWx'




@api_view(['GET', 'POST'])
def order_card(request):
    logging.basicConfig(filename='success.log', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    a = request.headers['Authorization']
    print(a)
    # a='a551691e038e7dedea11ef558f69bc5ca80a7eed'
    try:
        user = User.objects.get(auth_token=a)
    except Exception as e:
        message=str(e)
        logging.info(f'{a} User Does not exist')
        return JsonResponse({'message': message}, status=400)


    if request.method=="GET":
        my_list = []
        data=list(Orders.objects.filter(user=user).values())
        for i in data:
            print(i)
            car=i['card']
            print(car)
            card=list(Post_Card.objects.filter(id=car).values('card_no', 'card_expiry', 'user'))
            my_list.append(card)
            # car = json.dumps(card, indent=4, sort_keys=True, default=str)


        return Response({"Cards": my_list}, content_type='application/json', status=200)
    try:
        if request.method =='POST':
            card=request.data['card_id']
            Orders.objects.create(user=user, card=card)
            car=Post_Card.objects.get(id=int(card))
            car.is_verified_card=False
            car.under_verification_card=False
            print(car.user)
            if request.data.get('type') =='card':
                a = request.data.get ( 'amount' )
                email = request.data.get ( 'email' )
                my_amount = int(a)
                my_amount = int(my_amount) * 0.2
                test_payment = stripe.PaymentIntent.create(
                    amount=int(my_amount), currency='eur',
                    payment_method_types=['card'],
                    receipt_email='shahidmuneerawan@gmail.com' )
                print ( test_payment['amount'] )
                amount = test_payment['amount']
                print ( test_payment['id'] )
                id = test_payment['id']
                print ( test_payment['client_secret'] )
                s_id = test_payment['client_secret']
                print ( test_payment['created'] )
                c_no = test_payment['created']
                z = AdminAmountData.objects.create ( amount_id=id , client_secret=s_id , amount=amount , created=c_no )
                amount = int ( a ) - my_amount
                test_payment_intent = stripe.PaymentIntent.create (
                    amount=int ( amount ) , currency='eur' ,
                    payment_method_types=['card'] ,
                    receipt_email=email )
                print ( test_payment_intent['amount'] )
                amount = test_payment_intent['amount']
                print ( test_payment_intent['id'] )
                id = test_payment_intent['id']
                print ( test_payment_intent['client_secret'] )
                s_id = test_payment_intent['client_secret']
                print ( test_payment_intent['created'] )
                c_no = test_payment_intent['created']
                CardPayment.objects.create ( amount_id=id , client_secret=s_id , amount=amount , created=c_no )
                car.save ()
                return Response ( {'data': test_payment_intent,
                                   'type': 'card'}, status=status.HTTP_200_OK )
            if request.data.get('type') == 'wallet':
                a = AmountTracking.objects.filter ( user=user ).last ()
                print ( a.user )
                price = request.data.get('amount')
                amount = int ( a.amount ) - int ( price )
                a.amount = amount
                if a.amount < 0:
                    return Response ( {'success': False ,
                                       'error': "Low Balance"} , status=status.HTTP_400_BAD_REQUEST )
                else:
                    print(a.amount)
                    test_payment = stripe.PaymentIntent.create(
                        amount=int(price) , currency='eur' ,
                        payment_method_types=['card'] ,
                        receipt_email=car.user )
                    a.save()
                    car.save ()
                return Response ( {'success': True ,
                                   "balance": a.amount,
                                   'type':"wallet",
                                   'data':test_payment} , status=status.HTTP_200_OK )

    except Exception as e:
        error=str(e)
        return Response({'error':error, 'success':False}, status=status.HTTP_400_BAD_REQUEST)


