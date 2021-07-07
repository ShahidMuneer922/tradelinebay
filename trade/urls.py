from django.urls import path
from .views import registration_view, f_pass
from .admin_views import UserViewSet
from .payment_views import AdminAccountViewSet
from . import feature_views, orders_views
from . import views, admin_views, special_card_views, del_card_views, confirm_card_views, message_views, payment_views
from .views import LoginAPI

# FOR LOGIN
# from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    # path('register/' , RegisterAPI.as_view(), name='register' ),
    # path('login/', obtain_auth_token, name='login'),

    path('seller/', views.seller),
    path('admin/users/', UserViewSet.as_view()),

    # FULLY DONE APIS

    path('admin/confirm_card_post/<pk>', admin_views.confirm_card_post),
    path('admin/post_card_view/', admin_views.post_card_view),
    path('in_card_view/<pk>/', views.in_card_view),
    path('in_seller_view/<pk>', views.in_seller_view),
    path('in_seller_dash/', views.in_seller_dash),  # THROUGH HEADERS
    path('all_sellers/', views.all_sellers),
    path('card_dashboard_view/', confirm_card_views.card_dashboard_view),
    path('pending_cards/', confirm_card_views.pending_cards),

    # For First Step registation and login apis
    path('register/', registration_view, name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('registration/', views.further_registration),  # THROUGH HEADER
    path('otp/', views.verify_email),  # THROUGH HEADER

    # FOR ADDING CARD
    path('add_card/', views.card),  # THROUGH HEADER

    # special cards apis
    path('del_special_card/', del_card_views.del_special_card),  # FOR DELETING SPECIAL CARDS
    path('verification_card/<pk>', special_card_views.verification_card),  # THROUGH ID     #For sending data to Admin
    path('special_card_confirm_view/', special_card_views.special_card_confirm_view),  # FOR GETING DATA ON DASH BOARD
    path('admin/special_card_view/', admin_views.special_card_view),  # FOR DISPLAYING DATA ON ADMIN SCREEN
    path('admin/special_card_verified/<pk>', admin_views.special_card_verified),  # FOR ACCEPTING AND REJECTING CARDS

    # FORGOT PASSWORD

    path('forgot_password/', views.forgot_password),  # send your email
    path('update/', views.update_user),  # THROUGH HEADER
    path('update_password/', views.update_password),  # THROUGH HEADER
    path('verify_code/<pk>/', views.verify_code),  # THROUGH ID
    path('f_pass/', f_pass.as_view()),

    # Payment Apis
    path('pay/', payment_views.test_payment),
    path('card_pay/', payment_views.card_pay),
    path('ascro_pay/', payment_views.wal_payment),
    path('admin/admin_account/', AdminAccountViewSet.as_view()),

    # ORDER CARDS
    path('order_card/', orders_views.order_card),
    path('admin/check_cards/', admin_views.check_cards),

    # MESSAGES
    path('messages/<int:sender>/<int:receiver>/', message_views.message_list, name='message-detail'),
    path('messages/', message_views.message_list, name='message-list'),
    path('chat/', message_views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>/', message_views.message_view, name='chat'),

    # for store dashboard
    path('verify/', views.verify),

    # Feature Seller apis
    path('feature_display/', feature_views.feature_confirm_view),
    path('admin/verified_feature_post/<pk>', admin_views.verified_feature),  # THROUGH ID    # FOR Making Feature seller
    path('admin/f_seller/', admin_views.feature_seller_view),  # For Getting ALL feature sellers
    path('f_button/', feature_views.Verification_feature_seller),  # For Feature Button  #THROUGH HEADER

    # seller apis

    path('admin/b_seller/', admin_views.b_seller_view),
    path('admin/seller_registration/<pk>', admin_views.become_seller_recognition),  # THROUGH ID
    path('admin/seller_registration_post/<pk>', admin_views.become_seller_recognition_view),  # THROUGH ID
    path('verification_seller/', views.verification_seller),  # THROUGH HEADER

    # For buyer dashboard data
    path('user_detail/', views.user_detail),  # THROUGH HEADER

]
