from rest_framework import serializers
from . models import Post_Card, User, F_password, Message, Payment, AdminAmountData


class VerifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post_Card
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'date_joined', 'is_verified', 'otp', 'password', "is_superuser", "is_verified_seller", "auth_token", "b_seller", "name", 'something')
        # fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['password'])

        return user





class All_dataSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Post_Card
        # fields = ("card_image", "user","card_no", "realative_name", "card_credit", "card_sell_price", "card_bid_price", "verify_data")
        fields = "__all__"



class UseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ("name", "address", 'DOB', "profile_pic", 'driving_license_front', 'driving_license_back', 'social_card', 'phone', 'is_verified', 'is_verified_seller',"b_seller")
        fields = '__all__'


class UpdataeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=2,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'password',
                  'name',
                  'address',
                  'phone')
        read_only_fields = ('date_created', 'date_modified', 'username')

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
        else:
            instance.save()
            return instance

        instance.save()
        return instance




class f_serializer(serializers.ModelSerializer):
    class Meta:
        model = F_password
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']




class Payment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class AdminAmountData_Serializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAmountData
        fields = '__all__'
