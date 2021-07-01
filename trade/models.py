from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django_resized import ResizedImageField

# Create your models here.
class User(AbstractUser):
    username = models.EmailField(max_length=50, unique=True)
    otp = models.IntegerField(null=True)
    under_verification_feature=models.BooleanField(default=False)
    verified_feature=models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    b_seller= models.BooleanField(default=False)
    is_verified_seller = models.BooleanField(default=False)
    something = models.BooleanField(default=False)
    name = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)
    DOB = models.DateField(null=True)
    profile_pic = ResizedImageField(size=[500, 300],force_format='PNG', blank=True, null=True)
    driving_license_front = ResizedImageField(size=[500, 300], force_format='PNG', blank=True, null=True)
    driving_license_back = ResizedImageField(size=[500, 300], force_format='PNG', blank=True, null=True)
    social_card = ResizedImageField(size=[500, 300], force_format='PNG', blank=True, null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Post_Card(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    is_verified_card = models.BooleanField(default=False)
    under_verification_card = models.BooleanField(default=False)
    card_image = ResizedImageField(size=[500, 300], force_format='PNG', blank=True, null=True)
    card_no = models.CharField(max_length=20, null=True)
    card_limit=models.FloatField(null=True)
    special_card=models.BooleanField(default=False)
    special_card_verification=models.BooleanField(default=False)
    special_card_posted=models.DateTimeField(null=True)
    card_expiry=models.DateField(null=True)
    realative_name = models.CharField(max_length=200, null=True)
    card_balance = models.FloatField(null=True)
    card_sell_price = models.FloatField(null=True)
    card_posted=models.DateTimeField( auto_created=True, auto_now_add=True)
    card_bid_price = models.FloatField(null=True)

class F_password(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    rest_password_time=models.DateTimeField(auto_now_add=True, auto_created=True)
    password_reset_code=models.IntegerField()




class Orders(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    card=models.IntegerField(null=True)



class Payment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.IntegerField(null=True)
    card_expiry=models.DateField(null=True)
    first_name=models.CharField(max_length=200, null=True)
    last_name=models.CharField(max_length=200, null=True)
    card_no=models.IntegerField(null=True)
    CVC=models.IntegerField(null=True)
    under_verification=models.BooleanField(default=False, null=True)
    verified=models.BooleanField(default=False, null=True)
    total_amount=models.IntegerField(default=0)







class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)


class AmountTracking(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    amount_id=models.CharField(max_length=2000, null=True)
    client_secret=models.CharField(max_length=2000, null=True)
    created=models.CharField(max_length=200, null=True)
    amount=models.IntegerField(default=0)

class CardPayment(models.Model):
    amount_id = models.CharField ( max_length=2000 , null=True )
    client_secret = models.CharField ( max_length=2000 , null=True )
    created = models.CharField ( max_length=200 , null=True )
    amount = models.IntegerField ( default=0 )

class AdminAmountData(models.Model):
    amount_id = models.CharField ( max_length=2000 , null=True )
    client_secret = models.CharField ( max_length=2000 , null=True )
    created = models.CharField ( max_length=200 , null=True )
    amount = models.IntegerField ( default=0 )


