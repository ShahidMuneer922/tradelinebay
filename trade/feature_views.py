import logging
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import User
from rest_framework.response import Response
from django.http import JsonResponse




@api_view(['POST'])
def Verification_feature_seller(request):
    logging.basicConfig(filename='success.log', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')
    a = request.headers['Authorization']
    try:
        user = User.objects.get(auth_token=a)
    except Exception as e:
        logging.info(f'{a} Does not Exist')
        return JsonResponse({'error': 'This user does not exist',
                             "success": False,
                             "message": str(e)}, status=400)

    if request.method == 'POST':
        verified = request.data['under_verification_feature']
        if user.under_verification_feature == True:
            return JsonResponse({'message':"Already verified waiting for admin response"})
        if verified == 'true':
            user.under_verification_feature = True
            user.save()
            logging.info(f'{user.username} verified user')
            return JsonResponse({"success": True,}, status=200)
        else:
            logging.info(f'{user.username} Can not verify seller')
            return JsonResponse({"Success": False},status=400)





@api_view(['GET'])
def feature_confirm_view(request):
    logging.basicConfig(filename='success.log', level=logging.INFO)
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    a = True
    try:
        user = User.objects.filter(verified_feature=a)
    except Exception as e:
        message=str(e)
        logging.error(f'{a} User Does not exist')
        return JsonResponse({"success": False,
                             'error': message}, status=400)

    if request.method == 'GET':
        data = user.values("name", "profile_pic", "address", 'id')
        logging.info(f'Got Data')
        return Response(data, status=200)
    else:
        logging.error(f'Cannot GET data')
        return JsonResponse({"success": False}, status=400)


