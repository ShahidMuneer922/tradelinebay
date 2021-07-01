from datetime import datetime, timedelta
from .models import Post_Card, F_password
from django.http import JsonResponse



def del_special_card(request):
    a=Post_Card.objects.filter(special_card_posted__lte=datetime.now() - timedelta(seconds=10))
    for b in a:
        print(b)
        print(b.special_card)
        b.special_card=False
        b.special_card_verification=False
        b.save()
    return JsonResponse({"success":True}, status=200)